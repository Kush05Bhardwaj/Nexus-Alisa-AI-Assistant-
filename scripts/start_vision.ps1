# Start Vision System Script
# Monitors user presence and attention via webcam

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host "=" * 59 -ForegroundColor Cyan
Write-Host "  👁️ Starting Alisa Vision System" -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host "=" * 59 -ForegroundColor Cyan

Set-Location -Path "$PSScriptRoot\vision"

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
$packages = pip list | Select-String "opencv-python"
if (-Not $packages) {
    Write-Host "⚠️  Dependencies not installed. Installing..." -ForegroundColor Yellow
    pip install opencv-python mediapipe numpy
}

# Start vision client
Write-Host "`n" + "=" * 60 -ForegroundColor Cyan
Write-Host "👁️ Starting vision monitoring..." -ForegroundColor Green
Write-Host "📡 Connecting to backend at ws://127.0.0.1:8000/ws/chat" -ForegroundColor Yellow
Write-Host "📹 Webcam will monitor your presence and attention" -ForegroundColor Gray
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host "=" * 59 -ForegroundColor Cyan
Write-Host ""

python vision_client.py
