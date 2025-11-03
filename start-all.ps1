# start-all.ps1 - launch all six portfolio projects
# Usage: powershell -ExecutionPolicy Bypass -File .\start-all.ps1

$ErrorActionPreference = 'Stop'

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Portfolio Launcher - Starting All Projects" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

$root = $PSScriptRoot

# Ensure Event Relay Hub has correct .env configuration
$eventHubEnv = @"
DEBUG=False
HOST=0.0.0.0
PORT=8202
DATABASE_URL=sqlite:///./event_hub.db
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_ENABLED=True
"@

Write-Host "Fixing Event Relay Hub configuration..." -ForegroundColor Yellow
$envPath = Join-Path $root "event-relay-hub\.env"
Set-Content -Path $envPath -Value $eventHubEnv -Encoding ASCII -Force
Write-Host "  [OK] Config updated" -ForegroundColor Green
Write-Host ""

$p1 = Join-Path $root "global-price-sentinel"
$p2 = Join-Path $root "event-relay-hub"
$p3 = Join-Path $root "saas-northstar-dashboard"
$p4 = Join-Path $root "doc-knowledge-forge"
$p5 = Join-Path $root "a11y-component-atlas"
$p6 = Join-Path $root "insight-viz-studio"

Write-Host "[1/6] Starting Global Price Sentinel (Port 8101)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$p1'; .\start.ps1" | Out-Null
Start-Sleep -Seconds 3

Write-Host "[2/6] Starting Event Relay Hub (Port 8202)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$p2'; .\start.ps1" | Out-Null
Start-Sleep -Seconds 3

Write-Host "[3/6] Starting SaaS Northstar Dashboard (Port 8303)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$p3'; npm run dev" | Out-Null
Start-Sleep -Seconds 3

Write-Host "[4/6] Starting Doc Knowledge Forge (Port 8404)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$p4'; .\start.bat" | Out-Null
Start-Sleep -Seconds 3

Write-Host "[5/6] Starting A11y Component Atlas (Port 8505)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$p5'; npm run storybook" | Out-Null
Start-Sleep -Seconds 3

Write-Host "[6/6] Starting Insight Viz Studio (Port 8606)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$p6'; .\start.bat" | Out-Null
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "  All Projects Launched!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "Wait 30-60 seconds, then visit:" -ForegroundColor Cyan
Write-Host "  http://localhost:8101  (Main Portal)" -ForegroundColor White
Write-Host "  http://localhost:8202  (Event Relay Hub)" -ForegroundColor White
Write-Host "  http://localhost:8303  (SaaS Dashboard)" -ForegroundColor White
Write-Host "  http://localhost:8404  (Doc Knowledge Forge)" -ForegroundColor White
Write-Host "  http://localhost:8505  (A11y Component Atlas - Storybook)" -ForegroundColor White
Write-Host "  http://localhost:8606  (Insight Viz Studio)" -ForegroundColor White
Write-Host ""
Write-Host "Use stop-all.ps1 to stop every service." -ForegroundColor Yellow
Read-Host "Press Enter to close this window"
