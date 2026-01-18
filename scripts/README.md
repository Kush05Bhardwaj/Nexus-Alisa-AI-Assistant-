# 🚀 Alisa Scripts

PowerShell startup scripts and Python utilities for the Alisa AI Assistant project.

**Last Updated:** January 17, 2026
**Total Scripts:** 15 (10 PowerShell + 5 Python)

---

## 📋 Overview

This folder contains all startup scripts and testing utilities for Alisa. Each script is designed to be self-contained and production-ready.

### Script Capabilities

**Automated Setup:**
- Virtual environment detection and creation
- Dependency installation with version checking
- Path resolution and navigation
- Process management and error handling
- Component lifecycle management

**Smart Features:**
- Auto-reconnection for network components
- Graceful shutdown handling
- Real-time status reporting
- Cross-script coordination
- Resource cleanup

---

## 📁 Script Directory Structure

```
scripts/
├── PowerShell Startup Scripts (.ps1)
│   ├── start_backend.ps1           # Core backend server
│   ├── start_overlay.ps1           # Avatar animation window
│   ├── start_text_chat.ps1         # Text interface
│   ├── start_voice.ps1             # Voice interface (alias)
│   ├── start_voice_chat.ps1        # Voice interface (main)
│   ├── start_vision.ps1            # Webcam presence detection
│   ├── start_vision_screen.ps1     # Screen + webcam analysis
│   ├── start_phase10a.ps1          # Desktop understanding
│   ├── start_phase10b.ps1          # Desktop actions
│   └── start_phase10c.ps1          # Task memory & habits
│
├── Python Testing & Utilities (.py)
│   ├── test_idle_system.py         # Idle thought tests
│   ├── test_phase10b.py            # Desktop actions tests
│   ├── test_phase10c.py            # Task memory tests
│   └── view_history.py             # Database viewer
│
└── README.md                        # This file
```

---

## 🎮 PowerShell Startup Scripts

### 🔧 Core System

#### `start_backend.ps1`
**Purpose:** Launch the FastAPI backend server (required for all features)

**What it does:**
```powershell
1. Navigate to backend/ directory
2. Check for virtual environment (venv/)
3. Create venv if missing: python -m venv venv
4. Activate venv: .\venv\Scripts\Activate.ps1
5. Install dependencies: pip install -r requirements.txt
6. Start server: uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

**Usage:**
```powershell
.\scripts\start_backend.ps1
```

**Output:**
- Server URL: `http://127.0.0.1:8000`
- WebSocket: `ws://127.0.0.1:8000/ws/chat`
- Health check: `GET http://127.0.0.1:8000/`
- Auto-reload on code changes

**When to use:** Always start this FIRST before any other component

**Dependencies:**
- Python 3.10+
- FastAPI, uvicorn, websockets
- SQLAlchemy, httpx

**Troubleshooting:**
- Port already in use → Kill existing process: `netstat -ano | findstr :8000`
- Import errors → Reinstall dependencies: `pip install -r requirements.txt`
- venv issues → Delete venv/ and let script recreate it

---

### 🎭 Interface Scripts

#### `start_overlay.ps1`
**Purpose:** Launch the animated avatar overlay window

**What it does:**
```powershell
1. Navigate to overlay/ directory
2. Start: python main.py
3. Create transparent window (800x800)
4. Load emotion assets
5. Connect to backend WebSocket
6. Begin animation loops (blinking, talking)
```

**Usage:**
```powershell
.\scripts\start_overlay.ps1
```

**Features:**
- 6 emotion expressions (happy, teasing, serious, calm, sad, neutral)
- Automatic blinking (every 3 seconds)
- Mouth animation during speech
- Draggable window (click and drag)
- Always-on-top display
- Thread-safe WebSocket handling

**Requirements:**
- Backend must be running
- Tkinter (included with Python)
- Pillow for image processing

**Customization:**
- Edit `overlay/assets/*.png` for custom avatar
- Modify `overlay/avatar_window.py` for animation timing

#### `start_text_chat.ps1`
**Purpose:** Text-based chat interface with voice output

**What it does:**
```powershell
1. Navigate to voice/ directory
2. Start: python text_chat.py
3. Connect to backend WebSocket
4. Enter message loop
```

**Usage:**
```powershell
.\scripts\start_text_chat.ps1
```

**Interaction:**
```
You: Hello Alisa!
[Alisa speaks and types response]
Alisa (😏): Hey there! What's up? *smirks*

You: How are you?
[Alisa speaks]
Alisa (😌): I'm doing great, thanks for asking~
```

**Features:**
- Type messages in terminal
- Receive voice responses via Edge TTS
- See emotion indicators (😊😌😏😐😢)
- Automatic speech timing
- Text cleaning (removes emotion tags)
- Overlay synchronization

**Configuration:**
- Voice: Edit `voice/voice_config.py`
- Speech rate: `SPEECH_RATE = "+15%"`
- Pitch: `PITCH_SHIFT = "+10Hz"`

**Best for:** 
- Quick conversations
- Development and testing
- When you don't have a microphone

#### `start_voice.ps1` / `start_voice_chat.ps1`
**Purpose:** Full voice conversation mode (hands-free)

**What it does:**
```powershell
1. Navigate to voice/ directory
2. Start: python voice_chat_optimized.py
3. Initialize Faster Whisper STT
4. Connect to backend WebSocket
5. Enter press-to-talk loop
```

**Usage:**
```powershell
.\scripts\start_voice.ps1
# or
.\scripts\start_voice_chat.ps1
```

**Interaction:**
```
Press ENTER to start recording, ENTER again to send (or 'q' to quit):
[Press Enter]
🎤 Recording... (Press Enter to stop)
[Speak your message]
[Press Enter]
🔄 Transcribing...
You said: "Tell me a joke"

Alisa (😏): Alright, here's one for you...
[Hears voice response]
```

**Features:**
- Press-to-talk recording (Enter key)
- Faster Whisper speech recognition
- Voice output via Edge TTS
- Continuous conversation
- Clean console output (no token spam)
- Automatic speech timing
- Emotion emoji display

**Requirements:**
- Microphone access
- Faster Whisper model (~300MB)
- sounddevice, soundfile
- Edge TTS

**Configuration:**
- STT model: Edit `voice/voice_input.py` → `model = WhisperModel("small")`
- Recording duration: `DURATION = 5` seconds
- Voice settings: `voice/voice_config.py`

