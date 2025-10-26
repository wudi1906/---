# STOP ALL PROJECTS - Simple Script

Write-Host ""
Write-Host "Stopping all services..." -ForegroundColor Yellow
Write-Host ""

# Kill processes on specific ports
$ports = @(8101, 8202, 8303, 8404, 8505, 8606)

foreach ($port in $ports) {
    $connections = netstat -ano | Select-String ":$port " | Select-String "LISTENING"
    
    foreach ($conn in $connections) {
        $parts = $conn -split '\s+' | Where-Object { $_ -ne '' }
        $pid = $parts[-1]
        
        if ($pid -and $pid -match '^\d+$') {
            try {
                Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
                Write-Host "Stopped process on port $port" -ForegroundColor Green
            } catch {
                # Ignore errors
            }
        }
    }
}

Write-Host ""
Write-Host "All services stopped." -ForegroundColor Cyan
Write-Host ""

