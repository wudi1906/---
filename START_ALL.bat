@echo off
chcp 65001 >nul
echo.
echo ============================================
echo   Portfolio Launcher - Starting All Projects
echo ============================================
echo.
echo Starting PowerShell script...
echo.

powershell -ExecutionPolicy Bypass -File "%~dp0start-all.ps1"

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to start services
    echo.
    pause
    exit /b 1
)

echo.
echo All services launched!
echo.
pause