**Best for:**
- Natural conversation
- Hands-free interaction
- Accessibility
- Immersive experience

---

### 👁️ Vision Scripts

#### `start_vision.ps1`
**Purpose:** Webcam-based presence detection (lightweight)

**What it does:**
```powershell
1. Navigate to vision/ directory
2. Start: python vision_client.py
3. Initialize webcam (OpenCV)
4. Load face detection models
5. Connect to backend WebSocket
6. Begin detection loop (1.5s interval)
```

**Usage:**
```powershell
.\scripts\start_vision.ps1
```

**Detection Capabilities:**
- **Face presence:** present/absent
- **Attention tracking:** focused/distracted
- **Emotion estimation:** happy/sad/neutral
- **Gaze direction:** looking at screen / away

**Performance:**
- CPU usage: ~5-10% (Balanced preset)
- Detection interval: 1.5 seconds
- Frame skip: Every 2nd frame
- Cache enabled: 0.5s TTL

**Messages Sent:**
```
[VISION_FACE]present    # Face detected
[VISION_FACE]absent     # No face
[VISION_FACE]focused    # Looking at screen
[VISION_FACE]distracted # Looking away
```

**Configuration:**
- Preset: Edit `vision/vision_config.py` → `apply_preset("balanced")`
- Presets: `ultra_light`, `balanced`, `enhanced`
- MediaPipe: Set `USE_MEDIAPIPE = True` for better accuracy

**Troubleshooting:**
- No webcam found → Check device manager, try different camera index
- High CPU usage → Switch to `ultra_light` preset
- False detections → Use `enhanced` preset with MediaPipe

**Best for:**
- Idle detection
- Presence-aware responses
- Attention tracking
- Low resource usage

#### `start_vision_screen.ps1`
**Purpose:** Full vision with desktop understanding (Phase 10A)

**What it does:**
```powershell
1. Navigate to vision/ directory
2. Start: python vision_client_screen.py
3. Initialize webcam + screen capture
4. Load OCR (Tesseract)
5. Connect to backend WebSocket
6. Begin dual analysis loop:
   - Webcam: Continuous (1.5s)
   - Screen: Periodic (10s)
```

**Usage:**
```powershell
.\scripts\start_vision_screen.ps1
```

**Detection Capabilities:**
- **All from start_vision.ps1**, PLUS:
- **Application detection** (VS Code, Chrome, Terminal, etc.)
- **File type recognition** (.py, .js, .html, .md, etc.)
- **Task inference** (coding, browsing, debugging, writing, etc.)
- **Error detection** (SyntaxError, ModuleNotFoundError, build failures, etc.)
- **Window title tracking**
- **Screen text extraction** (OCR)

**Messages Sent:**
```
[VISION_FACE]present
[VISION_DESKTOP]task|app|file_type|has_error|offer|window_title|text_sample
```

**Example Message:**
```
[VISION_DESKTOP]coding_python|vscode|.py|True|fix_error|main.py - Visual Studio Code|SyntaxError: invalid syntax
```

**Features:**
- Screen capture every 10 seconds
- Smart help offers (5-minute cooldown)
- Context-aware suggestions
- Error pattern matching (12+ patterns)
- 8 app categories
- 12 task types

**Performance:**
- CPU usage: ~15-20%
- Screen capture: ~50-100ms
- OCR processing: ~200-500ms
- Total overhead: <1s per 10s

**Troubleshooting:**
- Tesseract not found → Install: `choco install tesseract`
- OCR slow → Reduce screen resolution or increase interval
- High CPU → Disable screen capture, use vision.py only

**Best for:**
- Context-aware assistance
- Error detection and help
- Desktop automation
- Phase 10A features

---

### 🚀 Phase 10 Feature Scripts

#### `start_phase10a.ps1`
**Purpose:** Launch all components with Desktop Understanding (Phase 10A)

**What it does:**
```powershell
1. Start backend (Terminal 1)
2. Start overlay (Terminal 2)
3. Start vision_screen (Terminal 3)
4. Start text_chat (Terminal 4)
```

**Usage:**
```powershell
.\scripts\start_phase10a.ps1
```

**Phase 10A Features Enabled:**

**1. Application Detection (8 categories)**
- Code editors: VS Code, PyCharm, IntelliJ, etc.
- Browsers: Chrome, Firefox, Edge, etc.
- Terminals: PowerShell, CMD, WSL, etc.
- Document editors: Word, Notepad, etc.
- PDF viewers: Acrobat, Foxit, etc.
- Media players: VLC, Spotify, etc.
- Communication: Discord, Slack, Teams, etc.
- Other: Unrecognized applications

**2. File Type Recognition (20+ extensions)**
- Code: .py, .js, .ts, .java, .cpp, .cs, .go, .rs, etc.
- Web: .html, .css, .scss, .jsx, .tsx, .vue, etc.
- Data: .json, .xml, .yaml, .csv, .sql, etc.
- Documents: .md, .txt, .doc, .pdf, etc.
- Config: .env, .ini, .conf, .toml, etc.

**3. Task Inference (12 types)**
- `coding_python` - Working with Python files
- `coding_javascript` - JavaScript/TypeScript development
- `coding_web` - HTML/CSS/frontend work
- `coding_other` - Other programming languages
- `debugging` - Debugging (error detected)
- `browsing` - Web browsing
- `reading_docs` - Reading documentation/PDFs
- `writing` - Document editing
- `terminal_work` - Command-line tasks
- `communication` - Messaging/email
- `media` - Video/audio playback
- `unknown` - Unrecognized activity

**4. Error Detection (12+ patterns)**
```
SyntaxError, IndentationError, ModuleNotFoundError, AttributeError
NameError, TypeError, ValueError, ImportError, KeyError, IndexError
FileNotFoundError, PermissionError, RuntimeError, ConnectionError
Build failed, Compilation error, Test failed, npm ERR!, error:
```

**5. Smart Help Offers**
- Cooldown period: 5 minutes
- Triggers: Error detected + appropriate task
- Context-aware suggestions
- Non-intrusive (waits for natural pauses)

**Example Interaction:**
```
[You're coding in VS Code]
[SyntaxError appears on screen]

Alisa (😌): I noticed you're working on main.py and there might be a 
syntax error... would you like me to take a look? I can help debug it~
```

