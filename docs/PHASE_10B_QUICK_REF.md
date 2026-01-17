# 🎮 Phase 10B Quick Reference

## One-Line Summary
**Desktop automation with permission - Alisa can act when you want her to.**

---

## What It Does

| Feature | Example |
|---------|---------|
| **Open Apps** | "open chrome" → Chrome opens |
| **Close Apps** | "close notepad" → Notepad closes |
| **Browser Tabs** | "new tab" → Opens new tab |
| **Navigate** | "go to google.com" → Navigates |
| **Type Text** | "type hello" → Types text |
| **Scroll** | "scroll down" → Scrolls page |
| **Read Files** | "read file test.txt" → Shows content |
| **Take Notes** | "take note: reminder" → Saves note |

---

## Quick Commands

### Apps
```
"open chrome"
"close notepad"
"launch calculator"
"quit vscode"
```

### Browser
```
"new tab"
"close tab"
"next tab"
"go to github.com"
```

### Actions
```
"scroll down"
"scroll up"
"type hello world"
```

### Files
```
"read file config.json"
"take note: important reminder"
```

---

## Two Modes

### Direct Commands (Execute Immediately)
```
User: "open chrome"
Alisa: "Opened chrome"
```

### Confirmation Flow (Ask Permission)
```
User: "Can you open Chrome?"
Alisa: "Want me to open Chrome?"
User: "yes"
Alisa: "Done!"
```

---

## Confirmation Responses

### To Confirm
```
"yes"
"yeah"
"sure"
"okay"
"do it"
```

### To Decline
```
"no"
"nope"
"cancel"
"don't"
```

---

## Common Apps

Pre-configured:
- chrome
- firefox
- edge
- notepad
- calculator
- vscode
- explorer
- cmd
- powershell

---

## Safety Features

| Feature | Protection |
|---------|------------|
| **Blacklist** | Blocks rm -rf, shutdown, format |
| **Path Restrictions** | Files only to Documents/Desktop/Downloads |
| **Rate Limit** | Max 10 actions/minute |
| **Logging** | All actions tracked |
| **Failsafe** | Move mouse to corner to abort |

---

## File Operations

### Reading Files
- Any file you can read
- Max 50 lines shown
- 1MB file size limit

### Writing Notes
- Saved to: `Documents\Alisa Notes\`
- Filename: `note_YYYYMMDD_HHMMSS.txt`
- Auto-creates directory

---

## Examples

### Example 1: Quick Launch
```
User: "open notepad"
Alisa: "Opened notepad"
```

### Example 2: Browser Work
```
User: "new tab"
Alisa: "Opened new tab"
User: "go to stackoverflow.com"
Alisa: "Navigating to https://stackoverflow.com"
```

### Example 3: Taking Notes
```
User: "take note: call dentist tomorrow"
Alisa: "Note saved to: ...\note_20260117_143022.txt"
```

### Example 4: File Reading
```
User: "read file todo.txt"
Alisa: "Here's what I found:
       1. Finish project
       2. Buy groceries"
```

---

## Integration with Other Features

### With Phase 9B (Companion)
```
[User silent, appears stuck]
Alisa: "Need any help?"
User: "yeah, open Chrome"
Alisa: "Done!"
```

### With Phase 10A (Desktop Understanding)
```
[Alisa detects error on screen]
Alisa: "I see a Python error. Want me to open the docs?"
User: "yes"
[Opens browser to Python docs]
```

### With Voice Chat
```
[Voice] User: "Alisa, open Chrome"
[Voice] Alisa: "Opening Chrome now"
[Chrome opens]
```

---

## Configuration

No configuration needed!

Optional customization in `backend/app/desktop_actions.py`:

```python
# Add custom app
self.app_paths["myapp"] = r"C:\Path\To\App.exe"

# Adjust rate limit
self.RATE_LIMIT = 20  # Actions per minute

# Change PyAutoGUI speed
pyautogui.PAUSE = 1.0  # Slower
```

---

## Logs

Watch for these in backend logs:

```
🎯 Phase 10B: Detected open app command - chrome
⚡ Phase 10B: Direct command, executing immediately
✅ Phase 10B: Action executed successfully
```

```
❓ Phase 10B: Asking for confirmation via LLM
✅ Phase 10B: User confirmed action
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| App won't open | Check app path in code |
| "Command blocked" | Dangerous command detected |
| "Permission denied" | Check file permissions |
| "Rate limit exceeded" | Wait 1 minute |

---

## Privacy

- ✅ All local (no network/cloud)
- ✅ User consent required
- ✅ Actions logged
- ✅ Limited scope
- ✅ No privilege escalation

---

## Performance

- **CPU**: <1% idle, ~5% during action
- **RAM**: ~10MB
- **Latency**: 50-500ms per action

---

## Status

**Phase 10B**: ✅ Active and ready  
**Start**: Automatic with backend  
**Dependencies**: pyautogui, psutil  
**Compatibility**: All features  

---

**Permission-based. Safety-first. Always in control.**
