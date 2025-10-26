# Fix and Start Event Relay Hub

$ErrorActionPreference = 'Stop'

Write-Host ""
Write-Host "Event Relay Hub - Fix and Start" -ForegroundColor Cyan
Write-Host ""

# Remove old venv if exists
if (Test-Path ".venv") {
    Write-Host "[*] Removing old virtual environment..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force .venv
}

# Create new venv
Write-Host "[*] Creating fresh virtual environment..." -ForegroundColor Yellow
python -m venv .venv

# Activate
Write-Host "[*] Activating virtual environment..." -ForegroundColor Yellow
& ".\.venv\Scripts\Activate.ps1"

# Upgrade pip
Write-Host "[*] Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet

# Install dependencies
Write-Host "[*] Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Copy config
if (-not (Test-Path ".env")) {
    Write-Host "[*] Creating .env file..." -ForegroundColor Yellow
    Copy-Item "env.example" ".env"
}

# Create necessary directories
New-Item -ItemType Directory -Force -Path "data" | Out-Null

# Init database
Write-Host "[*] Initializing database..." -ForegroundColor Yellow
python -c "from app.models import init_db; init_db(); print('[OK] Database initialized')"

# Test import
Write-Host "[*] Testing imports..." -ForegroundColor Yellow
python -c "from app.main import app; print('[OK] All imports successful')"

Write-Host ""
Write-Host "[OK] Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Starting server on port 8202..." -ForegroundColor Green
Write-Host "Visit: http://localhost:8202" -ForegroundColor Cyan
Write-Host ""

# Start server
uvicorn app.main:app --host 0.0.0.0 --port 8202 --reload