**Configuration:**
- Cooldown: `desktop_understanding.py` → `MIN_OFFER_INTERVAL = 300`
- Detection patterns: `desktop_understanding.py` → `error_patterns`

**Best for:**
- Contextual assistance
- Error detection
- Smart help timing
- Desktop awareness

#### `start_phase10b.ps1`
**Purpose:** Launch with Desktop Actions enabled (Phase 10B)

**What it does:**
```powershell
# Same as Phase 10A, PLUS enables desktop automation
```

**Usage:**
```powershell
.\scripts\start_phase10b.ps1
```

**Phase 10B Features Enabled:**

**1. Application Management**
```python
"open chrome"           # Launch Google Chrome
"open vscode"           # Launch VS Code
"open notepad"          # Launch Notepad
"close firefox"         # Close Firefox
"switch to terminal"    # Focus Terminal window
```

**Supported Apps:**
- Browsers: chrome, firefox, edge
- Editors: vscode, notepad, notepad++, sublime
- Office: word, excel, powerpoint
- Communication: discord, slack, teams
- Media: spotify, vlc
- Utilities: calculator, explorer

**2. Browser Control**
```python
"open tab google.com"   # Open new tab
"open tab youtube.com"  # Navigate to URL
"close tab"             # Close current tab
"new tab"               # Blank new tab
```

**3. Keyboard & Mouse Automation**
```python
"type Hello World"      # Type text
"press enter"           # Press key
"click 500 300"         # Click coordinates
"scroll down"           # Scroll down
"scroll up 5"           # Scroll up 5 units
```

**Supported Keys:**
- enter, tab, space, backspace, delete
- up, down, left, right
- ctrl, alt, shift, win
- f1-f12, escape, home, end, pageup, pagedown

**4. File Operations**
```python
"read file C:\path\to\file.txt"          # Read file content
"write note Remember to commit changes"  # Save note
```

**5. Window Management**
```python
"minimize window"       # Minimize active window
"maximize window"       # Maximize active window
"close window"          # Close active window
```

**6. Safe Command Execution**
```python
"run command dir"       # List directory
"run command echo hello" # Echo text
```

**Safety Features:**
- **Command Whitelist:** Only safe commands allowed
  - Allowed: dir, echo, ping, whoami, date, time, ipconfig
  - Blocked: rm, del, format, shutdown, regedit, etc.

- **Path Restrictions:**
  - Blocked: C:\Windows, C:\Program Files, C:\System32
  - Allowed: User directories, project folders

- **Rate Limiting:**
  - Max 10 actions per session
  - Prevents runaway automation
  - Manual override available

- **Action Confirmation:**
  - Potentially destructive actions require confirmation
  - Clear action descriptions before execution

**Example Interaction:**
```
You: Open VS Code and create a new Python file

Alisa (😏): Sure thing! Opening VS Code for you...
[VS Code launches]
Alisa (😌): Alright, it's open. Would you like me to create a new 
file or open an existing project?
```

**Configuration:**
- App paths: `desktop_actions.py` → `app_paths`
- Rate limit: `desktop_actions.py` → `MAX_ACTIONS_PER_SESSION`
- Safety rules: `desktop_actions.py` → `is_action_safe()`

**Best for:**
- Desktop automation
- Productivity enhancement
- Hands-free workflows
- Repetitive task automation

#### `start_phase10c.ps1`
**Purpose:** Launch with Task Memory & Habit Learning (Phase 10C)

**What it does:**
```powershell
# Same as Phase 10B, PLUS enables adaptive learning
```

**Usage:**
```powershell
.\scripts\start_phase10c.ps1
```

**Phase 10C Features Enabled:**

**1. Work Schedule Learning**
- Tracks activity by hour of day
- Identifies typical work hours
- Recognizes breaks and focus periods
- Adapts interruption timing

**Example:**
```
After 2 weeks of observation:
"I noticed you usually work on code between 2-6 PM. 
Should I avoid interrupting you during those hours?"
```

**2. Application Usage Patterns**
- Learns task → application associations
- Identifies frequently used tools
- Predicts needed applications

**Example:**
```
[You say "I need to debug this"]
Alisa: "Opening VS Code and the terminal for you, 
since you usually debug with both~"
```

**3. Silence Preference Detection**
- Analyzes silence durations by time of day
- Learns when you prefer quiet focus
- Adjusts spontaneous speech timing

**Example:**
```
"I've noticed you prefer longer periods of silence in 
the morning. I'll speak less often then~"
```

**4. Repeated Task Recognition**
- Detects frequently repeated tasks
- Offers automation suggestions
- Creates workflow shortcuts

**Example:**
```
"You've started your dev environment 5 times this week. 
Would you like me to create a startup script?"
```

**5. Context Switch Analysis**
- Tracks transitions between tasks
- Identifies work patterns
- Optimizes assistance timing

**Example:**
```
"You usually switch from coding to testing around 4 PM. 
Need me to run your tests?"
```

**6. Adaptive Behavioral Adjustments**
- Personality adapts to your preferences
- Speech frequency auto-adjusts
- Help offers become more relevant
- Emotional tone matches context

**Data Tracked:**
```json
{
  "work_schedule": {
    "14": [timestamps], // 2 PM
    "15": [timestamps], // 3 PM
    // ...
  },
  "app_usage": {
    "debugging": {
      "vscode": 15,
      "terminal": 12
    }
  },
  "silence_preferences": {
    "09": [300, 450, 600], // Morning: longer silences
    "14": [120, 180, 200]  // Afternoon: shorter OK
  },
  "repeated_tasks": {
    "start dev environment": 5,
    "run tests": 8
  }
}
```

**Learning Timeline:**
- **Day 1-3:** Basic observation, no adaptations
- **Day 4-7:** Initial patterns detected
- **Week 2:** Confident predictions, starts suggesting
- **Week 3+:** Fully adaptive, personalized behavior

**Privacy:**
- All data stored locally (`task_memory.json`)
- No external transmission
- Can be cleared anytime
- User has full control

**Configuration:**
- Storage path: `task_memory.py` → `storage_path`
- Learning rate: `task_memory.py` → `MIN_OBSERVATIONS`
- Interrupt logic: `task_memory.py` → `should_interrupt_now()`

