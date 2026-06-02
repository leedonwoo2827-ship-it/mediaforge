"""voicewright 어댑터 — 번들 폴더 하나를 받아 음성/자막을 만든다.

voicewright는 원래 workspace/ch{NN}/audio 레이아웃으로 출력하지만, mp4maker는
번들 직속 audio/·subtitles/ 를 읽는다. 여기서 run_batch(flat_layout=True)로
번들에 직접 쓰도록 맞춘다.

공개 함수:
    synthesize(bundle_dir, only=None, ...)  → 전체 또는 특정 씬만 합성
    rebuild_chapter_srt(bundle_dir)         → 디스크의 per-scene SRT/WAV로 통합 SRT 재생성
"""
from __future__ import annotations

import re
from copy import deepcopy
from pathlib import Path

import soundfile as sf

from voicewright.batch import parse_script, run_batch
from voicewright.engine import Engine
from voicewright.paths import narration_filename, normalize_chapter_id
from voicewright.srt import merge_scene_cues, parse_srt_cues

_PER_SCENE_SRT_RE = re.compile(r"^ch[^_]+_(\d+)_narration\.srt$")


def _bundle_chapter_id(bundle_dir: Path) -> str | None:
    """번들 폴더 이름(ch90_bundle)에서 챕터 id('90')를 추출."""
    return normalize_chapter_id(bundle_dir.name.replace("_bundle", ""))


def find_script(bundle_dir: Path) -> Path:
    script_dir = bundle_dir / "script"
    hits = sorted(script_dir.glob("*_script.json"))
    if not hits:
        raise FileNotFoundError(f"대본 JSON이 없습니다: {script_dir}\\*_script.json")
    return hits[0]


async def synthesize(
    bundle_dir: str | Path,
    *,
    only: list[int] | None = None,
    voice_override: str | None = None,
    speed: float | None = None,
    total_step: int | None = None,
    on_progress=None,
) -> dict:
    """번들의 대본으로 음성(wav)+자막(srt)을 생성한다.

    only=None  → 전체 씬 배치
    only=[2,5] → 2,5번 씬만 재생성 (나머지는 디스크에 있던 것 유지)

    발음 교정은 config/pronunciation_map.yaml(웹 UI에서 편집) 를 합성 직전에
    자동 적용한다(engine 내부, 핫리로드). 단어 추가 후 그 씬만 재생성하면 반영됨.
    """
    bundle = Path(bundle_dir).resolve()
    script_path = find_script(bundle)
    script = parse_script(script_path.read_bytes())

    if only:
        wanted = set(int(n) for n in only)
        filtered = deepcopy(script)
        filtered.scenes = [sc for sc in script.scenes if sc.scene in wanted]
        if not filtered.scenes:
            raise ValueError(f"--only {sorted(wanted)} 에 해당하는 씬이 대본에 없습니다.")
        run_script = filtered
    else:
        run_script = script

    engine = await Engine.get()
    result = await run_batch(
        engine=engine,
        script=run_script,
        chapter_id_explicit=_bundle_chapter_id(bundle),
        filename_hint=script_path.name,
        output_root=bundle,
        voice_override=voice_override,
        speed=speed,
        total_step=total_step,
        on_progress=on_progress,
        flat_layout=True,
    )

    # 통합 SRT는 항상 디스크의 모든 per-scene SRT/WAV 기준으로 다시 만든다.
    # (부분 재생성 시 run_batch는 그 씬들만으로 통합 SRT를 만들기 때문에 보정 필요.
    #  사용자가 검수 탭에서 손본 per-scene SRT 타임코드도 이때 반영된다.)
    chapter_srt = rebuild_chapter_srt(bundle)

    return {
        "chapter": result.chapter_id,
        "bundle": str(bundle),
        "audio_dir": str(bundle / "audio"),
        "subtitles_dir": str(bundle / "subtitles"),
        "files": result.files,
        "chapter_srt": str(chapter_srt) if chapter_srt else None,
        "warnings": result.warnings,
        "scenes_done": [sc.scene for sc in run_script.scenes],
    }


def _wav_duration(path: Path) -> float:
    info = sf.info(str(path))
    return info.frames / float(info.samplerate)


def rebuild_chapter_srt(bundle_dir: str | Path) -> Path | None:
    """번들의 audio/*.wav + subtitles/*_narration.srt 를 모아 통합 chNN.srt 재생성.

    per-scene SRT(멀티큐)를 실측 오디오 길이만큼 누적 offset으로 병합한다.
    audio가 없는 씬은 통합 SRT에 넣지 못하므로 건너뛴다.
    """
    bundle = Path(bundle_dir).resolve()
    sub_dir = bundle / "subtitles"
    audio_dir = bundle / "audio"
    chapter_id = _bundle_chapter_id(bundle)
    if not sub_dir.exists() or chapter_id is None:
        return None

    scene_data: list[tuple[int, list, float]] = []
    for srt_p in sorted(sub_dir.glob("*_narration.srt")):
        m = _PER_SCENE_SRT_RE.match(srt_p.name)
        if not m:
            continue
        scene_num = int(m.group(1))
        wav_p = audio_dir / narration_filename(chapter_id, scene_num)
        if not wav_p.exists():
            continue
        cues = parse_srt_cues(srt_p.read_text(encoding="utf-8"))
        scene_data.append((scene_num, cues, _wav_duration(wav_p)))

    if not scene_data:
        return None

    scene_data.sort(key=lambda t: t[0])
    text = merge_scene_cues([(cues, dur) for _, cues, dur in scene_data])
    out = sub_dir / f"ch{chapter_id}.srt"
    out.write_text(text, encoding="utf-8")
    return out
