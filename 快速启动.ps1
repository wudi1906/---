# Quick Start - Simplified version
# Only starts Project 1 (most stable)

$ErrorActionPreference = 'Stop'

Write-Host ""
Write-Host "Quick Start - Project 1 Only" -ForegroundColor Cyan
Write-Host ""

cd "$PSScriptRoot\global-price-sentinel"

# Check venv
if (-not (Test-Path ".venv")) {
    Write-Host "[*] First time setup..." -ForegroundColor Yellow
    python -m venv .venv
}

# Activate
& ".\.venv\Scripts\Activate.ps1"

# Install if needed
if (-not (Test-Path ".\.venv\Lib\site-packages\fastapi")) {
    Write-Host "[*] Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt --quiet
    playwright install chromium
}

# Copy config
if (-not (Test-Path ".env")) {
    Copy-Item "env.example" ".env"
}

# Init DB
python -c "from app.models import init_db; init_db()" 2>$null

# Start
Write-Host ""
Write-Host "Starting service..." -ForegroundColor Green
Write-Host "Visit: http://localhost:8101" -ForegroundColor Cyan
Write-Host ""

uvicorn app.main:app --host 0.0.0.0 --port 8101 --reload