**Best for:**
- Long-term usage (weeks to months)
- Personalization over time
- Adaptive assistance
- Workflow optimization
- Habit-aware interaction

---

## 🧪 Python Testing & Utility Scripts

### Testing Scripts

#### `test_idle_system.py`
**Purpose:** Comprehensive test suite for Phase 9B Idle Companion System

**What it tests:**
```python
1. Core chat functionality
   - Message sending/receiving
   - Response collection
   - Emotion extraction

2. Idle detection logic
   - Silence tracking
   - Category calculation (short/medium/long/very_long)
   - Probability adjustments

3. Thought generation
   - Context-aware prompts
   - Vision integration
   - Desktop context inclusion

4. Cooldown management
   - Minimum intervals
   - Reset logic
   - Probability modifiers

5. Vision state integration
   - Presence detection
   - Attention tracking
   - Context building
```

**Usage:**
```powershell
python .\scripts\test_idle_system.py
```

**Output Example:**
```
🧪 Testing Idle Companion System

✅ Test 1: Chat system integrity
   - WebSocket connection: OK
   - Message sending: OK
   - Response parsing: OK

✅ Test 2: Idle detection
   - 180s silence → Category: medium
   - Probability: 0.15 → 0.23 (with modifiers)
   - Should speak: True

✅ Test 3: Context generation
   - Vision state: present, focused
   - Desktop context: coding_python, vscode
   - Prompt length: 456 characters

All tests passed! ✨
```

**Requirements:**
- Backend must be running
- Python 3.10+

**Best for:**
- Development
- Regression testing
- Debugging idle behavior

#### `test_phase10b.py`
**Purpose:** Test suite for Phase 10B Desktop Actions System

**What it tests:**
```python
1. Action parsing
   - Command interpretation
   - Parameter extraction
   - Intent recognition

2. Permission system
   - Safe command validation
   - Path restriction checking
   - Whitelist enforcement

3. Safety features
   - Blacklist filtering
   - Dangerous action blocking
   - Confirmation requirements

4. Rate limiting
   - Session action counter
   - Limit enforcement
   - Reset functionality

5. Execution flow
   - pyautogui integration
   - psutil process management
   - subprocess safety
```

**Usage:**
```powershell
python .\scripts\test_phase10b.py
```

**Output Example:**
```
🧪 Testing Desktop Actions System

✅ Test 1: Action parsing
   - "open chrome" → Action: open_app, Param: chrome
   - "type hello" → Action: type_text, Text: hello
   - "click 100 200" → Action: click, X: 100, Y: 200

✅ Test 2: Safety checks
   - "rm -rf /" → ❌ BLOCKED (blacklisted)
   - "read C:\Windows\system.ini" → ❌ BLOCKED (restricted path)
   - "open notepad" → ✅ ALLOWED

✅ Test 3: Rate limiting
   - Action 1-10: ✅ Allowed
   - Action 11: ❌ Rate limit exceeded

All safety tests passed! 🛡️
```

**Requirements:**
- Backend running
- pyautogui installed
- psutil installed

**Best for:**
- Safety validation
- Action testing
- Security audits

#### `test_phase10c.py`
**Purpose:** Test suite for Phase 10C Task Memory & Habit Learning System

**What it tests:**
```python
1. Pattern detection
   - Work schedule identification
   - Silence pattern recognition
   - Task sequence detection

2. Learning algorithms
   - Observation accumulation
   - Pattern confidence calculation
   - Threshold validation

3. Data persistence
   - JSON save/load
   - Data integrity
   - Migration handling

4. Interrupt logic
   - Work hour detection
   - Silence preference matching
   - Context-appropriate timing

5. Adaptive insights
   - Task prediction
   - App usage suggestions
   - Behavioral adjustments
```

**Usage:**
```powershell
python .\scripts\test_phase10c.py
```

**Output Example:**
```
🧪 Testing Task Memory System

✅ Test 1: Pattern detection
   - 15 observations → Work hours: 14:00-18:00
   - Silence preferences: Morning (300s+), Afternoon (120s+)
   - Top task: "debugging" (8 occurrences)

✅ Test 2: Learning timeline
   - Day 1-3: Observation mode
   - Day 4-7: Pattern detection
   - Week 2+: Active suggestions

✅ Test 3: Interrupt decisions
   - During work hours (14-18): ❌ Don't interrupt
   - Outside work hours: ✅ OK to speak
   - User absent: ⏸️ Wait for return

✅ Test 4: Data persistence
   - Saved 247 observations
   - Loaded successfully
   - Data integrity: OK

All learning tests passed! 🧠
```

**Requirements:**
- Backend running
- Write access to project directory

**Best for:**
- Learning algorithm validation
- Pattern detection testing
- Long-term behavior verification

---

### Utility Scripts

#### `view_history.py`
**Purpose:** View and analyze conversation history from database

**What it does:**
```python
1. Connect to alisa_memory.db
2. Query ConversationHistory table
3. Format and display messages
4. Show statistics
```

**Usage:**
```powershell
python .\scripts\view_history.py
```

**Output Example:**
```
📜 Conversation History (Session: abc123)

Total Messages: 24
User Messages: 12
Assistant Messages: 12
Date Range: 2026-01-15 to 2026-01-17

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[2026-01-17 14:23:45] User:
Hello Alisa!

[2026-01-17 14:23:47] Assistant:
Hey there! What's up? *smirks*

[2026-01-17 14:24:10] User:
Can you help me debug this code?

[2026-01-17 14:24:15] Assistant:
Of course! Show me what you're working on and I'll take a look~

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Statistics:
- Average message length: 87 characters
- Most common emotion: teasing (8 times)
- Conversation duration: 2 hours, 45 minutes
```

**Options:**
```powershell
# View last N messages
python .\scripts\view_history.py --limit 10

# Filter by session
python .\scripts\view_history.py --session abc123

# Export to file
python .\scripts\view_history.py --export history.txt

# Show statistics only
python .\scripts\view_history.py --stats
```

**Requirements:**
- Backend database exists (alisa_memory.db)
- SQLAlchemy installed

**Best for:**
- Debugging conversations
- Analyzing interactions
- Data export
- Quality assurance

---

## 📋 Complete Usage Examples

### Example 1: Minimal Setup (Text Chat Only)

**Goal:** Basic conversation with voice output

