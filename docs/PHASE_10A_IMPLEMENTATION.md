# 🖥️ Phase 10A: Desktop Understanding - Implementation Guide

## What is Phase 10A?

Phase 10A gives Alisa the ability to **understand what you're doing** on your desktop and **offer contextual help** when appropriate.

### Key Principle

**She understands, but doesn't act yet. She offers, not forces.**

---

## How It Works

### The System

1. **Screen Capture** - Grabs screenshot periodically (every 10 seconds)
2. **Window Detection** - Knows what app you're using
3. **OCR** - Reads visible text on screen
4. **Context Analysis** - Understands your current task
5. **Error Detection** - Recognizes error messages
6. **Offer System** - Suggests help when appropriate (rare, not spam)

### Decision Flow

```
Every 10 seconds:
  ↓
Capture screen
  ↓
Analyze window + text
  ↓
Understand context:
  - What app?
  - What file type?
  - What task?
  - Any errors?
  ↓
Should offer help?
  - Has error?
  - User seems stuck?
  - Haven't offered recently? (5+ min cooldown)
  ↓
Yes → Send offer to Alisa
No → Store context silently
```

---

## Features

### ✅ Application Detection

Recognizes categories:
- **Code** - VS Code, PyCharm, Sublime, etc.
- **Browser** - Chrome, Firefox, Edge
- **Document** - Word, PDF viewers
- **Terminal** - PowerShell, CMD, Git Bash
- **Communication** - Discord, Slack, Teams
- **Media** - VLC, Spotify, YouTube

### ✅ File Type Detection

Identifies:
- **Code files** - `.py`, `.js`, `.ts`, `.java`, etc.
- **Web files** - `.html`, `.css`, `.jsx`
- **Data files** - `.json`, `.xml`, `.yaml`, `.csv`
- **Documents** - `.txt`, `.md`, `.pdf`, `.docx`
- **Config files** - `.config`, `.ini`, `.env`

### ✅ Task Inference

Understands what you're doing:
- `coding_python` - Writing Python code
- `coding_javascript` - Writing JavaScript code
- `coding` - General coding
- `editing_data` - Working with data files
- `browsing` - Web browsing
- `watching_video` - Watching YouTube/videos
- `browsing_code` - Looking at GitHub
- `researching_problem` - On StackOverflow
- `reading_document` - Reading PDF/docs
- `running_python` - Terminal Python commands
- `using_git` - Git commands
- `terminal_work` - General terminal use

### ✅ Error Detection

Recognizes error patterns:
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

### ✅ Smart Offer System

Offers help when:
- ✅ Error is detected
- ✅ At least 5 minutes since last offer (no spam)
- ✅ User seems to be working on the issue
- ✅ Context is appropriate

**Doesn't spam:**
- ❌ Won't offer every time
- ❌ 5 minute cooldown between offers
- ❌ Only on fresh errors
- ❌ Respects user flow

---

## Examples

### Example 1: Python Error

```
Screen shows:
  File "main.py", line 42
    print(x)
  NameError: name 'x' is not defined

Desktop Understanding:
  - App: code (VS Code)
  - File: .py (Python)
  - Task: coding_python
  - Error: Yes - "NameError: name 'x' is not defined"
  
Alisa offers:
  "I see you have a Python error. Want me to help?"
```

### Example 2: Reading Documentation

```
Screen shows:
  Adobe Acrobat Reader - "Python Tutorial.pdf"

Desktop Understanding:
  - App: pdf
  - File: .pdf
  - Task: reading_document
  - Error: No
  
Alisa: (Stays quiet, just stores context)
```

### Example 3: Git Command Error

```
Terminal shows:
  $ git push origin master
  fatal: could not read Username

Desktop Understanding:
  - App: terminal
  - Task: using_git
  - Error: Yes - "fatal: could not read Username"
  
Alisa offers:
  "Command error? Want me to take a look?"
```

### Example 4: Researching on StackOverflow

```
Browser shows:
  stackoverflow.com - "How to fix ModuleNotFoundError"

Desktop Understanding:
  - App: browser
  - Task: researching_problem
  - Error: No (just researching)
  
Alisa: (Stores context, might offer help later if stuck)
```

---

## Configuration

### Adjust Capture Frequency

Edit `vision/vision_client_screen.py`:

```python
# More frequent (use more resources)
SCREEN_CAPTURE_INTERVAL = 5  # Every 5 seconds

# Less frequent (lighter, default)
SCREEN_CAPTURE_INTERVAL = 10  # Every 10 seconds

# Rare (very light)
SCREEN_CAPTURE_INTERVAL = 20  # Every 20 seconds
```

