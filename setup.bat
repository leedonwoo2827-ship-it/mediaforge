@echo off
chcp 65001 >nul
REM mediaforge setup (Windows): virtual env + dependencies + TTS models
setlocal
cd /d "%~dp0"

where python >nul 2>nul || (echo [error] Install Python 3.11-3.13 first. & pause & exit /b 1)

echo [setup] Creating virtual environment (.venv)
if not exist ".venv\Scripts\python.exe" python -m venv .venv || (pause & exit /b 1)

echo [setup] Installing dependencies
".venv\Scripts\python.exe" -m pip install --upgrade pip
".venv\Scripts\python.exe" -m pip install -r requirements.txt || (pause & exit /b 1)

echo [setup] Checking ffmpeg
where ffmpeg >nul 2>nul || echo [warn] ffmpeg not on PATH. Install: winget install Gyan.FFmpeg

echo [setup] Checking TTS models (assets\onnx)
if exist "assets\onnx\vocoder.onnx" (
  echo   models already present - skip.
) else (
  echo   models not found. Downloading from HuggingFace ^(~380MB-1GB, needs git-lfs^).
  echo   ^(or copy an existing assets folder from another PC and press Ctrl+C^)
  powershell -ExecutionPolicy Bypass -File "scripts\setup_assets.ps1"
)

echo.
echo [setup] Done. Double-click run.bat (the browser opens automatically).
pause
endlocal