**Steps:**
```powershell
# Terminal 1: Backend server
.\scripts\start_backend.ps1

# Wait for "Application startup complete"

# Terminal 2: Text chat
.\scripts\start_text_chat.ps1
```

**What you get:**
- Type messages in terminal
- Receive voice responses
- Emotion indicators in text
- Basic conversation memory

**Resource usage:** ~200MB RAM, <5% CPU

**Best for:** Quick testing, minimal setup, development

---

### Example 2: Standard Setup (Text + Avatar)

**Goal:** Visual feedback with animated avatar

**Steps:**
```powershell
# Terminal 1: Backend
.\scripts\start_backend.ps1

# Terminal 2: Avatar overlay
.\scripts\start_overlay.ps1

# Terminal 3: Text chat
.\scripts\start_text_chat.ps1
```

**What you get:**
- All from Example 1, PLUS:
- Animated avatar window
- Facial expressions change with emotion
- Mouth moves during speech
- Blinking animation

**Resource usage:** ~300MB RAM, ~10% CPU

**Best for:** Immersive experience, visual feedback

---

### Example 3: Voice Interaction

**Goal:** Hands-free voice conversation

**Steps:**
```powershell
# Terminal 1: Backend
.\scripts\start_backend.ps1

# Terminal 2: Overlay (optional but recommended)
.\scripts\start_overlay.ps1

# Terminal 3: Voice chat
.\scripts\start_voice.ps1
```

**What you get:**
- Press-to-talk recording
- Speech-to-text transcription
- Voice responses
- Natural conversation flow

**Resource usage:** ~400MB RAM, ~15% CPU

**Best for:** Natural interaction, accessibility, hands-free use

---

### Example 4: Presence-Aware Assistant

**Goal:** Alisa knows when you're present/away

**Steps:**
```powershell
# Terminal 1: Backend
.\scripts\start_backend.ps1

# Terminal 2: Overlay
.\scripts\start_overlay.ps1

# Terminal 3: Text chat
.\scripts\start_text_chat.ps1

# Terminal 4: Webcam vision
.\scripts\start_vision.ps1
```

**What you get:**
- All from Example 2, PLUS:
- Presence detection (present/absent)
- Attention tracking (focused/distracted)
- Alisa knows when you return
- Pauses when you're away

**Resource usage:** ~450MB RAM, ~15% CPU

**Best for:** Idle companion behavior, presence awareness

---

### Example 5: Full Desktop Integration (Phase 10A)

**Goal:** Context-aware assistance with desktop understanding

**Steps:**
```powershell
# Quick way:
.\scripts\start_phase10a.ps1

# Or manually:
# Terminal 1: Backend
.\scripts\start_backend.ps1

# Terminal 2: Overlay
.\scripts\start_overlay.ps1

# Terminal 3: Desktop vision (screen + webcam)
.\scripts\start_vision_screen.ps1

# Terminal 4: Text chat
.\scripts\start_text_chat.ps1
```

