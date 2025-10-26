@echo off
setlocal DisableDelayedExpansion
pushd "%~dp0"
chcp 65001 >nul
echo.
echo ========================================
echo   Event Relay Hub
echo ========================================
echo.

REM Determine venv executables
set "VENV_PY=.venv\Scripts\python.exe"
set "VENV_PIP=.venv\Scripts\pip.exe"

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found
    pause
    popd
    exit /b 1
)

REM Create venv if not exists
if not exist ".venv\Scripts\python.exe" (
    echo [*] Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause & popd & exit /b 1
    )
    echo [OK] Virtual environment created
)

REM Generate .env (SQLite)
echo [*] Creating .env with SQLite...
(
    echo DEBUG=False
    echo HOST=0.0.0.0
    echo PORT=8202
    echo DATABASE_URL=sqlite:///./event_hub.db
    echo RATE_LIMIT_PER_MINUTE=60
    echo RATE_LIMIT_ENABLED=True
) > .env

REM Install dependencies
if not exist ".venv\Lib\site-packages\fastapi" (
    echo [*] Installing dependencies (please wait)...
    "%VENV_PY%" -m pip install --upgrade pip
    "%VENV_PIP%" install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] pip install failed
        pause & popd & exit /b 1
    )
    echo [OK] Dependencies installed
)

REM Init database
echo [*] Initializing database...
"%VENV_PY%" - <<PY
from app.models import init_db
init_db()
print('[OK] Database ready')
PY

echo.
echo ========================================
echo   Starting Server
echo ========================================
echo.
echo Main Page:  http://localhost:8202
echo API Docs:   http://localhost:8202/api/docs
echo.
echo Press Ctrl+C to stop
echo.

"%VENV_PY%" -m uvicorn app.main:app --host 0.0.0.0 --port 8202 --reload

popd
endlocal
