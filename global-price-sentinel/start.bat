@echo off
setlocal DisableDelayedExpansion
pushd "%~dp0"
chcp 65001 >nul
echo.
echo ========================================
echo   Global Price Sentinel
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

REM Install dependencies
if not exist ".venv\Lib\site-packages\fastapi" (
    echo [*] Installing dependencies (this may take several minutes)...
    "%VENV_PY%" -m pip install --upgrade pip
    if errorlevel 1 echo [WARN] pip upgrade failed
    "%VENV_PIP%" install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] pip install failed
        pause & popd & exit /b 1
    )
    echo [*] Installing Playwright browsers...
    "%VENV_PY%" -m playwright install chromium
    echo [OK] Dependencies installed
)

REM Copy config
if not exist ".env" (
    echo [*] Creating .env file...
    copy /Y env.example .env >nul
)

if not exist "configs" mkdir configs >nul

REM Init database
echo [*] Initializing database...
"%VENV_PY%" -c "from app.models import init_db; init_db(); print('[OK] Database ready')"

REM Ensure dirs
if not exist "reports" mkdir reports >nul
if not exist "screenshots" mkdir screenshots >nul

echo.
echo ========================================
echo   Starting Server
echo ========================================
echo.
echo Main Page:  http://localhost:8101
echo API Docs:   http://localhost:8101/api/docs
echo.
echo Press Ctrl+C to stop
echo.

REM Start server using venv python
"%VENV_PY%" -m uvicorn app.main:app --host 0.0.0.0 --port 8101 --reload

popd
endlocal
