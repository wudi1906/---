# Complete Fix for Event Relay Hub (Project 2)

$ErrorActionPreference = 'Stop'

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Fixing Event Relay Hub (Project 2)" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

cd "E:\Program Files\cursorproject\作品集\event-relay-hub"

# Step 1: Remove old virtual environment
if (Test-Path ".venv") {
    Write-Host "[1/7] Removing old virtual environment..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force .venv
    Write-Host "      [OK] Removed" -ForegroundColor Green
} else {
    Write-Host "[1/7] No old virtual environment found" -ForegroundColor Green
}

# Step 2: Create new virtual environment
Write-Host "[2/7] Creating fresh virtual environment..." -ForegroundColor Yellow
python -m venv .venv
Write-Host "      [OK] Created" -ForegroundColor Green

# Step 3: Activate virtual environment
Write-Host "[3/7] Activating virtual environment..." -ForegroundColor Yellow
& ".\.venv\Scripts\Activate.ps1"
Write-Host "      [OK] Activated" -ForegroundColor Green

# Step 4: Upgrade pip
Write-Host "[4/7] Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet
Write-Host "      [OK] Upgraded" -ForegroundColor Green

# Step 5: Install dependencies
Write-Host "[5/7] Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet
Write-Host "      [OK] Installed" -ForegroundColor Green

# Step 6: Setup configuration
Write-Host "[6/7] Setting up configuration..." -ForegroundColor Yellow

# Force overwrite .env with SQLite config
$envContent = @"
DEBUG=False
HOST=0.0.0.0
PORT=8202
DATABASE_URL=sqlite:///./event_hub.db
GITHUB_WEBHOOK_SECRET=
STRIPE_WEBHOOK_SECRET=
CUSTOM_WEBHOOK_SECRET=
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_ENABLED=True
REDIS_URL=
FORWARD_ENABLED=False
FORWARD_URL=
FORWARD_TIMEOUT=10
RETENTION_DAYS=30
CORS_ORIGINS=["*"]
"@

$envContent | Out-File -FilePath ".env" -Encoding UTF8
Write-Host "      [OK] .env configured with SQLite" -ForegroundColor Green

# Step 7: Initialize database
Write-Host "[7/7] Initializing database..." -ForegroundColor Yellow
python -c "from app.models import init_db; init_db(); print('[OK] Database initialized')"

Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "  Project 2 Fixed Successfully!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Starting server on port 8202..." -ForegroundColor Cyan
Write-Host "Visit: http://localhost:8202" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop" -ForegroundColor Gray
Write-Host ""

# Start the server
uvicorn app.main:app --host 0.0.0.0 --port 8202 --reload

