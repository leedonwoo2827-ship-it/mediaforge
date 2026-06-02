@echo off
REM mediaforge 설치 (Windows) — 가상환경 + 의존성 + TTS 모델
setlocal
cd /d "%~dp0"

where python >nul 2>nul || (echo [error] Python 3.11~3.13 을 먼저 설치하세요. & exit /b 1)

echo [setup] 가상환경 생성 (.venv)
if not exist ".venv\Scripts\python.exe" python -m venv .venv || exit /b 1

echo [setup] 의존성 설치
".venv\Scripts\python.exe" -m pip install --upgrade pip
".venv\Scripts\python.exe" -m pip install -r requirements.txt || exit /b 1

echo [setup] ffmpeg 확인
where ffmpeg >nul 2>nul || echo [warn] ffmpeg 가 PATH 에 없습니다. winget install Gyan.FFmpeg 로 설치하세요.

echo [setup] TTS 모델 확인 (assets\onnx)
if exist "assets\onnx\vocoder.onnx" (
  echo   모델 이미 있음 — 건너뜀.
) else (
  echo   모델이 없습니다. HuggingFace에서 다운로드합니다 ^(약 380MB~1GB, git-lfs 필요^).
  echo   ^(이미 다른 PC의 assets 폴더가 있으면 Ctrl+C 후 그걸 복사해도 됩니다^)
  powershell -ExecutionPolicy Bypass -File "scripts\setup_assets.ps1"
)

echo.
echo [setup] 완료. run.bat 더블클릭 → 브라우저가 자동으로 열립니다.
endlocal