### Adjust Offer Cooldown

Edit `vision/desktop_understanding.py`:

```python
# More helpful (offers more often)
if time_since_last_offer < 180:  # 3 minutes (was 300)
    return {"should_offer": False, ...}

# Less intrusive (offers less often)
if time_since_last_offer < 600:  # 10 minutes (was 300)
    return {"should_offer": False, ...}
```

### Add Custom Error Patterns

Edit `vision/desktop_understanding.py`:

```python
self.error_patterns = [
    r"error",
    r"exception",
    # Add your custom patterns:
    r"warning",
    r"deprecated",
    r"crash",
    # etc.
]
```

### Add Custom Applications

```python
self.app_categories = {
    "code": ["vscode", "visual studio code", "pycharm", ...],
    # Add custom category:
    "design": ["photoshop", "figma", "canva"],
}
```

---

## Integration with Phase 9B

Phase 10A enhances Phase 9B (Companion Mode):

- **Phase 9B** - Speaks spontaneously based on silence
- **Phase 10A** - Adds desktop context to companion's understanding

### Combined Behavior

```
Scenario: User coding quietly for 8 minutes, Python error appears

Phase 9B: "Hmm, you've been quiet..."
  ↓
Phase 10A context added: "I see a Python error on screen"
  ↓
Result: "Hmm, you've been quiet. Having trouble with that Python error?"
```

---

## Privacy & Performance

### Privacy

- ✅ **All processing local** - No cloud uploads
- ✅ **Periodic only** - Not constant monitoring
- ✅ **Text only** - Screen text extracted, image discarded
- ✅ **Limited retention** - Only stores latest context
- ✅ **No screenshots saved** - Captured, analyzed, discarded

### Performance

- ✅ **10 second intervals** - Not resource-heavy
- ✅ **Smart caching** - Doesn't reprocess same screen
- ✅ **Lightweight OCR** - Uses efficient pytesseract
- ✅ **No heavy AI** - Simple pattern matching
- ✅ **~5-10% CPU** - Combined with webcam vision

---

## Files

### Created
- **`vision/desktop_understanding.py`** - Core understanding system
- **`scripts/start_phase10a.ps1`** - Startup script

### Modified
- **`vision/vision_client_screen.py`** - Enhanced with Phase 10A
- **`backend/app/ws.py`** - Handles desktop understanding messages

---

## Usage

### Start Phase 10A

```powershell
.\scripts\start_phase10a.ps1
```

### Or manually:

```powershell
cd vision
.\venv\Scripts\Activate.ps1
python vision_client_screen.py
```

### Expected Output

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

### Logs to Watch

```
🖥️  Context: User is writing Python code
⚠️  Error detected: NameError: name 'x' is not defined
💡 Alisa can offer: I see you have a Python error. Want me to help?
✅ Phase 10A offer sent: I noticed that Python error...
```

---

## Troubleshooting

### "OCR not working"
1. Install Tesseract OCR: https://github.com/tesseract-ocr/tesseract
2. Add to PATH
3. Restart terminal

### "Too many offers"
- Increase cooldown time (see Configuration above)
- Reduce error pattern sensitivity

### "Not detecting errors"
- Check if error keywords match your error type
- Add custom error patterns (see Configuration)

### "High CPU usage"
- Increase `SCREEN_CAPTURE_INTERVAL` to 15 or 20
- Reduce OCR region (edit `screen_analyze.py`)

### "Not offering help at all"
- Check logs for "Desktop understanding" messages
- Verify error is being detected
- Check if cooldown period has passed (5 min default)

---

## Philosophy

Phase 10A makes Alisa **aware** without being **intrusive**:

### ✅ Good Behavior
- Understands silently
- Stores context
- Offers help when appropriate
- Respects cooldown
- Brief, natural offers

### ❌ Bad Behavior (Prevented)
- Constant interruptions
- Spam offers
- Forced conversations
- Privacy invasion
- Heavy resource usage

---

## Future Enhancements

Potential additions:
- [ ] Summarize long PDFs on request
- [ ] Auto-open relevant documentation
- [ ] Suggest code fixes (with user permission)
- [ ] Learn user's workflow patterns
- [ ] Multi-monitor support
- [ ] Clipboard integration
- [ ] Activity timeline

---

**Phase 10A Status**: ✅ Implemented and ready
**Compatibility**: Works with Phase 9B, vision, voice, overlay
**Breaking Changes**: None - pure addition
