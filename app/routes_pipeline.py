"""mediaforge 파이프라인 API (/api/mf/*).

번들 단위로: 대본 확인 → 이미지 가져오기 → 음성/자막 → MP4 합성, 그리고
⚡ 한 번에. 무거운 작업(음성/렌더)은 백그라운드 작업으로 돌리고 폴링한다.
"""
from __future__ import annotations

import asyncio
import json
import mimetypes
from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from ingest.import_images import import_from_downloads

from . import bundles
from .jobs import Job, get_registry
from .render import probe as mp4_probe
from .render import render as mp4_render
from .synth import synthesize

router = APIRouter()

_VALID_KINDS = ("images", "audio", "subtitles", "draft", "script")


# ----------------------------- 요청 모델 -----------------------------
class CreateBundleReq(BaseModel):
    name: str


class ImportReq(BaseModel):
    prefer: str = "latest"
    downloads: str | None = None
    move: bool = False


class SynthReq(BaseModel):
    only: list[int] | None = None
    voice_override: str | None = None
    speed: float | None = None


class RenderReq(BaseModel):
    only: list[int] | None = None
    dry_run: bool = False
    keep_work: bool = False


# ----------------------------- 번들 -----------------------------
@router.get("/bundles")
async def get_bundles() -> dict:
    return {"bundles": bundles.list_bundles()}


@router.post("/bundles")
async def post_bundle(req: CreateBundleReq) -> dict:
    root = bundles.create_bundle(req.name.strip())
    return {"bundle": root.name, "path": str(root)}


@router.get("/bundles/{name}/status")
async def get_status(name: str) -> dict:
    return bundles.bundle_status(name)


@router.get("/bundles/{name}/script")
async def get_script(name: str) -> dict:
    root = bundles.bundle_path(name)
    sp = bundles.find_script(root)
    if not sp:
        raise HTTPException(404, f"{name}/script/*_script.json 없음")
    try:
        data = json.loads(sp.read_text(encoding="utf-8"))
    except Exception as exc:
        raise HTTPException(422, f"대본 JSON 파싱 실패: {exc}") from exc
    return {"file": sp.name, "data": data}


# ----------------------------- 이미지 가져오기 -----------------------------
@router.post("/bundles/{name}/import_images")
async def import_images(name: str, req: ImportReq) -> dict:
    root = bundles.bundle_path(name)
    if not root.is_dir():
        raise HTTPException(404, f"번들 없음: {name}")
    try:
        rows = import_from_downloads(root, downloads=req.downloads,
                                     prefer=req.prefer, move=req.move)
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc
    return {"imported": rows, "status": bundles.bundle_status(name)}


# ----------------------------- 작업(음성/렌더/한번에) -----------------------------
def _spawn(coro) -> None:
    asyncio.create_task(coro)


async def _job_synth(job: Job, name: str, req: SynthReq) -> None:
    reg = get_registry()
    try:
        job.status = "running"
        job.stage = "음성/자막 생성"
        root = bundles.bundle_path(name)

        def cb(completed: int, total: int, scene: int | None):
            job.completed, job.total = completed, total
            job.stage = f"음성/자막 생성 (씬 {scene})" if scene else "음성/자막 생성"
            job.add_log(f"씬 {scene}: {completed}/{total}")

        result = await synthesize(
            root, only=req.only, voice_override=req.voice_override,
            speed=req.speed, on_progress=cb,
        )
        reg.finish(job, status="done", result=result)
    except Exception as exc:  # noqa: BLE001
        reg.finish(job, status="error", error=str(exc))


async def _job_render(job: Job, name: str, req: RenderReq) -> None:
    reg = get_registry()
    try:
        job.status = "running"
        job.stage = "MP4 합성"
        root = bundles.bundle_path(name)

        def on_event(ev: dict):
            t = ev.get("type")
            if t == "progress":
                job.completed, job.total = ev["completed"], ev["total"]
                job.stage = f"MP4 합성 (씬 {ev['scene']})"
            elif t == "log":
                job.add_log(ev["line"])

        res = await mp4_render(root, only=req.only, dry_run=req.dry_run,
                               keep_work=req.keep_work, on_event=on_event)
        if res["ok"]:
            reg.finish(job, status="done", result=res)
        else:
            reg.finish(job, status="error",
                       error=f"mp4maker 종료코드 {res['returncode']}", result=res)
    except Exception as exc:  # noqa: BLE001
        reg.finish(job, status="error", error=str(exc))


