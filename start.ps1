#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Start both backend and frontend servers together
.DESCRIPTION
    This script starts the FastAPI backend and Vite frontend development servers
    in separate PowerShell windows. Press Ctrl+C in this window to stop monitoring.
#>

Write-Host "Starting Full Stack Application..." -ForegroundColor Green
Write-Host ""

# Get the project root directory
$projectRoot = $PSScriptRoot

# Start Backend Server
Write-Host "Starting Backend Server on Port 8000..." -ForegroundColor Cyan
$backendPath = Join-Path $projectRoot "backend\src"
$venvPath = Join-Path $projectRoot ".venv\Scripts\Activate.ps1"

$backendCommand = "cd '$backendPath'; & '$venvPath'; python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

$backendJob = Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendCommand -PassThru -WindowStyle Normal

Start-Sleep -Seconds 2

# Start Frontend Server
Write-Host "Starting Frontend Server on Port 5173..." -ForegroundColor Cyan
$frontendPath = Join-Path $projectRoot "frontend"
$frontendCommand = "cd '$frontendPath'; npm run dev"

$frontendJob = Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendCommand -PassThru -WindowStyle Normal

Write-Host ""
Write-Host "Servers Started Successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Access Points:" -ForegroundColor Yellow
Write-Host "   Frontend: http://localhost:5173" -ForegroundColor White
Write-Host "   Backend:  http://localhost:8000" -ForegroundColor White
Write-Host "   API Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "To stop servers, close both PowerShell windows" -ForegroundColor Yellow
Write-Host "or press Ctrl+C in this window and run:" -ForegroundColor Yellow
Write-Host "   Stop-Process -Id $($backendJob.Id),$($frontendJob.Id)" -ForegroundColor Gray
Write-Host ""
Write-Host "Monitoring servers... (Press Ctrl+C to exit monitoring)" -ForegroundColor Gray
Write-Host ""

# Monitor processes
try {
    while ($true) {
        if ($backendJob.HasExited) {
            Write-Host "Backend server stopped unexpectedly" -ForegroundColor Red
            break
        }
        if ($frontendJob.HasExited) {
            Write-Host "Frontend server stopped unexpectedly" -ForegroundColor Red
            break
        }
        Start-Sleep -Seconds 2
    }
}
catch {
    Write-Host ""
    Write-Host "Monitoring stopped" -ForegroundColor Yellow
    Write-Host "Servers are still running in separate windows" -ForegroundColor Gray
}
