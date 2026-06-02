@echo off
chcp 65001 >nul
REM mediaforge web app launcher. Double-click to run; browser opens automatically.
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
  echo [setup] Virtual environment not found. Run setup.bat first.
  pause
  exit /b 1
)

set "PYTHONPATH=%~dp0;%PYTHONPATH%"
echo [run] mediaforge -^> http://localhost:7878   (close this window to stop)

REM open the browser; the page auto-refreshes once the server is up
start "" http://localhost:7878

REM --reload: 코드(app/ingest/voicewright/mp4maker)가 바뀌면 자동 재시작.
REM   _assets/assets(출력·모델)는 감시하지 않음 → 합성 중 끊기지 않음.
".venv\Scripts\python.exe" -m uvicorn app.main:app --host 0.0.0.0 --port 7878 ^
  --reload --reload-dir app --reload-dir ingest --reload-dir voicewright --reload-dir mp4maker
endlocal
