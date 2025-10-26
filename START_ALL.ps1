# START ALL PROJECTS - Simple English Only Script
# No special characters to avoid encoding issues

$ErrorActionPreference = 'Stop'

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Portfolio Launcher - Starting All" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

$root = "E:\Program Files\cursorproject\作品集"

# Fix Project 2 config first
Write-Host "Fixing Project 2 database config..." -ForegroundColor Yellow
$p2 = Join-Path $root "event-relay-hub"
$envFile = Join-Path $p2 ".env"

$envText = @"
DEBUG=False
HOST=0.0.0.0
PORT=8202
DATABASE_URL=sqlite:///./event_hub.db
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_ENABLED=True
"@

$envText | Out-File -FilePath $envFile -Encoding ASCII -Force
Write-Host "Config fixed!" -ForegroundColor Green
Write-Host ""

# Start Project 1
Write-Host "Starting Project 1 on port 8101..." -ForegroundColor Yellow
$p1 = Join-Path $root "global-price-sentinel"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$p1'; .\start.ps1"
Start-Sleep -Seconds 3

# Start Project 2
Write-Host "Starting Project 2 on port 8202..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$p2'; .\start.ps1"
Start-Sleep -Seconds 3

# Start Project 3
Write-Host "Starting Project 3 on port 8303..." -ForegroundColor Yellow
$p3 = Join-Path $root "saas-northstar-dashboard"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$p3'; npm run dev"
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "  All Projects Started!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "Wait 30 seconds, then visit:" -ForegroundColor Cyan
Write-Host ""
Write-Host "  http://localhost:8101  (Main Portal)" -ForegroundColor White
Write-Host "  http://localhost:8202  (Event Hub)" -ForegroundColor White
Write-Host "  http://localhost:8303  (SaaS Dashboard)" -ForegroundColor White
Write-Host ""
Write-Host "Press Enter to close this window..." -ForegroundColor Yellow
Read-Host

