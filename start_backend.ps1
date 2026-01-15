# Start Backend Server Script
# Run this first before starting the overlay

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host "=" * 59 -ForegroundColor Cyan
Write-Host "  🚀 Starting Alisa Assistant Backend" -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host "=" * 59 -ForegroundColor Cyan

Set-Location -Path "$PSScriptRoot\backend"

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
$packages = pip list | Select-String "fastapi"
if (-Not $packages) {
    Write-Host "⚠️  Dependencies not installed. Installing..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

# Start server
Write-Host "`n" + "=" * 60 -ForegroundColor Cyan
Write-Host "🌐 Starting FastAPI server on http://127.0.0.1:8000" -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host "=" * 59 -ForegroundColor Cyan
Write-Host ""

uvicorn app.main:app --reload
