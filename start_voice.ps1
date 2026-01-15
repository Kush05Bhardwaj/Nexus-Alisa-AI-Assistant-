# Start Voice Chat Script
# Make sure backend is running first!

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host "=" * 59 -ForegroundColor Cyan
Write-Host "  🎙️ Starting Alisa Voice Chat" -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host "=" * 59 -ForegroundColor Cyan

Set-Location -Path "$PSScriptRoot\voice"

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
$packages = pip list | Select-String "edge-tts"
if (-Not $packages) {
    Write-Host "⚠️  Dependencies not installed. Installing..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

# Start voice chat
Write-Host "`n" + "=" * 60 -ForegroundColor Cyan
Write-Host "🎤 Starting voice chat..." -ForegroundColor Green
Write-Host "📡 Connecting to backend at ws://127.0.0.1:8000/ws/chat" -ForegroundColor Cyan
Write-Host "🎙️ Press ENTER to talk, Ctrl+C to quit" -ForegroundColor Yellow
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host "=" * 59 -ForegroundColor Cyan
Write-Host ""

python voice_chat.py
