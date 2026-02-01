# Quick Start Guide

## Start Both Servers Together

### Option 1: PowerShell Script (Recommended)
```powershell
.\start.ps1
```

This will open two separate windows:
- Backend server (Port 8000)
- Frontend server (Port 5173)

### Option 2: Manual Start
**Terminal 1 - Backend:**
```powershell
cd backend\src
& ..\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```powershell
cd frontend
npm run dev
```

## Stop Servers

### Using Script
```powershell
.\stop.ps1
```

### Manual Stop
Press `Ctrl+C` in each terminal window

## Access Points
- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs

## Troubleshooting

### Port Already in Use
If you get port conflicts:
```powershell
# Stop all servers
.\stop.ps1

# Or manually kill processes
Get-Process -Name "python" | Where-Object {$_.CommandLine -like "*uvicorn*"} | Stop-Process -Force
Get-Process -Name "node" | Stop-Process -Force
```

### Backend Won't Start
1. Ensure virtual environment is activated
2. Check if app.db exists in `backend/src/`
3. Verify all dependencies installed: `pip install -r backend/requirements.txt`

### Frontend Won't Start
1. Ensure node_modules installed: `cd frontend && npm install`
2. Check Node.js version: `node --version` (should be 18+)
