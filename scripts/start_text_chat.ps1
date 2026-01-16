# Start Alisa Text Chat (Type & Listen Mode)
# Perfect for midnight coding sessions - type instead of talk!

Write-Host "Starting Alisa Text Chat (with voice output)..." -ForegroundColor Cyan

# Activate virtual environment if it exists
if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & venv\Scripts\Activate.ps1
}

# Navigate to voice directory and run text chat
Set-Location voice
python text_chat.py
