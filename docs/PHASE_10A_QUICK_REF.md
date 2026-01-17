# 🖥️ Phase 10A Quick Reference

## One-Line Summary
**Desktop understanding that knows what you're doing and offers help when appropriate.**

---

## Start Phase 10A

```powershell
.\scripts\start_phase10a.ps1
```

---

## What It Does

| Feature | Description |
|---------|-------------|
| **App Detection** | Knows if you're in VS Code, Chrome, Terminal, etc. |
| **File Detection** | Recognizes `.py`, `.js`, `.pdf`, etc. |
| **Task Inference** | Understands if you're coding, browsing, researching |
| **Error Detection** | Spots error messages on screen |
| **Help Offers** | Suggests help when errors appear (rare, not spam) |

---

## Detected Tasks

| Task | What It Means |
|------|---------------|
| `coding_python` | Writing Python code |
| `coding_javascript` | Writing JavaScript code |
| `coding` | General programming |
| `editing_data` | Working with JSON/CSV/XML |
| `browsing` | General web browsing |
| `watching_video` | YouTube or video player |
| `browsing_code` | On GitHub or code sites |
| `researching_problem` | On StackOverflow, docs |
| `reading_document` | Viewing PDF or docs |
| `running_python` | Python in terminal |
| `using_git` | Git commands |
| `terminal_work` | General terminal use |

---

## Error Patterns Detected

- "error"
- "exception"
- "failed"
- "not found"
- "cannot"
- "unable to"
- "invalid"
- "undefined"
- "null reference"
- "syntax error"
- "traceback"
- "stack trace"

---

## Offer Logic

```
Has error? → Yes
  ↓
Last offer > 5 min ago? → Yes
  ↓
User actively working? → Yes
  ↓
✅ Offer help
```

**Cooldown**: 5 minutes between offers (no spam)

---

## Configuration Tweaks

### Change Capture Frequency
**File**: `vision/vision_client_screen.py`
```python
SCREEN_CAPTURE_INTERVAL = 10  # seconds (default)
# Lower = more frequent, higher = lighter
```

### Change Offer Cooldown
**File**: `vision/desktop_understanding.py`
```python
if time_since_last_offer < 300:  # seconds (5 min default)
```

### Add Custom Error Pattern
**File**: `vision/desktop_understanding.py`
```python
self.error_patterns = [
    r"error",
    r"exception",
    r"your_custom_pattern",  # Add here
]
```

---

## Example Scenarios

### Scenario 1: Python Error in VS Code
```
Screen: "NameError: name 'x' is not defined"

Alisa understands:
  App: code (VS Code)
  File: .py
  Task: coding_python
  Error: Yes
  
Alisa offers: "I see you have a Python error. Want me to help?"
```

### Scenario 2: Reading PDF
```
Screen: "Python Tutorial.pdf" in Adobe Reader

Alisa understands:
  App: pdf
  File: .pdf
  Task: reading_document
  Error: No
  
Alisa: (Stays quiet, stores context)
```

### Scenario 3: Git Error in Terminal
```
Terminal: "fatal: could not read Username"

Alisa understands:
  App: terminal
  Task: using_git
  Error: Yes
  
Alisa offers: "Command error? Want me to take a look?"
```

---

## Integration with Phase 9B

**Phase 9B** (Companion): Speaks spontaneously based on silence  
**Phase 10A** (Desktop): Adds desktop context to understanding

**Combined Example**:
```
User: *Coding quietly for 8 minutes, Python error appears*

Phase 9B trigger: 8 min silence → might speak
Phase 10A context: Python error detected

Result: "Hmm, you've been quiet. Having trouble with that Python error?"
```

---

## Privacy

- ✅ All local processing
- ✅ No cloud uploads
- ✅ Periodic capture (not constant)
- ✅ Text only (image discarded)
- ✅ No screenshot storage

---

## Performance

- **CPU**: ~5-10% (combined with webcam)
- **RAM**: ~100MB additional
- **Interval**: 10 seconds (configurable)
- **OCR**: Lightweight pytesseract

---

## Files

| File | Purpose |
|------|---------|
| `vision/desktop_understanding.py` | Core understanding system |
| `vision/vision_client_screen.py` | Screen client with Phase 10A |
| `backend/app/ws.py` | Handles desktop messages |
| `scripts/start_phase10a.ps1` | Startup script |

---

## Logs to Watch

```
🖥️  Context: User is writing Python code
⚠️  Error detected: NameError: name 'x' is not defined
💡 Alisa can offer: I see you have a Python error. Want me to help?
✅ Phase 10A offer sent
```

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| OCR not working | Install Tesseract OCR, add to PATH |
| Too many offers | Increase cooldown (300 → 600 seconds) |
| Not detecting errors | Add custom error patterns |
| High CPU | Increase interval (10 → 20 seconds) |
| No offers at all | Check logs, verify error detection |

---

## Philosophy

**Aware, not intrusive**
- Understands silently
- Offers help rarely
- Respects cooldown
- Brief, natural

---

## Status

✅ **Implemented and Ready**  
✅ **Compatible with Phase 9B**  
✅ **No Breaking Changes**
