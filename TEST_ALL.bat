@echo off
chcp 65001 >nul
echo.
echo ============================================
echo   Testing All Services
echo ============================================
echo.

echo [1/3] Testing Project 1 (Port 8101)...
curl -s http://localhost:8101/api/health >nul 2>&1
if errorlevel 1 (
    echo   [FAIL] Project 1 not responding
) else (
    echo   [OK] Project 1 is running
)

echo.
echo [2/3] Testing Project 2 (Port 8202)...
curl -s http://localhost:8202/api/health >nul 2>&1
if errorlevel 1 (
    echo   [FAIL] Project 2 not responding
) else (
    echo   [OK] Project 2 is running
)

echo.
echo [3/3] Testing Project 3 (Port 8303)...
curl -s http://localhost:8303 >nul 2>&1
if errorlevel 1 (
    echo   [FAIL] Project 3 not responding
) else (
    echo   [OK] Project 3 is running
)

echo.
echo ============================================
echo   Test Complete
echo ============================================
echo.
pause

