@echo off
setlocal DisableDelayedExpansion
pushd "%~dp0"
chcp 65001 >nul
echo.
echo ========================================
echo   Insight Viz Studio
echo ========================================
echo.

set "VENV_PY=.venv\Scripts\python.exe"
set "VENV_PIP=.venv\Scripts\pip.exe"

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found
    pause & popd & exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo [*] Creating virtual environment...
    python -m venv .venv
    echo [OK] Virtual environment created
)

if not exist ".venv\Lib\site-packages\fastapi" (
    echo [*] Installing dependencies...
    "%VENV_PY%" -m pip install --upgrade pip
    "%VENV_PIP%" install -r requirements.txt
    echo [OK] Dependencies installed
)

if not exist ".env" copy /Y env.example .env >nul

if not exist "uploads" mkdir uploads >nul
if not exist "exports" mkdir exports >nul

echo.
echo ========================================
echo   Starting Server
echo ========================================
echo.
echo Main Page:  http://localhost:8606
echo API Docs:   http://localhost:8606/api/docs
echo.
echo Press Ctrl+C to stop
echo.

"%VENV_PY%" -m uvicorn app.main:app --host 0.0.0.0 --port 8606 --reload

popd
endlocal

