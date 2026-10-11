
@echo off
setlocal
cd /d "%~dp0"

if not exist "env\Scripts\python.exe" (
    echo ERROR: Virtual environment not found.
    echo Run setupdev.bat first.
    pause
    exit /b 1
)

if not exist "frontend\node_modules" (
    echo ERROR: Frontend dependencies not found.
    echo Run setupdev.bat first.
    pause
    exit /b 1
)

echo Starting FastAPI backend...
start "Voting API - FastAPI" /D "%~dp0" cmd /k "env\Scripts\python.exe -m uvicorn main:app --reload --host 127.0.0.1 --port 8000"

echo Starting React frontend...
start "Voting UI - React" /D "%~dp0frontend" cmd /k "npm run dev -- --host 127.0.0.1"

echo.
echo Backend:  http://127.0.0.1:8000
echo Swagger:  http://127.0.0.1:8000/docs
echo Frontend: http://127.0.0.1:5173
echo.
pause
