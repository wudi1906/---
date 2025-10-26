# Event Relay Hub Start Script

$ErrorActionPreference = 'Stop'

Write-Host ""
Write-Host "Event Relay Hub - Starting..." -ForegroundColor Cyan
Write-Host ""

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python not found" -ForegroundColor Red
    exit 1
}

# Create venv
if (-not (Test-Path ".venv")) {
    Write-Host "[*] Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
}

# Activate
Write-Host "[*] Activating virtual environment..." -ForegroundColor Yellow
& ".\.venv\Scripts\Activate.ps1"

# Install dependencies
if (-not (Test-Path ".\.venv\Lib\site-packages\fastapi")) {
    Write-Host "[*] Installing dependencies..." -ForegroundColor Yellow
    python -m pip install --upgrade pip --quiet
    pip install -r requirements.txt --quiet
}

# Copy config
if (-not (Test-Path ".env")) {
    Copy-Item "env.example" ".env"
}

# Init DB
Write-Host "[*] Initializing database..." -ForegroundColor Yellow
python -c "from app.models import init_db; init_db()"
Write-Host "[OK] Database ready" -ForegroundColor Green

# Start
Write-Host ""
Write-Host "Starting server on port 8202..." -ForegroundColor Green
Write-Host "Visit: http://localhost:8202" -ForegroundColor Cyan
Write-Host ""

uvicorn app.main:app --host 0.0.0.0 --port 8202 --reload

