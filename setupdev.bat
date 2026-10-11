
@echo off
setlocal
cd /d "%~dp0"

echo ==========================================
echo Community Digital Voting System - Setup
echo ==========================================

if not exist "env\Scripts\python.exe" (
    echo Creating Python virtual environment...
    python -m venv env
    if errorlevel 1 goto error
)

echo Installing backend dependencies...
call "env\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto error

if not exist "alembic.ini" (
    echo ERROR: alembic.ini not found.
    echo Check the database migration configuration.
    goto error
)

if not exist "migrations\env.py" (
    echo ERROR: migrations\env.py not found.
    goto error
)

if not exist "migrations\versions" (
    echo ERROR: migrations\versions directory not found.
    goto error
)

echo Applying database migrations...
call "env\Scripts\python.exe" -m alembic upgrade head
if errorlevel 1 goto error

echo Loading sample data (skipped if the database already has proposals)...
call "env\Scripts\python.exe" seed_db.py
if errorlevel 1 goto error

if not exist "frontend\package.json" (
    echo ERROR: frontend\package.json not found.
    goto error
)

echo Installing frontend dependencies...
pushd frontend
call npm install
if errorlevel 1 (
    popd
    goto error
)
popd

echo.
echo Setup completed successfully.
pause
exit /b 0

:error
echo.
echo Setup failed. Review the error messages above.
pause
exit /b 1
