# Start Avatar Overlay Script
# Make sure backend is running first!

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Starting Alisa Assistant Overlay" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan

Set-Location -Path "$PSScriptRoot\overlay"

# Check if venv exists
if (-Not (Test-Path "venv")) {
    Write-Host "`n⚠️  Virtual environment not found. Creating..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
}

# Activate venv
Write-Host "`nActivating virtual environment..." -ForegroundColor Cyan
& ".\venv\Scripts\Activate.ps1"

# Check if dependencies are installed
Write-Host "Checking dependencies..." -ForegroundColor Cyan
$packages = pip list | Select-String "websockets"
if (-Not $packages) {
    Write-Host "⚠️  Dependencies not installed. Installing..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

# Start overlay
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Starting avatar overlay..." -ForegroundColor Green
Write-Host "Connecting to backend at ws://127.0.0.1:8000/ws/chat" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

python main.py
