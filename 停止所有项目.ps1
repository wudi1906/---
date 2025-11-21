# Stop All Running Projects

Write-Host ""
Write-Host "Stopping all portfolio projects..." -ForegroundColor Yellow
Write-Host ""

# Find and kill processes on specific ports
$ports = @(8101, 8202, 8303, 8404, 8505, 8606)

foreach ($port in $ports) {
    try {
        if ($IsWindows) {
            $connections = netstat -ano | Select-String ":$port " | Select-String "LISTENING"
            $pids = @()
            foreach ($connection in $connections) {
                $parts = $connection -split '\s+' | Where-Object { $_ -ne '' }
                if ($parts.Count -gt 0) {
                    $pid = $parts[-1]
                    if ($pid -and $pid -match '^\d+$') { $pids += [int]$pid }
                }
            }
        } else {
            # lsof -t prints only PIDs
            $pids = & lsof -nP -iTCP:$port -sTCP:LISTEN -t 2>$null | ForEach-Object { $_.Trim() } | Where-Object { $_ -match '^\d+$' } | ForEach-Object { [int]$_ }
        }

        if (-not $pids -or $pids.Count -eq 0) {
            Write-Host "No listener found on port $port" -ForegroundColor DarkGray
            continue
        }

        foreach ($pid in $pids) {
            try {
                Write-Host "Stopping PID $pid on port $($port)" -ForegroundColor Yellow
                Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
                Write-Host "  [OK] Stopped" -ForegroundColor Green
            } catch {
                Write-Host "  [WARN] Could not stop process $pid" -ForegroundColor Yellow
            }
        }
    } catch {
        Write-Host "  [WARN] Failed to query port $($port): $($_.Exception.Message)" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "All services stopped." -ForegroundColor Cyan
Write-Host ""

