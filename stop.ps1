#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Stop all running backend and frontend servers
.DESCRIPTION
    This script stops all uvicorn (backend) and node (frontend) processes
#>

Write-Host "🛑 Stopping servers..." -ForegroundColor Yellow
Write-Host ""

# Stop backend (uvicorn processes)
Write-Host "Stopping backend servers..." -ForegroundColor Cyan
$uvicornProcesses = Get-Process -Name "python" -ErrorAction SilentlyContinue | Where-Object {
    $_.CommandLine -like "*uvicorn*app.main:app*"
}

if ($uvicornProcesses) {
    $uvicornProcesses | Stop-Process -Force
    Write-Host "✅ Stopped $($uvicornProcesses.Count) backend process(es)" -ForegroundColor Green
} else {
    Write-Host "ℹ️  No backend processes found" -ForegroundColor Gray
}

# Stop frontend (vite/node processes)
Write-Host "Stopping frontend servers..." -ForegroundColor Cyan
$nodeProcesses = Get-Process -Name "node" -ErrorAction SilentlyContinue | Where-Object {
    $_.CommandLine -like "*vite*" -or $_.CommandLine -like "*npm*run*dev*"
}

if ($nodeProcesses) {
    $nodeProcesses | Stop-Process -Force
    Write-Host "✅ Stopped $($nodeProcesses.Count) frontend process(es)" -ForegroundColor Green
} else {
    Write-Host "ℹ️  No frontend processes found" -ForegroundColor Gray
}

Write-Host ""
Write-Host "✅ All servers stopped" -ForegroundColor Green
