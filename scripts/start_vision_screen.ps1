Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Starting Enhanced Vision System (Face + Screen)" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Green
& .\vision\venv\Scripts\Activate.ps1

# Check dependencies
Write-Host "Checking dependencies..." -ForegroundColor Green
pip show opencv-python mediapipe mss pytesseract pywin32 > $null

if ($LASTEXITCODE -ne 0) {
    Write-Host "Missing dependencies. Installing..." -ForegroundColor Yellow
    pip install -r vision\requirements.txt
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Starting enhanced vision monitoring..." -ForegroundColor Yellow
Write-Host "Connecting to backend at ws://127.0.0.1:8000/ws/chat" -ForegroundColor Yellow
Write-Host "Webcam will monitor your presence and attention" -ForegroundColor Yellow
Write-Host "Screen will be captured every 5-10 seconds" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Run the enhanced vision client
python vision/vision_client_screen.py

