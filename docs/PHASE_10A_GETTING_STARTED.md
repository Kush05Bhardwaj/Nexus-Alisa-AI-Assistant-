# 🖥️ Phase 10A: Getting Started Guide

## What You'll Get

After completing this guide:
- ✅ Alisa will understand what you're doing on your desktop
- ✅ She'll detect when you have errors
- ✅ She'll offer help appropriately (rare, not spam)
- ✅ Everything runs locally, privately

**Time needed**: 5-10 minutes

---

## Prerequisites

Before starting, you should have:

### Required
- ✅ Backend running (`.\scripts\start_backend.ps1`)
- ✅ Python 3.8+ installed
- ✅ Tesseract OCR installed ([Download](https://github.com/tesseract-ocr/tesseract))

### Optional (Enhances Experience)
- Phase 9B (Companion Mode) - works great together
- Webcam vision - combines attention with desktop context
- Voice chat - for verbal help offers

---

## Step 1: Install Tesseract OCR

### Windows

1. **Download Tesseract**:
   - Go to: https://github.com/UB-Mannheim/tesseract/wiki
   - Download Windows installer (tesseract-ocr-w64-setup-v5.x.x.exe)

2. **Install**:
   - Run installer
   - Default path: `C:\Program Files\Tesseract-OCR`
   - **IMPORTANT**: Check "Add to PATH" during installation

3. **Verify**:
   ```powershell
   tesseract --version
   # Should show: tesseract v5.x.x
   ```

If not in PATH, add manually:
```powershell
$env:Path += ";C:\Program Files\Tesseract-OCR"
```

---

## Step 2: Install Python Dependencies

### Option A: Use the Startup Script (Easiest)

The script checks and installs dependencies automatically:
```powershell
.\scripts\start_phase10a.ps1
```

### Option B: Manual Installation

```powershell
cd vision
.\venv\Scripts\Activate.ps1

# Install required packages
pip install pytesseract pillow mss opencv-python websockets
```

---

## Step 3: Start the Backend

In a **separate terminal**:

```powershell
.\scripts\start_backend.ps1
```

Wait for:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
✅ Backend ready
```

---

## Step 4: Start Phase 10A

In your **main terminal**:

```powershell
.\scripts\start_phase10a.ps1
```

You should see:
```
============================================================
👁️ Phase 10A - Desktop Understanding System
============================================================
Features:
  ✅ Face detection & attention tracking
  ✅ Screen content analysis
  ✅ Desktop understanding (knows what you're doing)
  ✅ Error detection
  ✅ Contextual help offers
============================================================

✅ Phase 10A - Desktop Understanding System started
📸 Screen will be analyzed every 10 seconds
🧠 Alisa will understand what you're doing and offer help when appropriate
✅ Connected to backend at ws://127.0.0.1:8000/ws/chat
```

---

## Step 5: Test It Out

### Test 1: Basic Understanding

1. Open **VS Code** with a Python file
2. Wait 10-20 seconds
3. Check terminal logs:
   ```
   🖥️  Context: User is writing Python code
   ```

### Test 2: Error Detection

1. Create a Python error in VS Code:
   ```python
   print(undefined_variable)
   ```
2. Run it to show error
3. Wait 10 seconds
4. Check logs:
   ```
   ⚠️  Error detected: NameError: name 'undefined_variable' is not defined
   💡 Alisa can offer: I see you have a Python error. Want me to help?
   ```

5. Alisa should offer help (if cooldown passed)

### Test 3: Browsing Detection

1. Open browser to **StackOverflow**
2. Wait 10 seconds
3. Check logs:
   ```
   🖥️  Context: User is researching a problem
   ```

---

## Step 6: Configure (Optional)

### Make It More Frequent

Edit `vision/vision_client_screen.py`:
```python
SCREEN_CAPTURE_INTERVAL = 5  # Was 10, now every 5 seconds
```

### Make Offers More Rare

Edit `vision/desktop_understanding.py`:
```python
if time_since_last_offer < 600:  # Was 300 (5 min), now 10 min
    return {"should_offer": False, ...}
```

### Add Custom Error Pattern

Edit `vision/desktop_understanding.py`:
```python
self.error_patterns = [
    r"error",
    r"exception",
    r"your_custom_keyword",  # Add here
]
```

---

## Integration with Other Features

### With Phase 9B (Companion Mode)

Start both:
```powershell
# Terminal 1: Backend
.\scripts\start_backend.ps1

# Terminal 2: Webcam + Companion (Phase 9B)
.\scripts\start_vision.ps1

# Terminal 3: Desktop Understanding (Phase 10A)
.\scripts\start_phase10a.ps1
```

**Result**: Alisa understands both:
- Your face/attention (webcam)
- Your desktop activity (screen)
- She can speak spontaneously with full context

### With Voice Chat

```powershell
# Terminal 1: Backend
.\scripts\start_backend.ps1

# Terminal 2: Desktop Understanding
.\scripts\start_phase10a.ps1

# Terminal 3: Voice Chat
.\scripts\start_voice_chat.ps1
```

**Result**: Alisa can verbally offer help when errors detected

### With Overlay

```powershell
# Terminal 1: Backend
.\scripts\start_backend.ps1

# Terminal 2: Desktop Understanding
.\scripts\start_phase10a.ps1

# Terminal 3: Overlay
.\scripts\start_overlay.ps1
```

**Result**: Visual avatar + desktop understanding

---

## What You'll Notice

### Immediate
- Logs showing desktop context every 10 seconds
- App, file type, task detection

### After a Few Minutes
- Error detection when coding
- Appropriate help offers (rare)
- Context-aware understanding

### Over Time
- Natural, non-intrusive behavior
- Helpful when stuck
- Quiet when not needed

---

## Expected Behavior

### ✅ Good Signs

- **Quiet understanding**: Most captures just store context silently
- **Rare offers**: Only when errors + cooldown passed
- **Accurate detection**: Correctly identifies apps, files, tasks
- **Low resource use**: ~5-10% CPU, ~100MB RAM

### ⚠️ Needs Adjustment

- **Too many offers**: Increase cooldown time
- **No offers at all**: Check Tesseract installation, verify errors detected
- **Wrong app detection**: Add custom app patterns
- **High CPU**: Increase capture interval

---

## Troubleshooting

### Issue: "Tesseract not found"

**Solution**:
1. Install Tesseract OCR
2. Add to PATH:
   ```powershell
   $env:Path += ";C:\Program Files\Tesseract-OCR"
   ```
3. Restart terminal
4. Verify: `tesseract --version`

### Issue: "No desktop understanding logs"

**Solution**:
1. Check backend is running
2. Verify WebSocket connection in logs
3. Wait 10-20 seconds for first capture

### Issue: "Errors not detected"

**Solution**:
1. Check if error keywords match (`error`, `exception`, etc.)
2. Add custom patterns if needed
3. Verify error is visible on screen

### Issue: "Too frequent captures slowing system"

**Solution**:
1. Increase `SCREEN_CAPTURE_INTERVAL` to 15 or 20
2. Reduce OCR region in `screen_analyze.py`

---

## Privacy Notes

Phase 10A is **completely private**:

- ✅ All processing happens locally on your machine
- ✅ No screenshots sent to cloud
- ✅ No data uploaded anywhere
- ✅ Text extracted from screen, image discarded immediately
- ✅ Only stores latest context (not history)
- ✅ Periodic capture, not constant monitoring

---

## Performance Notes

### Light System (Default)
- Capture every 10 seconds
- ~5-10% CPU
- ~100MB RAM
- Minimal impact

### Very Light
- Capture every 20 seconds
- ~3-5% CPU
- ~80MB RAM

### More Responsive
- Capture every 5 seconds
- ~10-15% CPU
- ~120MB RAM

**Recommendation**: Start with default (10 sec), adjust based on your system

---

## Next Steps

### Immediate
1. ✅ Test basic understanding
2. ✅ Trigger an error and see offer
3. ✅ Verify different apps detected

### Short Term
1. Fine-tune capture interval for your needs
2. Customize error patterns for your workflow
3. Add custom app categories if needed

### Long Term
1. Combine with Phase 9B for full companion experience
2. Enable voice chat for verbal help
3. Monitor and adjust based on actual usage

---

## Common Questions

### "Will she interrupt me all the time?"

**No.** Phase 10A has a 5-minute cooldown between offers. Most captures just store context silently.

### "Can I disable help offers but keep understanding?"

**Yes.** In `vision/desktop_understanding.py`, set:
```python
return {"should_offer": False, ...}  # Never offer
```

### "Does this work with multiple monitors?"

Currently captures primary monitor only. Multi-monitor support is a future enhancement.

### "How much battery does this use?"

About 5-10% extra CPU. On battery, consider increasing interval to 15-20 seconds.

---

## Success Checklist

You're ready when:

- [ ] Backend running
- [ ] Tesseract installed and in PATH
- [ ] Phase 10A script starts without errors
- [ ] Desktop context appears in logs
- [ ] Error detection works
- [ ] Help offer triggered (after cooldown)
- [ ] Comfortable with configuration options

---

## Get Help

If stuck:

1. **Check logs** - Look for error messages
2. **Read Implementation Guide** - `docs/PHASE_10A_IMPLEMENTATION.md`
3. **Check Quick Reference** - `docs/PHASE_10A_QUICK_REF.md`
4. **Review code** - `vision/desktop_understanding.py` has detailed comments

---

**Welcome to Phase 10A!** 🖥️

Alisa now understands your desktop context and can offer help when appropriate, all while staying quiet and respectful of your workflow.
