# Phase 10C: Task Memory & Habits - Status Check
# Shows learning status and patterns

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  PHASE 10C: TASK MEMORY & HABITS" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check if backend is running
$backendRunning = Get-Process python -ErrorAction SilentlyContinue | Where-Object {$_.MainWindowTitle -like "*uvicorn*" -or $_.CommandLine -like "*main:app*"}

if ($backendRunning) {
    Write-Host "✅ Backend is running (Phase 10C active)" -ForegroundColor Green
} else {
    Write-Host "❌ Backend is NOT running" -ForegroundColor Red
    Write-Host "   Phase 10C requires the backend to be active." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "   Start backend with:" -ForegroundColor Yellow
    Write-Host "   .\scripts\start_backend.ps1" -ForegroundColor White
    Write-Host ""
    exit
}

Write-Host ""
Write-Host "🎯 Phase 10C Status:" -ForegroundColor Cyan
Write-Host "   • Observing user activity" -ForegroundColor White
Write-Host "   • Learning work patterns" -ForegroundColor White
Write-Host "   • Adapting behavior quietly" -ForegroundColor White
Write-Host ""

# Check for memory file
$memoryPath = "$env:USERPROFILE\Documents\Alisa Memory\task_memory.json"

if (Test-Path $memoryPath) {
    Write-Host "📁 Memory File: Found" -ForegroundColor Green
    
    # Read and parse memory file
    try {
        $memory = Get-Content $memoryPath -Raw | ConvertFrom-Json
        
        Write-Host ""
        Write-Host "📊 Learning Statistics:" -ForegroundColor Cyan
        
        # Show patterns if available
        if ($memory.patterns) {
            $patterns = $memory.patterns
            
            # Peak hours
            if ($patterns.peak_coding_hours) {
                $peakHours = $patterns.peak_coding_hours -join ", "
                Write-Host "   🕐 Peak Hours: $peakHours" -ForegroundColor Yellow
            }
            
            # Quiet hours
            if ($patterns.preferred_silence_hours) {
                $quietHours = $patterns.preferred_silence_hours -join ", "
                Write-Host "   🤫 Quiet Hours: $quietHours" -ForegroundColor Yellow
            }
            
            # App preferences
            if ($patterns.app_preferences) {
                Write-Host "   📱 App Preferences:" -ForegroundColor Yellow
                $patterns.app_preferences.PSObject.Properties | ForEach-Object {
                    Write-Host "      • $($_.Name): $($_.Value)" -ForegroundColor White
                }
            }
            
            # Total tasks
            if ($patterns.total_tasks_observed) {
                Write-Host "   📈 Tasks Observed: $($patterns.total_tasks_observed)" -ForegroundColor Yellow
            }
            
            # Sessions tracked
            if ($patterns.sessions_tracked) {
                Write-Host "   📅 Sessions Tracked: $($patterns.sessions_tracked)" -ForegroundColor Yellow
            }
        } else {
            Write-Host "   ⏳ Still gathering data..." -ForegroundColor Yellow
            Write-Host "      Use Alisa normally for a few days to build patterns." -ForegroundColor Gray
        }
        
        # Last saved
        if ($memory.last_saved) {
            $lastSaved = [DateTimeOffset]::FromUnixTimeSeconds($memory.last_saved).LocalDateTime
            Write-Host ""
            Write-Host "   💾 Last Updated: $lastSaved" -ForegroundColor Gray
        }
        
    } catch {
        Write-Host "   ⚠️  Could not read memory file" -ForegroundColor Red
    }
    
} else {
    Write-Host "📁 Memory File: Not yet created" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "   This is normal on first run!" -ForegroundColor White
    Write-Host "   Memory file will be created after your first session." -ForegroundColor Gray
    Write-Host ""
    Write-Host "   To start learning:" -ForegroundColor White
    Write-Host "   1. Use Alisa normally (chat, code, work)" -ForegroundColor Gray
    Write-Host "   2. Disconnect properly when done" -ForegroundColor Gray
    Write-Host "   3. Check back here to see learned patterns" -ForegroundColor Gray
}

Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
Write-Host ""
Write-Host "ℹ️  Phase 10C learns by watching:" -ForegroundColor Cyan
Write-Host "   • When you work (peak hours)" -ForegroundColor White
Write-Host "   • When you prefer quiet (focus times)" -ForegroundColor White
Write-Host "   • Which apps you use (preferences)" -ForegroundColor White
Write-Host "   • Your common workflows (patterns)" -ForegroundColor White
Write-Host ""
Write-Host "   Then adapts quietly:" -ForegroundColor Cyan
Write-Host "   • Less interruptions during focus" -ForegroundColor White
Write-Host "   • More relevant suggestions" -ForegroundColor White
Write-Host "   • Personalized behavior" -ForegroundColor White
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
Write-Host ""
Write-Host "🔍 View Memory File:" -ForegroundColor Cyan
Write-Host "   notepad `"$memoryPath`"" -ForegroundColor White
Write-Host ""
Write-Host "🧪 Run Tests:" -ForegroundColor Cyan
Write-Host "   python scripts\test_phase10c.py" -ForegroundColor White
Write-Host ""
Write-Host "📚 Documentation:" -ForegroundColor Cyan
Write-Host "   • PHASE_10C_SUMMARY.md - Overview" -ForegroundColor White
Write-Host "   • docs\PHASE_10C_IMPLEMENTATION.md - Technical guide" -ForegroundColor White
Write-Host "   • docs\PHASE_10C_QUICK_REF.md - API reference" -ForegroundColor White
Write-Host "   • docs\PHASE_10C_GETTING_STARTED.md - User guide" -ForegroundColor White
Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
