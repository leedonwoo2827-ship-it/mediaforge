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

".venv\Scripts\python.exe" -m uvicorn app.main:app --host 0.0.0.0 --port 7878
endlocal