**What you get:**
- All from Example 4, PLUS:
- Application detection (what you're using)
- File type recognition (what you're working on)
- Task inference (what you're doing)
- Error detection (SyntaxError, build failures, etc.)
- Smart help offers at appropriate times

**Example interaction:**
```
[You're coding in VS Code]
[A SyntaxError appears in your terminal]

Alisa (😌): I noticed you're working on main.py and there 
seems to be a syntax error on line 42... would you like 
me to help debug it?
```

**Resource usage:** ~600MB RAM, ~20% CPU

**Best for:** Coding assistance, error help, contextual support

---

### Example 6: Desktop Automation (Phase 10B)

**Goal:** Alisa can control your desktop

**Steps:**
```powershell
# Quick way:
.\scripts\start_phase10b.ps1

# Or manually: Same as Phase 10A
# (Desktop actions are automatically enabled in backend)
```

**What you get:**
- All from Example 5, PLUS:
- Application launching/closing
- Browser tab control
- Keyboard/mouse automation
- File read/write
- Window management
- Safe command execution

**Example interaction:**
```
You: Open VS Code and navigate to my project folder

Alisa (😏): Sure thing! Opening VS Code...
[VS Code launches]

Alisa (😌): Alright, it's open! Which project folder 
should I navigate to?
```

**Resource usage:** ~600MB RAM, ~20% CPU

**Best for:** Productivity, automation, hands-free workflows

---

### Example 7: Complete AI Assistant (Phase 10C)

**Goal:** Long-term adaptive companion that learns your habits

**Steps:**
```powershell
# Quick way:
.\scripts\start_phase10c.ps1

# Or manually: Same as Phase 10B
# (Task memory learning is automatically enabled)
```

**What you get:**
- All from Example 6, PLUS:
- Work schedule learning
- App usage pattern recognition
- Silence preference detection
- Repeated task tracking
- Adaptive behavior over time
- Personalized suggestions

**Timeline:**
- **Week 1:** Basic observation, learning your patterns
- **Week 2:** Starting to make predictions and suggestions
- **Week 3+:** Fully personalized, knows your habits

**Example interaction (after 2 weeks):**
```
[You sit down at your computer at 2 PM]

Alisa (😌): Hey! Ready to start coding? I noticed you 
usually work on your Python project around this time. 
Want me to open VS Code and your terminal?

You: Yes please!

[VS Code and Terminal open automatically]

Alisa (😏): All set! By the way, you haven't committed 
your changes from yesterday. Should I remind you later?
```

**Resource usage:** ~600MB RAM, ~20% CPU

**Best for:** Daily use, long-term companionship, maximum personalization

---

## 🎯 Recommended Startup Sequences

### For Development/Testing
```powershell
1. .\scripts\start_backend.ps1
2. .\scripts\start_text_chat.ps1
```
Fast, minimal, good for testing changes.

### For Daily Use (Casual)
```powershell
1. .\scripts\start_backend.ps1
2. .\scripts\start_overlay.ps1
3. .\scripts\start_voice.ps1
4. .\scripts\start_vision.ps1
```
Voice interaction + avatar + presence detection.

### For Productivity (Advanced)
```powershell
.\scripts\start_phase10b.ps1
```
One command launches: backend + overlay + vision + desktop actions.

### For Long-Term Companionship
```powershell
.\scripts\start_phase10c.ps1
```
Maximum features, learns and adapts over time.

---

## 🔧 Script Technical Details

### PowerShell Script Architecture

All `.ps1` scripts follow this pattern:

```powershell
# 1. Error handling setup
$ErrorActionPreference = "Stop"

# 2. Path resolution
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
Set-Location $ProjectRoot

# 3. Environment setup
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv venv
}

# 4. Activation
.\venv\Scripts\Activate.ps1

# 5. Dependency check
if (-not (Test-Path "installed.flag")) {
    pip install -r requirements.txt
    New-Item "installed.flag"
}

# 6. Component launch
python <module>/<script>.py
```

### Automatic Features

**Virtual Environment Management:**
- Detects if venv exists
- Creates if missing
- Activates automatically
- Never requires manual activation

**Dependency Installation:**
- Checks for installed.flag
- Installs only if needed
- Caches installation state
- Fast subsequent launches

**Path Resolution:**
- Works from any directory
- Uses absolute paths
- Handles nested structures
- No manual navigation needed

**Error Recovery:**
- Catches Python errors
- Displays helpful messages
- Suggests fixes
- Non-zero exit codes

---

## 🚨 Troubleshooting

### Common Issues

#### 1. Script Execution Policy Error

**Error:**
```
.\scripts\start_backend.ps1 : File cannot be loaded because running 
scripts is disabled on this system.
```

**Cause:** PowerShell execution policy blocks scripts

**Solution:**
```powershell
# Check current policy
Get-ExecutionPolicy

# Set for current user (recommended)
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

# Or for current session only
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

**Verification:**
```powershell
Get-ExecutionPolicy -List
```

---

#### 2. Port Already in Use

**Error:**
```
ERROR:    [Errno 10048] error while attempting to bind on address 
('127.0.0.1', 8000): only one usage of each socket address is normally permitted
```

**Cause:** Backend already running or zombie process

**Solution:**
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Output: TCP 127.0.0.1:8000 ... LISTENING 12345
# Kill process by PID
taskkill /PID 12345 /F

# Or use PowerShell
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process -Force
```

---

#### 3. Module Not Found Errors

**Error:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**Cause:** Dependencies not installed or wrong Python environment

**Solutions:**

**A. Ensure venv is activated:**
```powershell
# You should see (venv) in your prompt
.\venv\Scripts\Activate.ps1

# Verify Python path
python -c "import sys; print(sys.executable)"
# Should show: ...\venv\Scripts\python.exe
```

**B. Reinstall dependencies:**
```powershell
pip install -r requirements.txt

# Or force reinstall
pip install --force-reinstall -r requirements.txt
```

**C. Check Python version:**
```powershell
python --version
# Should be Python 3.10 or higher
```

---

#### 4. Webcam Not Found

**Error:**
```
Error: Unable to open webcam (device index 0)
```

**Cause:** Webcam in use, wrong index, or permission denied

**Solutions:**

**A. Check if webcam is in use:**
- Close other applications using camera (Zoom, Teams, etc.)

**B. Try different camera index:**
```python
# Edit vision/webcam.py
cap = cv2.VideoCapture(1)  # Try 1, 2, 3...
```

**C. Check device manager:**
```powershell
# List video devices
Get-PnpDevice -Class Camera
```

**D. Grant permissions (Windows 11):**
- Settings → Privacy → Camera
- Allow desktop apps to access camera

---

#### 5. Tesseract OCR Not Found

**Error:**
```
TesseractNotFoundError: tesseract is not installed or it's not in your PATH
```

**Cause:** Tesseract not installed or not in PATH

**Solutions:**

**A. Install with Chocolatey (recommended):**
```powershell
# Install Chocolatey if not installed
choco install tesseract

# Verify installation
tesseract --version
```

**B. Manual installation:**
1. Download from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install to: `C:\Program Files\Tesseract-OCR`
3. Add to PATH:
```powershell
$env:PATH += ";C:\Program Files\Tesseract-OCR"
# Or add permanently via System Properties → Environment Variables
```

**C. Specify path in code:**
```python
# Edit vision/screen_analyze.py
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

---

#### 6. Edge TTS Voice Not Working

**Error:**
```
No audio output / Silent speech
```

**Cause:** Edge TTS issue, audio device problem, or codec missing

**Solutions:**

**A. Test Edge TTS directly:**
```powershell
edge-tts --voice en-US-AnaNeural --text "Test" --write-media test.mp3
# If this works, issue is with PyGame

# If this fails, reinstall Edge TTS
pip uninstall edge-tts
pip install edge-tts
```

**B. Check audio device:**
```powershell
# List audio devices
Get-AudioDevice -List

# Verify default playback device is correct
```

**C. Test PyGame audio:**
```python
python
>>> import pygame
>>> pygame.mixer.init()
>>> pygame.mixer.music.load("test.mp3")
>>> pygame.mixer.music.play()
```

**D. Verify voice name:**
```python
# Edit voice/voice_config.py
SELECTED_VOICE = "ana"  # Try different voices
```

---

#### 7. High CPU Usage

**Symptoms:**
- CPU at 80-100%
- System slowdown
- Fan noise

**Cause:** Vision processing too intensive

**Solutions:**

**A. Switch to lighter preset:**
```python
# Edit vision/vision_config.py
apply_preset("ultra_light")
```

**B. Increase detection interval:**
```python
# vision/vision_config.py
DETECTION_INTERVAL = 3.0  # From 1.5s to 3s
```

**C. Disable screen capture:**
```powershell
# Use basic vision instead of screen vision
.\scripts\start_vision.ps1
# Instead of
.\scripts\start_vision_screen.ps1
```

**D. Disable MediaPipe:**
```python
# vision/vision_config.py
USE_MEDIAPIPE = False  # Use Haar Cascade instead
```

---

#### 8. LLM Not Responding

**Error:**
```
Error: Connection refused [Errno 10061]
or
LLM streaming failed
```

**Cause:** LLM server not running

**Solutions:**

**A. Start llama-server:**
```powershell
cd F:\llama
.\llama-server.exe `
  -m .\models\Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf `
  -c 4096 `
  -ngl 33 `
  --split-mode layer
```

**B. Verify LLM server is running:**
```powershell
# Test endpoint
Invoke-WebRequest -Uri "http://127.0.0.1:8080/health"
```

**C. Check LLM URL in code:**
```python
# Edit backend/app/llm_client.py
LLM_URL = "http://127.0.0.1:8080/v1/chat/completions"
# Ensure port matches your llama-server
```

---

#### 9. WebSocket Connection Failed

**Error:**
```
WebSocketException: Connection refused
or
Failed to connect to backend
```

**Cause:** Backend not running or wrong URL

**Solutions:**

**A. Ensure backend is running:**
```powershell
# Check if backend is running
Invoke-WebRequest -Uri "http://127.0.0.1:8000/"
```

**B. Verify WebSocket URL:**
```python
# Check in voice/text_chat.py or vision/vision_client.py
WS_URL = "ws://127.0.0.1:8000/ws/chat"
# Ensure port is 8000 (backend default)
```

**C. Check firewall:**
```powershell
# Allow Python through firewall
New-NetFirewallRule -DisplayName "Python" -Direction Inbound -Program "C:\Path\To\python.exe" -Action Allow
```

---

#### 10. Virtual Environment Issues

**Error:**
```
venv\Scripts\Activate.ps1 : The system cannot find the path specified.
```

**Cause:** Corrupted venv or wrong Python installation

**Solutions:**

**A. Delete and recreate venv:**
```powershell
Remove-Item -Recurse -Force venv
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**B. Verify Python installation:**
```powershell
python --version
where python

# Should show Python 3.10+ from official installation
```

**C. Use full path:**
```powershell
# Instead of just 'python'
C:\Python310\python.exe -m venv venv
```

---

### Performance Optimization

#### Reduce RAM Usage

**Current:** ~600MB with all features  
**Target:** <400MB

**Optimizations:**
```python
# 1. Use lighter vision preset
apply_preset("ultra_light")

# 2. Reduce memory buffer size
max_turns = 5  # From 10

# 3. Disable screen capture
# Don't use start_vision_screen.ps1

# 4. Lower LLM context
# llama-server: -c 2048  # From 4096
```

#### Reduce CPU Usage

**Current:** ~20% with all features  
**Target:** <10%

**Optimizations:**
```python
# 1. Increase detection intervals
DETECTION_INTERVAL = 3.0  # From 1.5
SCREEN_CAPTURE_INTERVAL = 20  # From 10

# 2. Increase frame skip
FRAME_SKIP = 4  # From 2

# 3. Disable MediaPipe
USE_MEDIAPIPE = False

# 4. Use quantized LLM model
# Already using Q4_K_M (optimal)
```

#### Improve Response Speed

**Current:** ~2-5s per response  
**Target:** <2s

**Optimizations:**
```powershell
# 1. Use GPU acceleration for LLM
.\llama-server.exe -ngl 99  # All layers on GPU

# 2. Reduce context window
-c 2048  # From 4096 (faster processing)

# 3. Use smaller model
# Or use quantized model (already using Q4_K_M)

# 4. Reduce memory buffer
max_turns = 5  # Less context to process
```

---

## 📊 Quick Reference Tables

### Script Comparison Matrix

| Script | Terminals | RAM | CPU | GPU | Complexity | Best Use Case |
|--------|-----------|-----|-----|-----|------------|---------------|
| `start_backend.ps1` | 1 | 100MB | <5% | No | ⭐ Simple | Required first |
| `start_text_chat.ps1` | +1 | +100MB | <5% | No | ⭐ Simple | Quick testing |
| `start_voice.ps1` | +1 | +150MB | ~10% | Optional | ⭐⭐ Moderate | Natural interaction |
| `start_overlay.ps1` | +1 | +50MB | <5% | No | ⭐ Simple | Visual feedback |
| `start_vision.ps1` | +1 | +100MB | ~10% | No | ⭐⭐ Moderate | Presence detection |
| `start_vision_screen.ps1` | +1 | +150MB | ~15% | No | ⭐⭐⭐ Complex | Desktop awareness |
| `start_phase10a.ps1` | 4 | ~600MB | ~20% | No | ⭐⭐⭐ Complex | Contextual help |
| `start_phase10b.ps1` | 4 | ~600MB | ~20% | No | ⭐⭐⭐⭐ Advanced | Automation |
| `start_phase10c.ps1` | 4 | ~600MB | ~20% | No | ⭐⭐⭐⭐⭐ Expert | Long-term use |

### Feature Availability Matrix

| Feature | Minimal | Standard | Voice | Vision | Phase 10A | Phase 10B | Phase 10C |
|---------|---------|----------|-------|--------|-----------|-----------|-----------|
| Text chat | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Voice output | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Voice input | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Avatar animations | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Emotion display | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Presence detection | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Attention tracking | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| App detection | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| Task inference | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| Error detection | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| Desktop actions | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| App control | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| Browser automation | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| Keyboard/mouse | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| Habit learning | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Schedule detection | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Pattern recognition | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Adaptive behavior | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |

### Component Dependencies

| Component | Requires Backend | Requires Overlay | Requires Vision | Requires LLM |
|-----------|-----------------|------------------|-----------------|--------------|
| Backend | - | No | No | Yes |
| Overlay | Yes | - | No | No |
| Text Chat | Yes | No (optional) | No | No |
| Voice Chat | Yes | No (optional) | No | No |
| Vision (webcam) | Yes | No | - | No |
| Vision (screen) | Yes | No | Yes (webcam) | No |
| Phase 10A | Yes | No (recommended) | Yes (screen) | No |
| Phase 10B | Yes | No (recommended) | Yes (screen) | No |
| Phase 10C | Yes | No (recommended) | Yes (screen) | No |

### Script Launch Order

**Recommended startup sequence:**

1. **Backend** (`start_backend.ps1`) - Always first
2. **LLM Server** (llama-server.exe) - Before backend or async
3. **Overlay** (`start_overlay.ps1`) - For visual feedback
4. **Vision** (`start_vision.ps1` or `start_vision_screen.ps1`) - For presence
5. **Interface** (`start_text_chat.ps1` or `start_voice.ps1`) - Last

**Phase scripts do this automatically in correct order**

---

## 💡 Pro Tips & Best Practices

### Development Tips

**1. Use `--reload` flag (already in scripts)**
```powershell
# Backend auto-reloads on code changes
# No need to restart after edits
```

**2. Keep backend terminal visible**
```powershell
# Watch for errors and debug info
# See WebSocket connections
# Monitor LLM requests
```

**3. Use test scripts before production**
```powershell
# Validate changes
python .\scripts\test_idle_system.py
python .\scripts\test_phase10b.py
```

**4. Monitor resource usage**
```powershell
# Task Manager → Performance tab
# Watch CPU/RAM during development
# Optimize hot paths
```

### Production Tips

**1. Use Phase scripts for simplicity**
```powershell
# One command launches everything
.\scripts\start_phase10c.ps1
```

**2. Create startup shortcut**
```powershell
# Windows shortcut properties:
Target: powershell.exe -NoExit -File "F:\Projects\Alisa\scripts\start_phase10c.ps1"
Start in: F:\Projects\Alisa\Alisa-AI Assistant
```

**3. Enable auto-start (Windows)**
```powershell
# Create shortcut in:
# C:\Users\<username>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
```

**4. Use Task Scheduler for advanced control**
```powershell
# Schedule Alisa to start at login
# Set delays between components
# Add error notifications
```

### Customization Tips

**1. Modify voice settings**
```python
# voice/voice_config.py
SELECTED_VOICE = "jenny"  # Try different voices
SPEECH_RATE = "+20%"  # Speak faster
PITCH_SHIFT = "+15Hz"  # Higher pitch
```

**2. Adjust idle behavior**
```python
# backend/app/idle_companion.py
MIN_SILENCE_FOR_SPEECH = {
    "short": 60,    # Speak after 1 min (from 2 min)
    "medium": 180,  # Speak after 3 min (from 5 min)
}
```

**3. Customize avatar**
```powershell
# Replace images in overlay/assets/
# Keep same names and dimensions (400x400)
# Use RGBA PNG format
```

**4. Tune vision performance**
```python
# vision/vision_config.py
apply_preset("ultra_light")  # Lower CPU
apply_preset("enhanced")     # Better accuracy
```

### Security Tips

**1. Review desktop actions whitelist**
```python
# backend/app/desktop_actions.py
# Modify app_paths for your apps
# Add safe commands to whitelist
# Block dangerous paths
```

**2. Limit rate limits if needed**
```python
# backend/app/desktop_actions.py
MAX_ACTIONS_PER_SESSION = 5  # From 10
```

**3. Review file access**
```python
# Only allow reading from specific folders
# Block system directories
```

**4. Monitor task memory data**
```powershell
# Check what's being learned
# Delete task_memory.json to reset
```

---

## 📂 Related Documentation

### Module Documentation
- **[Backend README](../backend/README.md)** - Backend server details
- **[Overlay README](../overlay/README.md)** - Avatar system guide
- **[Voice README](../voice/README.md)** - Voice I/O setup
- **[Vision README](../vision/README.md)** - Vision system guide

### Phase Documentation
- **[Phase 10A Getting Started](../docs/PHASE_10A_GETTING_STARTED.md)** - Desktop understanding
- **[Phase 10B Getting Started](../docs/PHASE_10B_GETTING_STARTED.md)** - Desktop actions
- **[Phase 10C Getting Started](../docs/PHASE_10C_GETTING_STARTED.md)** - Task memory

### Implementation Guides
- **[Phase 10A Implementation](../docs/PHASE_10A_IMPLEMENTATION.md)** - Technical details
- **[Phase 10B Implementation](../docs/PHASE_10B_IMPLEMENTATION.md)** - Action system
- **[Phase 10C Implementation](../docs/PHASE_10C_IMPLEMENTATION.md)** - Learning algorithms

### Visual Guides
- **[Phase 10A Visual Guide](../docs/PHASE_10A_VISUAL_GUIDE.md)** - Diagrams and flows
- **[Phase 10B Visual Guide](../docs/PHASE_10B_VISUAL_GUIDE.md)** - Action workflows
- **[Phase 10C Visual Guide](../docs/PHASE_10C_VISUAL_GUIDE.md)** - Learning processes

### System Documentation
- **[System Architecture](../docs/SYSTEM_ARCHITECTURE.md)** - Complete architecture
- **[Codebase Structure](../docs/CODEBASE_STRUCTURE.md)** - File-by-file guide
- **[Development Guide](../docs/DEVELOPMENT.md)** - Developer handbook

---

## 🎯 Next Steps

### New Users
1. ✅ Read this README (you're here!)
2. ⬜ Start with minimal setup (backend + text chat)
3. ⬜ Add overlay for visual feedback
4. ⬜ Try voice chat for natural interaction
5. ⬜ Enable vision for presence detection
6. ⬜ Explore Phase 10A for context awareness

### Intermediate Users
1. ✅ Comfortable with basic setup
2. ⬜ Try Phase 10B for desktop automation
3. ⬜ Customize voice and personality
4. ⬜ Optimize performance for your system
5. ⬜ Create custom startup scripts

### Advanced Users
1. ✅ Using Phase 10B/C features
2. ⬜ Contribute to codebase
3. ⬜ Create custom modules
4. ⬜ Optimize for production deployment
5. ⬜ Share your configurations

---

## 🤝 Contributing

Found a bug? Want to improve a script?

1. Check existing issues
2. Create detailed bug report
3. Submit pull request with fixes
4. Update documentation

**Script Testing Checklist:**
- ✅ Works from clean environment
- ✅ Error messages are clear
- ✅ Dependencies auto-install
- ✅ Paths resolve correctly
- ✅ Cleanup on exit

---

## 📜 Script Change Log

### Version 3.0 (Current)
- ✅ Phase 10C complete
- ✅ All 10 PowerShell scripts
- ✅ 4 Python test utilities
- ✅ Comprehensive error handling
- ✅ Auto-setup features

### Version 2.0
- ✅ Phase 10A/B implemented
- ✅ Desktop understanding
- ✅ Desktop actions
- ✅ Vision screen analysis

### Version 1.0
- ✅ Core scripts
- ✅ Basic functionality
- ✅ Backend + overlay + voice

---

**Scripts Version:** 3.0  
**Last Updated:** January 17, 2026  
**Status:** Production Ready ✅  
**Total Scripts:** 15 (10 PowerShell + 5 Python)

---

## 📞 Support

**Documentation:** [docs/README.md](../docs/README.md)  
**Issues:** Check backend/overlay/voice/vision logs  
**Community:** [GitHub Issues](https://github.com/Kush05Bhardwaj/Nexus-Alisa-AI-Assistant)