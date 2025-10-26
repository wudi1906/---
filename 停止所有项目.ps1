# Stop All Running Projects

Write-Host ""
Write-Host "Stopping all portfolio projects..." -ForegroundColor Yellow
Write-Host ""

# Find and kill processes on specific ports
$ports = @(8101, 8202, 8303, 8404, 8505, 8606)

foreach ($port in $ports) {
    $connections = netstat -ano | Select-String ":$port " | Select-String "LISTENING"
    
    foreach ($connection in $connections) {
        $parts = $connection -split '\s+' | Where-Object { $_ -ne '' }
        $pid = $parts[-1]
        
        if ($pid -and $pid -match '^\d+$') {
            try {
                $process = Get-Process -Id $pid -ErrorAction SilentlyContinue
                if ($process) {
                    Write-Host "Stopping process on port $port (PID: $pid)" -ForegroundColor Yellow
                    Stop-Process -Id $pid -Force
                    Write-Host "  [OK] Stopped" -ForegroundColor Green
                }
            } catch {
                Write-Host "  [WARN] Could not stop process $pid" -ForegroundColor Yellow
            }
        }
    }
}

# Kill any remaining Python/Node processes for the projects
$processNames = @("python", "node", "npm")
foreach ($name in $processNames) {
    $processes = Get-Process -Name $name -ErrorAction SilentlyContinue | 
        Where-Object { $_.Path -like "*作品集*" }
    
    foreach ($proc in $processes) {
        Write-Host "Stopping $($proc.ProcessName) (PID: $($proc.Id))" -ForegroundColor Yellow
        Stop-Process -Id $proc.Id -Force -ErrorAction SilentlyContinue
    }
}

Write-Host ""
Write-Host "All services stopped." -ForegroundColor Cyan
Write-Host ""

