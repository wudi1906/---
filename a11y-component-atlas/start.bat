@echo off
pushd "%~dp0"
chcp 65001 >nul
echo.
echo ========================================
echo   A11y Component Atlas
echo ========================================
echo.

echo [*] Installing dependencies if needed...
if not exist "node_modules" (
    npm install
)

echo.
echo Starting Storybook on port 8505...
echo Press Ctrl+C to stop
echo.

npm run storybook

popd

