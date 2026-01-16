Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  🎙️ Starting Alisa Voice Chat (Speak & Listen)" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Activating virtual environment..." -ForegroundColor Yellow

# Activate backend venv (has all required packages)
.\backend\venv\Scripts\Activate.ps1

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  🎤 Press ENTER to speak" -ForegroundColor Green
Write-Host "  🔊 Alisa will respond with voice" -ForegroundColor Green
Write-Host "  👁️ Vision system detects your presence" -ForegroundColor Green
Write-Host "  🎭 Overlay shows avatar animations" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""

# Run the optimized voice chat
python voice\voice_chat_optimized.py
