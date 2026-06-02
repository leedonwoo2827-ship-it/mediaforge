@echo off
REM mediaforge 웹앱 실행 (Windows) — 더블클릭하면 브라우저가 자동으로 열립니다.
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
  echo [setup] 가상환경이 없습니다. 먼저 setup.bat 을 더블클릭해 설치하세요.
  pause
  exit /b 1
)

set "PYTHONPATH=%~dp0;%PYTHONPATH%"
echo [run] http://localhost:7878  (이 창을 닫으면 종료됩니다)

REM 서버가 뜨는 동안 브라우저를 먼저 띄워 둔다 (자동 새로고침됨)
start "" http://localhost:7878

".venv\Scripts\python.exe" -m uvicorn app.main:app --host 0.0.0.0 --port 7878
endlocal
