# Ultimate Start Script - Simplified and Reliable
# Starts all 3 projects in separate windows

$ErrorActionPreference = 'Stop'

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Starting All Projects in Separate Windows" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

$rootPath = $PSScriptRoot

# Project 1: Global Price Sentinel
Write-Host "[1/3] Starting Global Price Sentinel (Port 8101)..." -ForegroundColor Yellow
$project1Path = Join-Path $rootPath "global-price-sentinel"

Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "cd '$project1Path'; Write-Host 'Project 1: Global Price Sentinel' -ForegroundColor Green; .\start.ps1"
)

Start-Sleep -Seconds 2

# Project 2: Event Relay Hub
Write-Host "[2/3] Starting Event Relay Hub (Port 8202)..." -ForegroundColor Yellow
$project2Path = Join-Path $rootPath "event-relay-hub"

Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "cd '$project2Path'; Write-Host 'Project 2: Event Relay Hub' -ForegroundColor Green; .\start.ps1"
)

Start-Sleep -Seconds 2

# Project 3: SaaS Dashboard
Write-Host "[3/3] Starting SaaS Dashboard (Port 8303)..." -ForegroundColor Yellow
$project3Path = Join-Path $rootPath "saas-northstar-dashboard"

Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "cd '$project3Path'; Write-Host 'Project 3: SaaS Dashboard' -ForegroundColor Green; if (-not (Test-Path 'node_modules')) { Write-Host 'Installing dependencies (first time)...' -ForegroundColor Yellow; npm install }; npm run dev"
)

Start-Sleep -Seconds 3

# Display access info
Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "  All Projects Started!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Access your projects:" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Project 1: http://localhost:8101" -ForegroundColor White
Write-Host "    (Global Price Sentinel - Main Portal)" -ForegroundColor Gray
Write-Host ""
Write-Host "  Project 2: http://localhost:8202" -ForegroundColor White
Write-Host "    (Event Relay Hub)" -ForegroundColor Gray
Write-Host ""
Write-Host "  Project 3: http://localhost:8303" -ForegroundColor White
Write-Host "    (SaaS Northstar Dashboard)" -ForegroundColor Gray
Write-Host ""
Write-Host "Each project is running in its own window." -ForegroundColor Yellow
Write-Host "Close the window or press Ctrl+C to stop each service." -ForegroundColor Yellow
Write-Host ""
Write-Host "To stop all at once, run: .\停止所有项目.ps1" -ForegroundColor Yellow
Write-Host ""

# Wait for user
Write-Host "Press any key to close this window..." -ForegroundColor Cyan
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

