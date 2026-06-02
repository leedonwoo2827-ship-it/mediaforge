# mediaforge

이미지 → 음성/자막 → MP4를 **웹 화면 하나에서, 버튼 몇 개로** 만드는 로컬 도구.
**AI/LLM 호출 없음, 전부 내 PC(CPU)에서** 동작합니다. (voicewright TTS + mp4maker 합성을 합친 것)

---

## 무엇을 사람이 하고, 무엇이 자동인가

| 단계 | 누가 | 도구 |
|---|---|---|
| ① 대본 JSON 만들기 | 사람 | Claude / scriptforge (밖에서) |
| ② 이미지 만들기 | 사람 | **FlowGenie**(크롬 확장) → Google Flow |
| ③ 음성/자막 | **자동** | mediaforge (로컬 TTS) |
| ④ MP4 합성 | **자동** | mediaforge (ffmpeg) |

> 사람이 하는 건 **둘뿐**: ⓐ 대본 JSON 넣기 ⓑ Flow에서 이미지 받기.
> 그다음 mediaforge의 **⚡ 한 번에 만들기** 버튼이 가져오기→음성→합성을 한 번에 합니다.

⚠️ **mediaforge는 크롬 확장이 아닙니다.** 내 PC에서 켜고(`run.bat`) 브라우저로 `http://localhost:7878` 에 접속해 쓰는 **로컬 웹앱**입니다. 크롬에 설치하는 건 FlowGenie(이미지 생성)뿐입니다.

---

## 처음 설치하는 사람 (3단계)

### 0) 미리 필요한 것
- **Python 3.11 ~ 3.13** — https://www.python.org (설치 시 "Add to PATH" 체크)
- **ffmpeg** — Windows: `winget install Gyan.FFmpeg` (설치 후 새 터미널)
- **git + git-lfs** — https://git-scm.com , https://git-lfs.com (TTS 모델 다운로드에 필요)
- (이미지용) **FlowGenie** 크롬 확장 — 별도 저장소의 설치 안내 참고

### 1) 내려받기 + 설치
```powershell
git clone https://github.com/leedonwoo2827-ship-it/mediaforge.git
cd mediaforge
setup.bat            # 가상환경 + 의존성 + TTS 모델 자동 다운로드
```
`setup.bat` 이 하는 일: 가상환경(.venv) 생성 → 의존성 설치 → **TTS 모델 자동 다운로드**
(HuggingFace `Supertone/supertonic-3`, 약 380MB~1GB, **git-lfs 필요**).

> TTS 모델(약 380MB)은 GitHub 파일 한계를 넘어 저장소에 포함하지 않고 설치 때 받습니다.
> 이미 voicewright를 쓰던 PC라면 그 `assets/` 폴더를 mediaforge로 복사하거나(다운로드 생략),
> 환경변수 `VOICEWRIGHT_ASSETS_DIR` 로 그 경로를 가리켜도 됩니다.
> 모델 위치: `assets/onnx/*.onnx` + `assets/voice_styles/*.json`.

### 2) 실행 — run.bat 더블클릭
```
run.bat 더블클릭   →  브라우저가 http://localhost:7878 로 자동으로 열립니다
```
(터미널에서 `run.bat` 실행해도 됩니다. 창을 닫으면 종료.)

---

## 쓰는 순서

1. **새 번들 만들기** (`+ 새 번들`, 예: `ch90`). → `_assets/ch90_bundle/` 폴더가 생깁니다.
2. **[1 대본]** `_assets/ch90_bundle/script/` 에 대본 JSON(`ch90_script.json`)을 넣고 `↻`.
3. **[2 이미지]** `🔗 Flow 열기`로 이미지 생성 → 다운로드 → `📥 Downloads에서 가져오기`.
   - 한 씬을 여러 번 뽑으면 `_1,_2,…`가 쌓이는데 **가장 최근(마지막) 1장**만 가져옵니다.
4. **⚡ 한 번에 만들기** 한 방 → 음성/자막 + MP4까지 자동.
   - 이미지가 빠진 씬이 있으면 멈추고 "씬N 이미지 없음"을 알려줍니다.
5. **[4 결과]** 에서 미리보기 + 다운로드. 발음이 어색하면 `📖 발음 사전`에 단어 추가 후 다시 생성.

단계별로 따로 돌려도 됩니다: **[3 음성/자막] 🔊 생성**, **[4 결과] 🎬 풀 렌더**.

> 💡 **이미 이미지를 다 만들어 둔 경우**: Flow/가져오기 단계를 건너뛰어도 됩니다.
> 이미지를 `_assets/chNN_bundle/images/` 에 `chNN_XX_*` 이름으로 직접 넣고 바로
> **⚡ 한 번에 만들기**(또는 [3]→[4])를 누르면 됩니다.

---

## 폴더(번들) 규약
```
_assets/ch90_bundle/
  script/      ch90_script.json          ← 사람이 넣음
  images/      ch90_01_*.png             ← Flow에서 가져옴
  audio/       ch90_01_narration.wav     ← 자동(TTS)
  subtitles/   ch90_01_narration.srt     ← 자동
  draft/       ch90_final.mp4            ← 자동(합성)
```

## 더 읽기
- 운영/문제해결: [docs/](docs/) (RUN · BUNDLE · CLI · TROUBLESHOOTING · CUSTOMIZATIONS)
- 개념/배경: [knowledge/](knowledge/) (구조·왜 FlowGenie는 따로인지·발음사전·데이터흐름)

## 구성 / 라이선스
[voicewright](https://github.com/leedonwoo2827-ship-it/voicewright)(로컬 TTS)와
[mp4maker](https://github.com/leedonwoo2827-ship-it/mp4maker)(ffmpeg 합성)를 포함(vendor)해
통합 웹앱으로 묶은 것입니다. 두 코드의 수정 내역은 [docs/CUSTOMIZATIONS.md](docs/CUSTOMIZATIONS.md).
TTS 엔진은 Supertone Supertonic(모델은 HuggingFace에서 받음).

## 명령줄(고급)
```powershell
.venv\Scripts\activate
python ingest\import_images.py _assets\ch90_bundle      # 이미지 가져오기
python -m mp4maker _assets\ch90_bundle --probe          # 환경 점검
python -m mp4maker _assets\ch90_bundle --dry-run        # 검증만
python -m mp4maker _assets\ch90_bundle                  # 풀 렌더
```
