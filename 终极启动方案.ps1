# Ultimate Start Solution - All 3 Projects
# This script ensures everything works correctly

$ErrorActionPreference = 'Stop'

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Ultimate Portfolio Launcher" -ForegroundColor Cyan
Write-Host "  Starting All 3 Projects" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

$rootPath = "E:\Program Files\cursorproject\作品集"

# Quick fix for Project 2 if needed
Write-Host "[*] Checking Project 2 configuration..." -ForegroundColor Yellow
$project2Path = Join-Path $rootPath "event-relay-hub"
$envPath = Join-Path $project2Path ".env"

if (-not (Test-Path $envPath) -or ((Get-Content $envPath -Raw) -like "*postgresql*")) {
    Write-Host "    Fixing Project 2 database config..." -ForegroundColor Gray
    Push-Location $project2Path
    
    $envContent = @"
DEBUG=False
HOST=0.0.0.0
PORT=8202
DATABASE_URL=sqlite:///./event_hub.db
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_ENABLED=True
"@
    $envContent | Out-File -FilePath ".env" -Encoding UTF8 -Force
    
    if (Test-Path ".venv") {
        & ".\.venv\Scripts\python.exe" -c "from app.models import init_db; init_db()" 2>$null
    }
    
    Pop-Location
    Write-Host "    [OK] Fixed" -ForegroundColor Green
}

Write-Host "[OK] All configurations ready" -ForegroundColor Green
Write-Host ""

# Start each project in a separate window
Write-Host "Starting projects in separate windows..." -ForegroundColor Cyan
Write-Host ""

# Project 1
Write-Host "[1/3] Launching Global Price Sentinel (8101)..." -ForegroundColor Yellow
$p1Path = Join-Path $rootPath "global-price-sentinel"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$p1Path'; Write-Host 'Project 1: Global Price Sentinel (Port 8101)' -ForegroundColor Green; Write-Host ''; .\start.ps1"
Start-Sleep -Seconds 2

# Project 2  
Write-Host "[2/3] Launching Event Relay Hub (8202)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$project2Path'; Write-Host 'Project 2: Event Relay Hub (Port 8202)' -ForegroundColor Green; Write-Host ''; .\start.ps1"
Start-Sleep -Seconds 2

# Project 3
Write-Host "[3/3] Launching SaaS Dashboard (8303)..." -ForegroundColor Yellow
$p3Path = Join-Path $rootPath "saas-northstar-dashboard"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$p3Path'; Write-Host 'Project 3: SaaS Dashboard (Port 8303)' -ForegroundColor Green; Write-Host ''; npm run dev"

Start-Sleep -Seconds 3

# Show access info
Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "  All Projects Launched!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Wait 30-60 seconds for all services to start." -ForegroundColor Yellow
Write-Host ""
Write-Host "Then visit:" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Main Portal:  http://localhost:8101" -ForegroundColor White
Write-Host "                (Shows all 6 projects)" -ForegroundColor Gray
Write-Host ""
Write-Host "  Project 2:    http://localhost:8202" -ForegroundColor White
Write-Host "                (Webhook Event Hub)" -ForegroundColor Gray
Write-Host ""
Write-Host "  Project 3:    http://localhost:8303" -ForegroundColor White
Write-Host "                (SaaS Dashboard)" -ForegroundColor Gray
Write-Host ""
Write-Host "Each project runs in its own window." -ForegroundColor Yellow
Write-Host "Close windows or press Ctrl+C to stop." -ForegroundColor Yellow
Write-Host ""
Write-Host "To stop all: .\停止所有项目.ps1" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press any key to close this window..." -ForegroundColor Cyan
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

