# Simple Start Script for Global Price Sentinel
# No special characters, English only

$ErrorActionPreference = 'Stop'

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Global Price Sentinel" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python not found" -ForegroundColor Red
    exit 1
}

# Create venv if not exists
if (-not (Test-Path ".venv")) {
    Write-Host "[*] Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
    Write-Host "[OK] Virtual environment created" -ForegroundColor Green
}

# Activate venv
Write-Host "[*] Activating virtual environment..." -ForegroundColor Yellow
& ".\.venv\Scripts\Activate.ps1"

# Install dependencies if needed
$needInstall = $false
if (-not (Test-Path ".\.venv\Lib\site-packages\fastapi")) {
    $needInstall = $true
}

if ($needInstall) {
    Write-Host "[*] Installing dependencies (first time, please wait)..." -ForegroundColor Yellow
    python -m pip install --upgrade pip --quiet
    pip install -r requirements.txt --quiet
    Write-Host "[*] Installing Playwright browser..." -ForegroundColor Yellow
    playwright install chromium
    Write-Host "[OK] Dependencies installed" -ForegroundColor Green
}

# Copy config files
if (-not (Test-Path ".env")) {
    Write-Host "[*] Creating .env file" -ForegroundColor Yellow
    Copy-Item "env.example" ".env"
}

if (-not (Test-Path "configs")) {
    New-Item -ItemType Directory -Path "configs" | Out-Null
}

if (-not (Test-Path "configs\targets.yml")) {
    Write-Host "[*] Creating targets config" -ForegroundColor Yellow
    if (Test-Path "configs\targets.example.yml") {
        Copy-Item "configs\targets.example.yml" "configs\targets.yml"
    }
}

# Init database
Write-Host "[*] Initializing database..." -ForegroundColor Yellow
python -c "from app.models import init_db; init_db()"
Write-Host "[OK] Database ready" -ForegroundColor Green

# Generate sample report
if (-not (Test-Path "reports\latest.html")) {
    Write-Host "[*] Generating sample report..." -ForegroundColor Yellow
    python -c "from app.reporter import ReportGenerator; ReportGenerator.generate_html_report()" 2>$null
    Write-Host "[OK] Report generated" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Starting Server..." -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Main Page:  http://localhost:8101" -ForegroundColor Cyan
Write-Host "API Docs:   http://localhost:8101/api/docs" -ForegroundColor Cyan
Write-Host "Report:     http://localhost:8101/reports/latest.html" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

# Start server
uvicorn app.main:app --host 0.0.0.0 --port 8101 --reload

