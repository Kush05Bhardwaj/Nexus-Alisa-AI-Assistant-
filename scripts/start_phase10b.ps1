# Start Phase 10B - Desktop Actions System
# This enables Alisa to perform desktop actions with your permission

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host "=" * 59 -ForegroundColor Cyan
Write-Host "  🎮  Starting Phase 10B - Desktop Actions" -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host "=" * 59 -ForegroundColor Cyan

Write-Host ""
Write-Host "Features:" -ForegroundColor Yellow
Write-Host "  ✅ Open/close applications" -ForegroundColor Green
Write-Host "  ✅ Browser control (tabs, navigation)" -ForegroundColor Green
Write-Host "  ✅ Keyboard/mouse automation" -ForegroundColor Green
Write-Host "  ✅ File operations (read/write)" -ForegroundColor Green
Write-Host "  ✅ Permission-based execution" -ForegroundColor Green
Write-Host "  ✅ Safety guards active" -ForegroundColor Green
Write-Host ""
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host "=" * 59 -ForegroundColor Cyan
Write-Host ""

# Check if backend is already running
$backendRunning = Get-Process -Name "python" -ErrorAction SilentlyContinue | Where-Object {
    $_.CommandLine -like "*uvicorn*"
}

if ($backendRunning) {
    Write-Host "✅ Backend is already running" -ForegroundColor Green
    Write-Host "   Phase 10B is active" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Start text chat to use desktop actions:" -ForegroundColor Yellow
    Write-Host "  .\scripts\start_text_chat.ps1" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Or start voice chat:" -ForegroundColor Yellow
    Write-Host "  .\scripts\start_voice.ps1" -ForegroundColor Cyan
    Write-Host ""
    exit
}

# Backend not running, start it
Write-Host "Starting backend with Phase 10B..." -ForegroundColor Cyan
Write-Host ""

Set-Location -Path "$PSScriptRoot\..\backend"

# Check if venv exists
if (-Not (Test-Path "venv")) {
    Write-Host "⚠️  Virtual environment not found. Creating..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
}

# Activate venv
Write-Host "Activating virtual environment..." -ForegroundColor Cyan
& ".\venv\Scripts\Activate.ps1"

# Check if dependencies are installed
Write-Host "Checking dependencies..." -ForegroundColor Cyan

$pyautoguiInstalled = pip list 2>$null | Select-String "pyautogui"
$psutilInstalled = pip list 2>$null | Select-String "psutil"

if (-Not $pyautoguiInstalled -or -Not $psutilInstalled) {
    Write-Host "⚠️  Phase 10B dependencies missing. Installing..." -ForegroundColor Yellow
    pip install pyautogui psutil
    Write-Host "✅ Dependencies installed" -ForegroundColor Green
}

# Start backend
Write-Host ""
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host "=" * 59 -ForegroundColor Cyan
Write-Host "  🎮  Phase 10B - Desktop Actions System" -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host "=" * 59 -ForegroundColor Cyan
Write-Host ""
Write-Host "✅ Backend starting with Phase 10B enabled" -ForegroundColor Green
Write-Host "🎮 Desktop actions available with permission" -ForegroundColor Cyan
Write-Host "🛡️  Safety guards active" -ForegroundColor Yellow
Write-Host ""
Write-Host "Try commands like:" -ForegroundColor Yellow
Write-Host "  'open chrome'" -ForegroundColor Cyan
Write-Host "  'new tab'" -ForegroundColor Cyan
Write-Host "  'go to google.com'" -ForegroundColor Cyan
Write-Host "  'take note: reminder'" -ForegroundColor Cyan
Write-Host ""
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host "=" * 59 -ForegroundColor Cyan
Write-Host ""

cd ..
uvicorn backend.app.main:app --reload
