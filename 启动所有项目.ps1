# Master Start Script - Launch All Projects
# One command to start everything!

$ErrorActionPreference = 'Continue'

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Developer Portfolio - Master Launcher" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Resolve Python command (prefer Python 3.11 to ensure wheel availability for dependencies like PyMuPDF)
function Get-PythonCmd {
    # Prefer Homebrew Python 3.11 on macOS Apple Silicon
    $brewPy311 = "/opt/homebrew/opt/python@3.11/bin/python3.11"
    if (Test-Path $brewPy311) { return $brewPy311 }
    
    # Fallbacks
    foreach ($cmd in @("python3.11", "python3", "python")) {
        try {
            $found = Get-Command $cmd -ErrorAction SilentlyContinue
            if ($found) { return $cmd }
        } catch {}
    }
    throw "Python is not installed or not in PATH. Please install Python 3.11 (e.g. brew install python@3.11)."
}

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
        NpmScript = "dev"
        Status = "Ready"
    },
    @{
        Name = "Doc Knowledge Forge"
        Path = "doc-knowledge-forge"
        Port = 8404
        Type = "Python"
        Status = "Ready"
    },
    @{
        Name = "A11y Component Atlas"
        Path = "a11y-component-atlas"
        Port = 8505
        Type = "Node"
        NpmScript = "storybook"
        Status = "Ready"
    },
    @{
        Name = "Insight Viz Studio"
        Path = "insight-viz-studio"
        Port = 8606
        Type = "Python"
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
        $pyCmd = Get-PythonCmd
        # If venv exists, verify interpreter version; if mismatched, recreate
        if (Test-Path ".venv") {
            if ($IsWindows) { $venvPyCheck = ".\.venv\Scripts\python.exe" } else { $venvPyCheck = "./.venv/bin/python" }
            $currentVer = try { & $venvPyCheck -c "import sys; print(f'{sys.version_info[0]}.{sys.version_info[1]}')" 2>$null } catch { '' }
            $targetVer = try { & $pyCmd -c "import sys; print(f'{sys.version_info[0]}.{sys.version_info[1]}')" 2>$null } catch { '' }
            if (-not $currentVer -or -not $targetVer -or $currentVer -ne $targetVer) {
                Write-Host "  [*] Recreating virtual environment using Python $targetVer (previous: $currentVer)" -ForegroundColor Yellow
                Remove-Item -Recurse -Force ".venv" -ErrorAction SilentlyContinue
            }
        }
        if (-not (Test-Path ".venv")) {
            Write-Host "  [*] Creating virtual environment..." -ForegroundColor Yellow
            & $pyCmd -m venv .venv
            Start-Sleep -Seconds 2
        }
        if ($IsWindows) {
            $venvPython = ".\.venv\Scripts\python.exe"
            $venvPip = ".\.venv\Scripts\pip.exe"
            $venvPlaywright = ".\.venv\Scripts\playwright.exe"
        } else {
            $venvPython = "./.venv/bin/python"
            $venvPip = "./.venv/bin/pip"
            $venvPlaywright = "./.venv/bin/playwright"
        }
        Write-Host "  [*] Installing dependencies (this may take a few minutes)..." -ForegroundColor Yellow
        & $venvPython -m pip install --upgrade pip --quiet
        if (Test-Path "requirements.txt") { & $venvPip install -r requirements.txt --quiet }
        if ($ProjectName -eq "Global Price Sentinel") {
            Write-Host "  [*] Installing Playwright browser..." -ForegroundColor Yellow
            & $venvPlaywright install chromium --quiet
        }
        if (-not (Test-Path ".env")) {
            if (Test-Path ".env.example") { Copy-Item ".env.example" ".env" }
            elseif (Test-Path "env.example") { Copy-Item "env.example" ".env" }
        }
        if (-not (Test-Path "reports")) { New-Item -ItemType Directory -Path "reports" -Force | Out-Null }
        if (-not (Test-Path "screenshots")) { New-Item -ItemType Directory -Path "screenshots" -Force | Out-Null }
        Write-Host "  [*] Initializing database..." -ForegroundColor Yellow
        $initResult = & $venvPython -c "try:`n    from app.models import init_db`n    init_db()`n    print('OK')`nexcept Exception as e:`n    print(f'ERROR: {e}')" 2>&1
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
                if ($IsWindows) { $venvPython = Join-Path $projectPath ".venv\Scripts\python.exe" } else { $venvPython = Join-Path $projectPath ".venv/bin/python" }
                if ($IsWindows) {
                    $process = Start-Process -FilePath $venvPython -ArgumentList "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", $project.Port -WorkingDirectory $projectPath -WindowStyle Hidden -PassThru
                } else {
                    $process = Start-Process -FilePath $venvPython -ArgumentList "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", $project.Port -WorkingDirectory $projectPath -PassThru
                }
            } elseif ($project.Type -eq "Node") {
                $npmScript = if ($project.NpmScript) { $project.NpmScript } else { "dev" }
                if ($IsWindows) {
                    $process = Start-Process -FilePath "npm" -ArgumentList "run", $npmScript -WorkingDirectory $projectPath -WindowStyle Hidden -PassThru
                } else {
                    $process = Start-Process -FilePath "npm" -ArgumentList "run", $npmScript -WorkingDirectory $projectPath -PassThru
                }
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
