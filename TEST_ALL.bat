@echo off
chcp 65001 >nul
echo.
echo ============================================
echo   Testing All Services
echo ============================================
echo.

echo [1/6] Testing Project 1 (Port 8101)...
curl -s http://localhost:8101/api/health >nul 2>&1
if errorlevel 1 (
    echo   [FAIL] Project 1 not responding
) else (
    echo   [OK] Project 1 is running
)

echo.
echo [2/6] Testing Project 2 (Port 8202)...
curl -s http://localhost:8202/api/health >nul 2>&1
if errorlevel 1 (
    echo   [FAIL] Project 2 not responding
) else (
    echo   [OK] Project 2 is running
)

echo.
echo [3/6] Testing Project 3 (Port 8303)...
curl -s http://localhost:8303/api/health >nul 2>&1
if errorlevel 1 (
    echo   [FAIL] Project 3 not responding
) else (
    echo   [OK] Project 3 is running
)

echo.
echo [4/6] Testing Project 4 (Port 8404)...
curl -s http://localhost:8404/api/health >nul 2>&1
if errorlevel 1 (
    echo   [FAIL] Project 4 not responding
) else (
    echo   [OK] Project 4 is running
)

echo.
echo [5/6] Testing Project 5 (Port 8505)...
curl -s http://localhost:8505/ >nul 2>&1
if errorlevel 1 (
    echo   [FAIL] Project 5 not responding
) else (
    echo   [OK] Project 5 is running
)

echo.
echo [6/6] Testing Project 6 (Port 8606)...
curl -s http://localhost:8606/api/health >nul 2>&1
if errorlevel 1 (
    echo   [FAIL] Project 6 not responding
) else (
    echo   [OK] Project 6 is running
)

echo.
echo ============================================
echo   Test Complete
echo ============================================
echo.
pause

