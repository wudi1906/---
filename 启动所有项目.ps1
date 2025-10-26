# Master Start Script - Launch All Projects
# One command to start everything!

$ErrorActionPreference = 'Continue'

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Developer Portfolio - Master Launcher" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Project definitions
$projects = @(
    @{
        Name = "Global Price Sentinel"
        Path = "global-price-sentinel"
        Port = 8101
        Type = "Python"
        Status = "Ready"
    },
    @{
        Name = "Event Relay Hub"
        Path = "event-relay-hub"
        Port = 8202
        Type = "Python"
        Status = "Ready"
    },
    @{
        Name = "SaaS Northstar Dashboard"
        Path = "saas-northstar-dashboard"
        Port = 8303
        Type = "Node"
        Status = "Ready"
    }
)

$startedProjects = @()

# Function to setup Python project
function Setup-PythonProject {
    param($ProjectPath, $ProjectName)
    
    $fullPath = Join-Path $PSScriptRoot $ProjectPath
    Push-Location $fullPath
    
    try {
        # Create venv if not exists
        if (-not (Test-Path ".venv")) {
            Write-Host "  [*] Creating virtual environment..." -ForegroundColor Yellow
            python -m venv .venv
            Start-Sleep -Seconds 2
        }
        
        # Activate and check if dependencies installed
        $needInstall = $false
        if (-not (Test-Path ".\.venv\Lib\site-packages\fastapi")) {
            $needInstall = $true
        }
        
        if ($needInstall) {
            Write-Host "  [*] Installing dependencies (this may take a few minutes)..." -ForegroundColor Yellow
            
            # Upgrade pip first
            & ".\.venv\Scripts\python.exe" -m pip install --upgrade pip --quiet
            
            # Install requirements
            & ".\.venv\Scripts\pip.exe" install -r requirements.txt --quiet
            
            # Install Playwright for project 1
            if ($ProjectName -eq "Global Price Sentinel") {
                Write-Host "  [*] Installing Playwright browser..." -ForegroundColor Yellow
                & ".\.venv\Scripts\playwright.exe" install chromium --quiet
            }
        }
        
        # Copy config files
        if (-not (Test-Path ".env")) {
            if (Test-Path "env.example") {
                Copy-Item "env.example" ".env"
            }
        }
        
        # Create necessary directories
        if (-not (Test-Path "reports")) {
            New-Item -ItemType Directory -Path "reports" -Force | Out-Null
        }
        if (-not (Test-Path "screenshots")) {
            New-Item -ItemType Directory -Path "screenshots" -Force | Out-Null
        }
        
        # Init database with better error handling
        Write-Host "  [*] Initializing database..." -ForegroundColor Yellow
        $initResult = & ".\.venv\Scripts\python.exe" -c "try:`n    from app.models import init_db`n    init_db()`n    print('OK')`nexcept Exception as e:`n    print(f'ERROR: {e}')" 2>&1
        
        if ($initResult -like "*OK*") {
            Write-Host "  [OK] Database initialized" -ForegroundColor Green
        } else {
            Write-Host "  [WARN] Database init had warnings (might be OK): $initResult" -ForegroundColor Yellow
        }
        
        Write-Host "  [OK] Setup complete" -ForegroundColor Green
        return $true
        
    } catch {
        Write-Host "  [ERROR] Setup failed: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    } finally {
        Pop-Location
    }
}

# Function to setup Node project
function Setup-NodeProject {
    param($ProjectPath, $ProjectName)
    
    $fullPath = Join-Path $PSScriptRoot $ProjectPath
    Push-Location $fullPath
    
    try {
        # Install dependencies if needed
        if (-not (Test-Path "node_modules")) {
            Write-Host "  [*] Installing npm dependencies (first time, please wait)..." -ForegroundColor Yellow
            npm install --loglevel=error
        }
        
        Write-Host "  [OK] Setup complete" -ForegroundColor Green
        return $true
        
    } catch {
        Write-Host "  [ERROR] Setup failed: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    } finally {
        Pop-Location
    }
}

# Setup all projects
Write-Host "Step 1: Setting up projects..." -ForegroundColor Cyan
Write-Host ""

