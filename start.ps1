# Start both backend and frontend servers with one command
# Starts FastAPI backend and Vite frontend as background processes
# Saves process IDs to .run/ folder for clean shutdown with stop.ps1

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "       Starting SkillBridge Application                        " -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Get the project root directory
$projectRoot = $PSScriptRoot
$runDir = Join-Path $projectRoot ".run"
$backendPidFile = Join-Path $runDir "backend.pid"
$frontendPidFile = Join-Path $runDir "frontend.pid"

# Create .run directory if it doesn't exist
if (-not (Test-Path $runDir)) {
    New-Item -ItemType Directory -Path $runDir -Force | Out-Null
}

# Function to stop existing processes
function Stop-ExistingProcess {
    param([string]$pidFile, [string]$processName)
    
    if (Test-Path $pidFile) {
        $pid = Get-Content $pidFile -ErrorAction SilentlyContinue
        if ($pid) {
            $process = Get-Process -Id $pid -ErrorAction SilentlyContinue
            if ($process) {
                Write-Host "Warning: Stopping existing $processName (PID: $pid)..." -ForegroundColor Yellow
                Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
                Start-Sleep -Seconds 1
            }
        }
        Remove-Item $pidFile -Force -ErrorAction SilentlyContinue
    }
}

# Stop any existing servers
Stop-ExistingProcess -pidFile $backendPidFile -processName "backend"
Stop-ExistingProcess -pidFile $frontendPidFile -processName "frontend"

# ==================== START BACKEND ====================
Write-Host "Starting Backend Server..." -ForegroundColor Cyan

$backendSrc = Join-Path $projectRoot "backend\src"
$venvActivate = Join-Path $projectRoot "backend\.venv\Scripts\Activate.ps1"

# Check if virtual environment exists
if (-not (Test-Path $venvActivate)) {
    Write-Host "ERROR: Virtual environment not found at:" -ForegroundColor Red
    Write-Host "   $venvActivate" -ForegroundColor Red
    Write-Host "" 
    Write-Host "Please create the virtual environment first:" -ForegroundColor Yellow
    Write-Host "   cd backend" -ForegroundColor Gray
    Write-Host "   python -m venv .venv" -ForegroundColor Gray
    Write-Host "   .venv\Scripts\Activate.ps1" -ForegroundColor Gray
    Write-Host "   pip install -r requirements.txt" -ForegroundColor Gray
    exit 1
}

# Create temp script for backend
$backendScriptFile = Join-Path $runDir "start_backend.ps1"
$uvicornPath = Join-Path $projectRoot "backend\.venv\Scripts\uvicorn.exe"
@"
Set-Location '$backendSrc'
& '$venvActivate'
`$env:PYTHONPATH='$backendSrc'
& '$uvicornPath' app.main:app --reload --host 0.0.0.0 --port 8000
"@ | Out-File -FilePath $backendScriptFile -Encoding UTF8

# Start backend in background
$backendProcess = Start-Process powershell -ArgumentList "-NoProfile","-ExecutionPolicy","Bypass","-File",$backendScriptFile -PassThru -WindowStyle Hidden

# Save backend PID
$backendProcess.Id | Out-File -FilePath $backendPidFile -Encoding ASCII

Write-Host "   Backend started (PID: $($backendProcess.Id))" -ForegroundColor Green
Write-Host "   ->  http://localhost:8000" -ForegroundColor White
Write-Host "   ->  http://localhost:8000/docs (API docs)" -ForegroundColor Gray
Write-Host ""

# Wait for backend to initialize
Start-Sleep -Seconds 3

# ==================== START FRONTEND ====================
Write-Host "Starting Frontend Server..." -ForegroundColor Cyan

$frontendPath = Join-Path $projectRoot "frontend"

# Check if node_modules exists
$nodeModules = Join-Path $frontendPath "node_modules"
if (-not (Test-Path $nodeModules)) {
    Write-Host "Warning: node_modules not found. Run 'npm install' in frontend folder first." -ForegroundColor Yellow
}

# Create temp script for frontend
$frontendScriptFile = Join-Path $runDir "start_frontend.ps1"
@"
Set-Location '$frontendPath'
npm run dev
"@ | Out-File -FilePath $frontendScriptFile -Encoding UTF8

# Start frontend in background
$frontendProcess = Start-Process powershell -ArgumentList "-NoProfile","-ExecutionPolicy","Bypass","-File",$frontendScriptFile -PassThru -WindowStyle Hidden

# Save frontend PID
$frontendProcess.Id | Out-File -FilePath $frontendPidFile -Encoding ASCII

Write-Host "   Frontend started (PID: $($frontendProcess.Id))" -ForegroundColor Green
Write-Host "   ->  http://localhost:5173 (or check terminal)" -ForegroundColor White
Write-Host ""

# ==================== SUMMARY ====================
Write-Host "================================================================" -ForegroundColor Green
Write-Host "           All Servers Running Successfully                    " -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Access Points:" -ForegroundColor Yellow
Write-Host "   Frontend:  http://localhost:5173" -ForegroundColor White
Write-Host "   Backend:   http://localhost:8000" -ForegroundColor White
Write-Host "   API Docs:  http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "To stop servers, run:" -ForegroundColor Yellow
Write-Host "   .\stop.ps1" -ForegroundColor Cyan
Write-Host ""
Write-Host "Process IDs saved to:" -ForegroundColor Gray
Write-Host "   $backendPidFile" -ForegroundColor DarkGray
Write-Host "   $frontendPidFile" -ForegroundColor DarkGray
Write-Host ""
