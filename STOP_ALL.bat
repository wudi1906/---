@echo off
echo.
echo Stopping all services...
echo.

REM Kill processes on ports
for %%p in (8101 8202 8303) do (
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":%%p "') do (
        taskkill /F /PID %%a >nul 2>&1
    )
    echo Stopped port %%p
)

echo.
echo All services stopped.
echo.
pause

