# Start Phase 10A - Desktop Understanding System
# This enables Alisa to understand what you're doing and offer contextual help

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host "=" * 59 -ForegroundColor Cyan
Write-Host "  🖥️  Starting Phase 10A - Desktop Understanding" -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host "=" * 59 -ForegroundColor Cyan

Set-Location -Path "$PSScriptRoot\..\vision"

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
    pip install -r requirements.txt
}

# Start Phase 10A
Write-Host "`n" + "=" * 60 -ForegroundColor Cyan
Write-Host "🖥️  Starting Desktop Understanding System..." -ForegroundColor Green
Write-Host "📡 Connecting to backend at ws://127.0.0.1:8000/ws/chat" -ForegroundColor Yellow
Write-Host "`nFeatures:" -ForegroundColor Cyan
Write-Host "  ✅ Face detection & attention tracking" -ForegroundColor Gray
Write-Host "  ✅ Screen content analysis" -ForegroundColor Gray
Write-Host "  ✅ Desktop understanding (knows what you're doing)" -ForegroundColor Gray
Write-Host "  ✅ Error detection" -ForegroundColor Gray
Write-Host "  ✅ Contextual help offers" -ForegroundColor Gray
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host "=" * 59 -ForegroundColor Cyan
Write-Host ""

python vision_client_screen.py
