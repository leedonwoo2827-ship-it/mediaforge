@echo off
chcp 65001 >nul
REM mediaforge web app launcher. Run setup.bat first. Browser opens automatically.
REM --reload restarts the server when code (app/ingest/voicewright/mp4maker) changes.
REM Output folders (_assets/assets) are NOT watched, so synthesis is not interrupted.
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
  echo [setup] Virtual environment not found. Run setup.bat first.
  pause
  exit /b 1
)

set "PYTHONPATH=%~dp0;%PYTHONPATH%"
echo [run] Open http://localhost:7878 in your browser  (close this window to stop)

start "" http://localhost:7878

".venv\Scripts\python.exe" -m uvicorn app.main:app --host 127.0.0.1 --port 7878 --reload --reload-dir app --reload-dir ingest --reload-dir voicewright --reload-dir mp4maker
endlocal