async def _job_oneclick(job: Job, name: str) -> None:
    """⚡ 이미지 가져오기 → 음성/자막 → MP4. 누락/실패 시 그 단계에서 멈춤."""
    reg = get_registry()
    try:
        job.status = "running"
        root = bundles.bundle_path(name)

        # 1) 이미지 가져오기
        job.stage = "이미지 가져오기"
        rows = import_from_downloads(root)
        job.add_log(f"이미지 {len(rows)}개 씬 가져옴")
        st = bundles.bundle_status(name)
        if not st.get("has_script"):
            reg.finish(job, status="error", error="대본(script/*_script.json)이 없습니다.")
            return
        if st["missing_images"]:
            miss = ", ".join(f"씬{n}" for n in st["missing_images"])
            reg.finish(job, status="error",
                       error=f"{miss} 이미지 없음 — Flow에서 받아 Downloads에 두세요.")
            return

        # 2) 음성/자막 (오디오 누락 씬이 있을 때만)
        if st["missing_audio"]:
            job.stage = "음성/자막 생성"

            def cb(completed, total, scene):
                job.completed, job.total = completed, total
                job.stage = f"음성/자막 생성 (씬 {scene})" if scene else "음성/자막 생성"
            await synthesize(root, on_progress=cb)
            job.add_log("음성/자막 생성 완료")
        else:
            job.add_log("음성/자막 이미 존재 — 건너뜀")

        # 3) MP4 합성
        job.stage = "MP4 합성"

        def on_event(ev):
            if ev.get("type") == "progress":
                job.completed, job.total = ev["completed"], ev["total"]
                job.stage = f"MP4 합성 (씬 {ev['scene']})"
            elif ev.get("type") == "log":
                job.add_log(ev["line"])

        res = await mp4_render(root, on_event=on_event)
        if not res["ok"]:
            reg.finish(job, status="error",
                       error=f"MP4 합성 실패 (종료코드 {res['returncode']})", result=res)
            return
        reg.finish(job, status="done",
                   result={"final_mp4": res["final_mp4"], "outputs": res["outputs"],
                           "status": bundles.bundle_status(name)})
    except Exception as exc:  # noqa: BLE001
        reg.finish(job, status="error", error=str(exc))


@router.post("/bundles/{name}/synth")
async def post_synth(name: str, req: SynthReq) -> dict:
    job = get_registry().create(kind="synth", bundle=name)
    _spawn(_job_synth(job, name, req))
    return {"job_id": job.job_id}


@router.post("/bundles/{name}/render")
async def post_render(name: str, req: RenderReq) -> dict:
    job = get_registry().create(kind="render", bundle=name)
    _spawn(_job_render(job, name, req))
    return {"job_id": job.job_id}


@router.post("/bundles/{name}/oneclick")
async def post_oneclick(name: str) -> dict:
    job = get_registry().create(kind="oneclick", bundle=name)
    _spawn(_job_oneclick(job, name))
    return {"job_id": job.job_id}


@router.get("/jobs/{job_id}")
async def get_job(job_id: str) -> dict:
    job = get_registry().get(job_id)
    if job is None:
        raise HTTPException(404, "job not found")
    return job.to_dict()


# ----------------------------- 파일 서빙 (썸네일/미리듣기/다운로드) -----------------------------
@router.get("/file/{name}/{kind}/{filename}")
async def serve_file(name: str, kind: str, filename: str) -> FileResponse:
    if kind not in _VALID_KINDS:
        raise HTTPException(404, "unknown kind")
    if "/" in filename or "\\" in filename or filename.startswith(".."):
        raise HTTPException(400, "invalid filename")
    p = bundles.bundle_path(name) / kind / filename
    if not p.is_file():
        raise HTTPException(404, "file not found")
    media, _ = mimetypes.guess_type(str(p))
    return FileResponse(str(p), media_type=media or "application/octet-stream", filename=filename)


@router.get("/probe")
async def probe() -> dict:
    return await mp4_probe()
