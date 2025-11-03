# stop-all.ps1 - terminate all six portfolio projects
# Usage: powershell -ExecutionPolicy Bypass -File .\stop-all.ps1

$ErrorActionPreference = 'SilentlyContinue'

Write-Host ""
Write-Host "Stopping all portfolio services..." -ForegroundColor Yellow
Write-Host ""

$ports = @(8101, 8202, 8303, 8404, 8505, 8606)

foreach ($port in $ports) {
    Write-Host "Checking port $port..." -ForegroundColor Gray
    $connections = netstat -ano | Select-String ":$port " | Select-String "LISTENING"
    foreach ($connection in $connections) {
        $parts = $connection.ToString().Split(' ', [System.StringSplitOptions]::RemoveEmptyEntries)
        if ($parts.Count -gt 0) {
            $pid = $parts[-1]
            if ($pid -match '^\d+$') {
                $process = Get-Process -Id $pid -ErrorAction SilentlyContinue
                if ($process) {
                    Write-Host "  Stopping PID $pid on port $port" -ForegroundColor Yellow
                    Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
                }
            }
        }
    }
}

# Additional cleanup for python/node/npm processes inside the workspace
$processNames = @('python', 'node', 'npm')
foreach ($name in $processNames) {
    $matching = Get-Process -Name $name -ErrorAction SilentlyContinue | Where-Object { $_.Path -like '*cursorproject*' }
    foreach ($proc in $matching) {
        Write-Host "  Stopping $($proc.ProcessName) (PID $($proc.Id))" -ForegroundColor Yellow
        Stop-Process -Id $proc.Id -Force -ErrorAction SilentlyContinue
    }
}

Write-Host ""
Write-Host "All services stopped." -ForegroundColor Cyan
Write-Host ""
