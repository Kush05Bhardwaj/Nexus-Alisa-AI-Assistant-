# 🎮 Phase 10B: Desktop Actions - User Guide

**Welcome to Phase 10B!** Alisa can now perform actions on your desktop with your permission.

---

## What Can Alisa Do?

### 🚀 Launch & Control Apps
- Open Chrome, Notepad, Calculator, VS Code, etc.
- Close applications when you're done
- Switch between windows

### 🌐 Control Your Browser
- Open new tabs
- Close tabs
- Switch between tabs
- Navigate to websites

### ⌨️ Type & Interact
- Type text anywhere
- Scroll pages
- Press keyboard shortcuts

### 📁 Manage Files
- Read file contents
- Save quick notes
- All safely restricted to your Documents folder

---

## How to Use

### Quick Actions (Direct Commands)

Just tell Alisa what to do:

```
You: "open chrome"
Alisa: "Opened chrome"
```

```
You: "new tab"
Alisa: "Opened new tab"
```

```
You: "take note: meeting tomorrow at 3pm"
Alisa: "Note saved to: ...\Documents\Alisa Notes\note_20260117.txt"
```

### Natural Requests (With Confirmation)

Ask naturally, and Alisa will confirm:

```
You: "Can you open Chrome for me?"
Alisa: "Want me to open Chrome?"
You: "yes"
Alisa: "There you go, Chrome is open!"
```

```
You: "I need to check something online"
Alisa: "Should I open your browser?"
You: "sure"
Alisa: "Opening Chrome now!"
```

---

## Example Commands

### Opening Applications
- `"open chrome"`
- `"launch notepad"`
- `"start calculator"`
- `"open vscode"`

### Closing Applications
- `"close chrome"`
- `"quit notepad"`
- `"exit calculator"`

### Browser Actions
- `"new tab"`
- `"close tab"`
- `"next tab"`
- `"go to google.com"`
- `"navigate to github.com"`

### Typing & Scrolling
- `"type hello world"`
- `"scroll down"`
- `"scroll up"`

### Notes & Files
- `"take note: buy groceries tomorrow"`
- `"save note: call dentist"`
- `"read file test.txt"`

---

## Confirming or Declining

When Alisa asks for permission:

**To Confirm:**
- "yes"
- "yeah"
- "sure"
- "okay"
- "do it"

**To Decline:**
- "no"
- "nope"
- "cancel"
- "don't"

---

## Safety Features

### You're Protected ✅

1. **Always With Permission**
   - Direct commands execute immediately
   - Natural requests ask for confirmation
   - You can always say "no"

2. **Dangerous Actions Blocked**
   - Can't run shutdown/restart
   - Can't format drives
   - Can't delete system files

3. **Limited File Access**
   - Can only write to Documents/Desktop/Downloads
   - Can read any file you can read
   - Notes saved to safe location

4. **Rate Limited**
   - Max 10 actions per minute
   - Prevents accidental spam
   - Easy to adjust if needed

5. **All Actions Logged**
   - Every action is recorded
   - Transparent and traceable
   - You can see what happened

---

## Real-World Examples

### Example 1: Quick Research

```
You: "open chrome"
Alisa: "Opened chrome"
You: "new tab"
Alisa: "Opened new tab"
You: "go to stackoverflow.com"
Alisa: "Navigating to https://stackoverflow.com"
```

### Example 2: Taking Notes During Chat

```
You: "We should implement that new feature"
Alisa: "That sounds interesting!"
You: "take note: implement user profiles feature"
Alisa: "Note saved to: ...\Alisa Notes\note_20260117_143022.txt"
```

### Example 3: Working Together

```
You: "I'm stuck on this Python error"
Alisa: "Want me to open the Python docs?"
You: "yes please"
Alisa: "Opening browser to Python documentation"
[Browser opens to docs.python.org]
```

### Example 4: Quick Calculations

```
You: "I need to calculate something"
Alisa: "Should I open Calculator?"
You: "yes"
Alisa: "Calculator is open!"
```

---

## Tips & Tricks

### 💡 Combine with Voice

Use voice chat for hands-free control:

```
[Voice] "Alisa, open Chrome"
[Voice] "Opening Chrome now"
```

### 💡 Use with Desktop Understanding

If you have Phase 10A running, Alisa knows when to help:

```
[You're working in VS Code with an error]
Alisa: "I see you have a Python error. Want me to open the docs?"
You: "yes"
[Opens documentation automatically]
```

### 💡 Take Notes On-The-Go

During any conversation:

```
You: "take note: " + whatever you want to remember
```

Notes are auto-saved with timestamps.

### 💡 Browser Workflow

Chain commands for efficiency:

```
"new tab"
"go to github.com"
[wait for load]
"new tab"
"go to stackoverflow.com"
```

---

## Where Your Notes Are Saved

All notes go to:
```
C:\Users\[YourName]\Documents\Alisa Notes\
```

Filenames are automatic:
```
note_20260117_143022.txt
note_YYYYMMDD_HHMMSS.txt
```

---

## Troubleshooting

### "Failed to open chrome"

**Fix:** Check if Chrome is installed. You can add custom app paths in the code.

### "Command blocked"

**Fix:** This is a dangerous command (like shutdown). Alisa won't run it for safety.

### "Permission denied"

**Fix:** The file/folder needs different permissions, or you're trying to write outside safe directories.

### Actions too slow/fast

**Fix:** Adjustable in settings. See the implementation guide.

---

## Privacy Promise

✅ **All Local** - Nothing goes to the cloud  
✅ **Your Permission** - You control everything  
✅ **Transparent** - All actions logged  
✅ **Safe Scope** - Limited to what you allow  
✅ **No Secrets** - You can see all the code  

---

## Getting Started

### 1. Make sure backend is running

```powershell
.\scripts\start_backend.ps1
```

### 2. Start text or voice chat

```powershell
.\scripts\start_text_chat.ps1
# OR
.\scripts\start_voice.ps1
```

### 3. Try a command

```
"open notepad"
```

### 4. You're ready! 🎉

---

## Need More Help?

📖 **Full Documentation:**
- `docs/PHASE_10B_IMPLEMENTATION.md` - Complete guide
- `docs/PHASE_10B_QUICK_REF.md` - Quick reference
- `docs/PHASE_10B_GETTING_STARTED.md` - Setup guide

🧪 **Run Tests:**
```powershell
python .\scripts\test_phase10b.py
```

---

## What Makes Phase 10B Special?

### ✨ Natural & Safe
- Talk to Alisa naturally
- She asks before acting
- Safety built-in from day one

### ⚡ Fast & Efficient
- Actions execute in milliseconds
- Minimal system resources
- No lag or delays

### 🔒 Privacy-First
- Everything stays on your computer
- No cloud, no network, no tracking
- You're in complete control

### 🎯 Actually Useful
- Real productivity gains
- Time-saving automation
- Natural workflow integration

---

## Your Desktop Assistant is Ready! 🎮

Alisa can now:
- ✅ Open and close apps
- ✅ Control your browser
- ✅ Type and scroll
- ✅ Read files and take notes
- ✅ All with your permission

**Start using it now!**

```
"Alisa, open chrome"
```

---

**"Never autonomous. Always with permission. You're in control."**

---

Made with ❤️ for productivity and safety.