$setupSuccess = $true
foreach ($project in $projects) {
    if ($project.Status -eq "Ready") {
        Write-Host "[$($project.Name)]" -ForegroundColor Green
        
        $success = $false
        if ($project.Type -eq "Python") {
            $success = Setup-PythonProject -ProjectPath $project.Path -ProjectName $project.Name
        } elseif ($project.Type -eq "Node") {
            $success = Setup-NodeProject -ProjectPath $project.Path -ProjectName $project.Name
        }
        
        if (-not $success) {
            Write-Host "  [WARN] Setup failed, will skip this project" -ForegroundColor Yellow
            $project.Status = "Failed"
        }
        
        Write-Host ""
    }
}

# Check if at least one project is ready
$readyProjects = $projects | Where-Object { $_.Status -eq "Ready" }
if ($readyProjects.Count -eq 0) {
    Write-Host "No projects are ready to start. Please check the errors above." -ForegroundColor Red
    exit 1
}

# Start all ready projects in background
Write-Host ""
Write-Host "Step 2: Starting services..." -ForegroundColor Cyan
Write-Host ""

foreach ($project in $projects) {
    if ($project.Status -eq "Ready") {
        Write-Host "Starting: $($project.Name) on port $($project.Port)" -ForegroundColor Yellow
        
        $projectPath = Join-Path $PSScriptRoot $project.Path
        
        try {
            # Start process in background
            if ($project.Type -eq "Python") {
                $venvPython = Join-Path $projectPath ".venv\Scripts\python.exe"
                $process = Start-Process -FilePath $venvPython `
                    -ArgumentList "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", $project.Port `
                    -WorkingDirectory $projectPath `
                    -WindowStyle Hidden `
                    -PassThru
            } elseif ($project.Type -eq "Node") {
                $process = Start-Process -FilePath "npm" `
                    -ArgumentList "run", "dev" `
                    -WorkingDirectory $projectPath `
                    -WindowStyle Hidden `
                    -PassThru
            }
            
            $startedProjects += @{
                Name = $project.Name
                Port = $project.Port
                Process = $process
                Path = $projectPath
            }
            
            Write-Host "  [OK] Started (PID: $($process.Id))" -ForegroundColor Green
            Start-Sleep -Seconds 2
            
        } catch {
            Write-Host "  [ERROR] Failed to start: $($_.Exception.Message)" -ForegroundColor Red
        }
    }
}

if ($startedProjects.Count -eq 0) {
    Write-Host ""
    Write-Host "No services were started successfully." -ForegroundColor Red
    exit 1
}

# Wait for services to be ready
Write-Host ""
Write-Host "Step 3: Waiting for services to start..." -ForegroundColor Cyan
Start-Sleep -Seconds 8

# Display summary
Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "  Services Started!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""

Write-Host "Access your projects:" -ForegroundColor Cyan
Write-Host ""

foreach ($proj in $startedProjects) {
    Write-Host "  $($proj.Name)" -ForegroundColor White
    Write-Host "    URL: http://localhost:$($proj.Port)" -ForegroundColor Yellow
    Write-Host "    PID: $($proj.Process.Id)" -ForegroundColor Gray
    Write-Host ""
}

Write-Host "Main Portal: http://localhost:8101" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop all services" -ForegroundColor Yellow
Write-Host "Or run: .\停止所有项目.ps1 in another window" -ForegroundColor Yellow
Write-Host ""

# Keep script running and monitor processes
try {
    while ($true) {
        Start-Sleep -Seconds 10
        
        # Check if any process died
        $deadProjects = @()
        foreach ($proj in $startedProjects) {
            if ($proj.Process.HasExited) {
                if ($proj.Name -notin $deadProjects) {
                    Write-Host "[WARNING] $($proj.Name) stopped unexpectedly (exit code: $($proj.Process.ExitCode))" -ForegroundColor Red
                    $deadProjects += $proj.Name
                }
            }
        }
        
        # If all processes died, exit
        $aliveCount = ($startedProjects | Where-Object { -not $_.Process.HasExited }).Count
        if ($aliveCount -eq 0) {
            Write-Host ""
            Write-Host "All services have stopped." -ForegroundColor Yellow
            break
        }
    }
} finally {
    # Cleanup on exit
    Write-Host ""
    Write-Host "Stopping all services..." -ForegroundColor Yellow
    
    foreach ($proj in $startedProjects) {
        try {
            if (-not $proj.Process.HasExited) {
                Stop-Process -Id $proj.Process.Id -Force -ErrorAction SilentlyContinue
                Write-Host "  [OK] Stopped $($proj.Name)" -ForegroundColor Green
            }
        } catch {
            # Ignore errors during cleanup
        }
    }
    
    Write-Host ""
    Write-Host "All services stopped." -ForegroundColor Cyan
}
