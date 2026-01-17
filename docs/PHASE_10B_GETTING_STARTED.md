# 🎮 Phase 10B: Getting Started Guide

Welcome to **Phase 10B - Desktop Actions**! This guide will help you get started with Alisa's automation capabilities.

---

## What You'll Get

After setup, Alisa can:
- ✅ Open and close applications
- ✅ Control browser tabs and navigation
- ✅ Type text and scroll pages
- ✅ Read files and take notes
- ✅ All with your permission

---

## Prerequisites

- ✅ Backend installed and working
- ✅ Python 3.10+
- ✅ Windows OS
- ✅ Basic chat working with Alisa

---

## Step 1: Install Dependencies

Open PowerShell in the project directory:

```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install pyautogui psutil
```

**Expected output:**
```
Successfully installed pyautogui-0.9.54 psutil-5.9.6
```

---

## Step 2: Verify Installation

Test PyAutoGUI:

```powershell
python -c "import pyautogui; print('PyAutoGUI OK')"
```

Test PSUtil:

```powershell
python -c "import psutil; print('PSUtil OK')"
```

**Expected output:**
```
PyAutoGUI OK
PSUtil OK
```

---

## Step 3: Start Backend

```powershell
cd ..
.\scripts\start_backend.ps1
```

**Look for:**
```
🎮 Phase 10B - Desktop Actions System initialized
   Actions available with permission
   Safety guards active
```

---

## Step 4: Start Text Chat

In a new terminal:

```powershell
.\scripts\start_text_chat.ps1
```

---

## Step 5: Test It Out

### Test 1: Open Application

```
You: open notepad
Alisa: Opened notepad
```

**Expected:** Notepad should open

### Test 2: Confirmation Flow

```
You: Can you open Calculator?
Alisa: Want me to open Calculator for you?
You: yes
Alisa: Done!
```

**Expected:** Calculator opens after you say "yes"

### Test 3: Browser Control

First open Chrome, then:

```
You: new tab
Alisa: Opened new tab
You: go to google.com
Alisa: Navigating to https://google.com
```

**Expected:** New tab opens, then navigates to Google

### Test 4: Taking Notes

```
You: take note: test reminder for tomorrow
Alisa: Note saved to: C:\Users\...\Documents\Alisa Notes\note_20260117_143022.txt
```

**Expected:** Check Documents/Alisa Notes folder for the file

### Test 5: Reading Files

Create a test file first:

```powershell
echo "Hello from test file" > test.txt
```

Then:

```
You: read file test.txt
Alisa: Hello from test file
```

**Expected:** File content displayed

---

## Step 6: Try Combined Features

### With Voice Chat

Start voice chat:

```powershell
.\scripts\start_voice.ps1
```

Then speak:

```
[Voice] "Alisa, open Chrome"
[Voice] "Opening Chrome now"
[Chrome opens]
```

### With Desktop Understanding

If you have Phase 10A running:

```
[Working in VS Code with an error visible]

Alisa: "I see you have an error. Want me to open the docs?"
You: "yes"
[Browser opens to relevant documentation]
```

---

## Available Commands

### Apps
| Command | Action |
|---------|--------|
| "open chrome" | Opens Chrome |
| "close notepad" | Closes Notepad |
| "launch calculator" | Opens Calculator |

### Browser
| Command | Action |
|---------|--------|
| "new tab" | Opens new tab (Ctrl+T) |
| "close tab" | Closes current tab (Ctrl+W) |
| "next tab" | Switches to next tab |
| "go to [url]" | Navigates to URL |

### Actions
| Command | Action |
|---------|--------|
| "scroll down" | Scrolls page down |
| "scroll up" | Scrolls page up |
| "type [text]" | Types the text |

### Files
| Command | Action |
|---------|--------|
| "read file [path]" | Reads and shows file |
| "take note: [text]" | Saves note to Documents |

---

## Safety Features

You're protected by:

### 1. Permission System
- Direct commands execute immediately
- Requests require confirmation
- You can always say "no"

### 2. Command Blacklist
Dangerous commands are blocked:
- `shutdown`, `restart`
- `rm -rf`, `del /f`
- `format`

### 3. Path Restrictions
File writes only allowed in:
- Documents
- Desktop
- Downloads

### 4. Rate Limiting
Max 10 actions per minute

### 5. Failsafe
Move mouse to screen corner to abort any action

---

## Customization

