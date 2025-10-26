@echo off
pushd "%~dp0"
chcp 65001 >nul
echo.
echo ========================================
echo   SaaS Northstar Dashboard
echo ========================================
echo.

echo [*] Installing dependencies if needed...
if not exist "node_modules" (
    npm install
)

echo.
echo Starting Next.js dev server on port 8303...
echo Press Ctrl+C to stop

echo.
npm run dev

popd
