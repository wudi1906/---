# Fix Project 2 and Start All Projects

$ErrorActionPreference = 'Stop'

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Fixing Project 2 and Starting All" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

$rootPath = $PSScriptRoot

# First, fix Project 2
Write-Host "[*] Fixing Event Relay Hub (Project 2)..." -ForegroundColor Yellow
Write-Host ""

$project2Path = Join-Path $rootPath "event-relay-hub"
Push-Location $project2Path

# Remove old venv
if (Test-Path ".venv") {
    Write-Host "  Removing old venv..." -ForegroundColor Gray
    Remove-Item -Recurse -Force .venv
}

# Create new venv
Write-Host "  Creating new venv..." -ForegroundColor Gray
python -m venv .venv

# Activate and install
Write-Host "  Installing dependencies..." -ForegroundColor Gray
& ".\.venv\Scripts\python.exe" -m pip install --upgrade pip --quiet
& ".\.venv\Scripts\pip.exe" install -r requirements.txt --quiet

# Copy config
if (-not (Test-Path ".env")) {
    Copy-Item "env.example" ".env"
}

# Init DB
& ".\.venv\Scripts\python.exe" -c "from app.models import init_db; init_db()"

Pop-Location

Write-Host "[OK] Project 2 fixed!" -ForegroundColor Green
Write-Host ""

# Now start all projects in separate windows
Write-Host "Starting all projects..." -ForegroundColor Cyan
Write-Host ""

# Project 1
Write-Host "[1/3] Starting Project 1 (Port 8101)..." -ForegroundColor Yellow
$project1Path = Join-Path $rootPath "global-price-sentinel"
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "cd '$project1Path'; Write-Host 'Project 1: Global Price Sentinel' -ForegroundColor Green; Write-Host ''; .\start.ps1"
)
Start-Sleep -Seconds 2

# Project 2
Write-Host "[2/3] Starting Project 2 (Port 8202)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "cd '$project2Path'; Write-Host 'Project 2: Event Relay Hub' -ForegroundColor Green; Write-Host ''; .\start.ps1"
)
Start-Sleep -Seconds 2

# Project 3
Write-Host "[3/3] Starting Project 3 (Port 8303)..." -ForegroundColor Yellow
$project3Path = Join-Path $rootPath "saas-northstar-dashboard"
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "cd '$project3Path'; Write-Host 'Project 3: SaaS Dashboard' -ForegroundColor Green; Write-Host ''; npm run dev"
)

Start-Sleep -Seconds 3

# Display info
Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "  All Projects Started!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Please wait 30 seconds for services to start, then visit:" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Project 1: http://localhost:8101" -ForegroundColor White
Write-Host "  Project 2: http://localhost:8202" -ForegroundColor White
Write-Host "  Project 3: http://localhost:8303" -ForegroundColor White
Write-Host ""
Write-Host "Press any key to close this window..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