### Add Custom App

Edit `backend/app/desktop_actions.py`:

```python
self.app_paths = {
    # Existing apps...
    "myapp": r"C:\Path\To\MyApp.exe"
}
```

Now you can:
```
You: open myapp
Alisa: Opened myapp
```

### Adjust Safety Settings

In `desktop_actions.py`:

```python
# Change rate limit
self.RATE_LIMIT = 20  # Actions per minute

# Slow down actions
pyautogui.PAUSE = 1.0  # 1 second between actions
```

### Add Custom Safe Directories

```python
safe_dirs = [
    os.path.expanduser("~\\Documents"),
    os.path.expanduser("~\\Desktop"),
    os.path.expanduser("~\\Downloads"),
    os.path.expanduser("~\\MyCustomFolder"),  # Add this
]
```

---

## Integration Examples

### Example 1: Workflow Automation

```
You: open vscode
Alisa: Opened vscode
[Wait for VS Code to open]
You: new tab
Alisa: Opened new tab
You: type print("Hello World")
Alisa: Typed 20 characters
```

### Example 2: Quick Note Taking

During conversation:

```
You: that's a great idea
Alisa: Glad you like it!
You: take note: implement the new feature tomorrow
Alisa: Note saved to: ...\note_20260117_150033.txt
```

### Example 3: Research Helper

```
You: I need to look up Python generators
Alisa: Want me to open your browser?
You: yes
Alisa: Done!
[Chrome opens]
You: go to docs.python.org
Alisa: Navigating to https://docs.python.org
```

---

## Troubleshooting

### Problem: "Failed to open chrome"

**Solution:**
1. Check if Chrome is installed
2. Verify path in `desktop_actions.py`
3. Try full path: "open C:\Program Files\Google\Chrome\Application\chrome.exe"

### Problem: "Command blocked"

**Solution:**
- This is a dangerous command
- Check what you're trying to run
- Use safer alternatives

### Problem: "Permission denied" for file write

**Solution:**
1. Check file path is in Documents/Desktop/Downloads
2. Verify folder permissions
3. Create directory manually if needed

### Problem: Actions too fast/slow

**Solution:**
Edit `pyautogui.PAUSE` in `desktop_actions.py`:
```python
pyautogui.PAUSE = 1.0  # Slower (1 second)
pyautogui.PAUSE = 0.1  # Faster (0.1 seconds)
```

### Problem: "Rate limit exceeded"

**Solution:**
- Wait 60 seconds
- Reduce number of commands
- Or increase limit in code

---

## Best Practices

### ✅ Do

- Use explicit commands for quick actions
- Confirm actions when unsure
- Read logs to see what's happening
- Test actions before relying on them
- Keep app paths updated

### ❌ Don't

- Try to bypass safety features
- Run untrusted commands
- Spam actions rapidly
- Ignore error messages
- Disable failsafe

---

## Success Checklist

You're ready when:

- [ ] PyAutoGUI and PSUtil installed
- [ ] Backend shows "Phase 10B initialized"
- [ ] Can open apps with commands
- [ ] Confirmation flow works
- [ ] Browser controls work
- [ ] Notes save correctly
- [ ] File reading works
- [ ] Understand safety features

---

## Next Steps

### Explore More

1. **Try all action types** - Test each command category
2. **Customize app paths** - Add your frequently used apps
3. **Combine with voice** - Use voice commands for actions
4. **Integrate with Phase 10A** - Enable desktop understanding
5. **Create workflows** - Chain multiple actions together

### Advanced Usage

- Set up custom macros
- Create keyboard shortcuts
- Build automated workflows
- Integrate with other tools

---

## Get Help

If stuck:

1. **Check logs** - Backend shows detailed action info
2. **Read Implementation Guide** - `docs/PHASE_10B_IMPLEMENTATION.md`
3. **Check Quick Reference** - `docs/PHASE_10B_QUICK_REF.md`
4. **Review code** - `backend/app/desktop_actions.py` has comments

---

## Privacy & Security Reminder

- ✅ All actions are local (no network/cloud)
- ✅ You control what Alisa can do
- ✅ All actions are logged
- ✅ Safety features protect you
- ✅ No privilege escalation

---

**Welcome to Phase 10B!** 🎮

Alisa can now act with your permission, making her a truly capable desktop assistant while staying safe and respectful of your control.

**Never autonomous. Always with permission. You're in control.**
