# Fix Project 2 - Event Relay Hub

$ErrorActionPreference = 'Stop'

Write-Host ""
Write-Host "Fixing Event Relay Hub..." -ForegroundColor Cyan
Write-Host ""

cd "E:\Program Files\cursorproject\作品集\event-relay-hub"

# Remove old venv
if (Test-Path ".venv") {
    Write-Host "Removing old venv..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force .venv
}

# Create new venv
Write-Host "Creating new venv..." -ForegroundColor Yellow
python -m venv .venv

# Activate
& ".\.venv\Scripts\Activate.ps1"

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet

# Install
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Create proper .env with SQLite
Write-Host "Creating .env with SQLite..." -ForegroundColor Yellow
$envContent = @"
DEBUG=False
HOST=0.0.0.0
PORT=8202
DATABASE_URL=sqlite:///./event_hub.db
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_ENABLED=True
"@

$envContent | Out-File -FilePath ".env" -Encoding ASCII -Force

# Init DB
Write-Host "Initializing database..." -ForegroundColor Yellow
python -c "from app.models import init_db; init_db()"

Write-Host ""
Write-Host "Project 2 Fixed!" -ForegroundColor Green
Write-Host ""
Write-Host "Starting server..." -ForegroundColor Cyan
Write-Host ""

uvicorn app.main:app --host 0.0.0.0 --port 8202 --reload

