# Stop backend and frontend servers cleanly
# Stops servers using saved process IDs from .run/ folder
# Cleans up PID files after stopping processes

Write-Host "================================================================" -ForegroundColor Yellow
Write-Host "       Stopping SkillBridge Application                        " -ForegroundColor Yellow
Write-Host "================================================================" -ForegroundColor Yellow
Write-Host ""

# Get the project root directory
$projectRoot = $PSScriptRoot
$runDir = Join-Path $projectRoot ".run"
$backendPidFile = Join-Path $runDir "backend.pid"
$frontendPidFile = Join-Path $runDir "frontend.pid"

$stopCount = 0

# Function to stop process by PID file
function Stop-ProcessByPid {
    param([string]$pidFile, [string]$processName, [string]$displayName)
    
    if (Test-Path $pidFile) {
        $pid = Get-Content $pidFile -ErrorAction SilentlyContinue
        if ($pid) {
            $process = Get-Process -Id $pid -ErrorAction SilentlyContinue
            if ($process) {
                Write-Host "Stopping $displayName (PID: $pid)..." -ForegroundColor Cyan
                Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
                Start-Sleep -Seconds 1
                
                # Verify it stopped
                $stillRunning = Get-Process -Id $pid -ErrorAction SilentlyContinue
                if (-not $stillRunning) {
                    Write-Host "   $displayName stopped successfully" -ForegroundColor Green
                    $script:stopCount++
                } else {
                    Write-Host "   Warning: $displayName may still be running" -ForegroundColor Yellow
                }
            } else {
                Write-Host "   Info: $displayName process not found (already stopped?)" -ForegroundColor Gray
            }
        }
        # Clean up PID file
        Remove-Item $pidFile -Force -ErrorAction SilentlyContinue
    } else {
        Write-Host "   Info: No $displayName PID file found" -ForegroundColor Gray
    }
}

# Stop backend
Stop-ProcessByPid -pidFile $backendPidFile -processName "backend" -displayName "Backend Server"

# Stop frontend
Stop-ProcessByPid -pidFile $frontendPidFile -processName "frontend" -displayName "Frontend Server"

Write-Host ""

# Summary
if ($stopCount -gt 0) {
    Write-Host "================================================================" -ForegroundColor Green
    Write-Host "       Stopped $stopCount server(s) successfully                      " -ForegroundColor Green
    Write-Host "================================================================" -ForegroundColor Green
} else {
    Write-Host "================================================================" -ForegroundColor Gray
    Write-Host "       No running servers found                                " -ForegroundColor Gray
    Write-Host "================================================================" -ForegroundColor Gray
}

Write-Host ""

# Clean up helper scripts if they exist
$startBackendScript = Join-Path $runDir "start_backend.ps1"
$startFrontendScript = Join-Path $runDir "start_frontend.ps1"
if (Test-Path $startBackendScript) {
    Remove-Item $startBackendScript -Force -ErrorAction SilentlyContinue
}
if (Test-Path $startFrontendScript) {
    Remove-Item $startFrontendScript -Force -ErrorAction SilentlyContinue
}
