@echo off
chcp 65001 >nul
echo.
echo ============================================
echo   Starting All Portfolio Projects
echo ============================================
echo.

set ROOT=%~dp0

REM Fix Project 2 config
echo [*] Fixing Project 2 database config...
(
echo DEBUG=False
echo HOST=0.0.0.0
echo PORT=8202
echo DATABASE_URL=sqlite:///./event_hub.db
echo RATE_LIMIT_PER_MINUTE=60
echo RATE_LIMIT_ENABLED=True
) > "%ROOT%event-relay-hub\.env"
echo [OK] Config fixed
echo.

REM Start Project 1
echo [1/3] Starting Project 1 (Port 8101)...
start "Project 1 - Global Price Sentinel" cmd /k "cd /d \"%ROOT%global-price-sentinel\" && start.bat"
timeout /t 2 /nobreak >nul

REM Start Project 2
echo [2/3] Starting Project 2 (Port 8202)...
start "Project 2 - Event Relay Hub" cmd /k "cd /d \"%ROOT%event-relay-hub\" && start.bat"
timeout /t 2 /nobreak >nul

REM Start Project 3
echo [3/3] Starting Project 3 (Port 8303)...
start "Project 3 - SaaS Dashboard" cmd /k "cd /d \"%ROOT%saas-northstar-dashboard\" && start.bat"
timeout /t 2 /nobreak >nul

echo.
echo ============================================
echo   All Projects Started!
echo ============================================
echo.
echo Wait 30-60 seconds for all services to start.
echo.
echo Then visit:
echo   http://localhost:8101  (Main Portal)
echo   http://localhost:8202  (Event Hub)
echo   http://localhost:8303  (SaaS Dashboard)
echo.
echo Close windows or press Ctrl+C to stop services.
echo.
pause
