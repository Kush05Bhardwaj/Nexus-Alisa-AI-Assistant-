# 🖥️ Phase 10A: Visual System Guide

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         PHASE 10A SYSTEM                             │
│                    Desktop Understanding                             │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│   Desktop    │      │    Screen    │      │     OCR      │
│              │─────▶│   Capture    │─────▶│  Analysis    │
│ (Your Work)  │      │   (mss)      │      │(pytesseract) │
└──────────────┘      └──────────────┘      └──────────────┘
                                                      │
                                                      ▼
                              ┌──────────────────────────────────┐
                              │  Desktop Understanding System    │
                              │  - App Detection                 │
                              │  - File Type Recognition         │
                              │  - Task Inference                │
                              │  - Error Detection               │
                              │  - Offer Logic                   │
                              └──────────────────────────────────┘
                                                      │
                                                      ▼
                              ┌──────────────────────────────────┐
                              │    Context Message               │
                              │  [VISION_DESKTOP]                │
                              │  task|app|file|error|offer|...   │
                              └──────────────────────────────────┘
                                                      │
                                                      ▼
                              ┌──────────────────────────────────┐
                              │      Backend (ws.py)             │
                              │  - Parse desktop context         │
                              │  - Generate help offer           │
                              │  - Respond appropriately         │
                              └──────────────────────────────────┘
```

---

## Data Flow

```
Every 10 seconds:

1. CAPTURE
   ┌───────────────┐
   │  Screenshot   │ ◀─── mss (Windows screen capture)
   └───────────────┘
           │
           ▼
   ┌───────────────┐
   │  Extract Text │ ◀─── pytesseract OCR
   └───────────────┘
           │
           ▼
   ┌───────────────┐
   │  Window Info  │ ◀─── Active window title
   └───────────────┘

2. ANALYZE
   ┌───────────────┐
   │  Detect App   │ ◀─── VS Code? Chrome? Terminal?
   └───────────────┘
           │
           ▼
   ┌───────────────┐
   │  Detect File  │ ◀─── .py? .js? .pdf?
   └───────────────┘
           │
           ▼
   ┌───────────────┐
   │  Infer Task   │ ◀─── coding_python? browsing?
   └───────────────┘
           │
           ▼
   ┌───────────────┐
   │  Find Errors  │ ◀─── Regex patterns (error, exception, etc.)
   └───────────────┘

3. DECIDE
   ┌───────────────────────┐
   │   Should Offer Help?  │
   │                       │
   │   Error detected?     │ ──No──▶ Store context silently
   │          │            │
   │         Yes           │
   │          ▼            │
   │   Last offer > 5min?  │ ──No──▶ Store context silently
   │          │            │
   │         Yes           │
   │          ▼            │
   │   ✅ Offer Help       │
   └───────────────────────┘

4. SEND
   ┌───────────────────────────────────────────┐
   │  [VISION_DESKTOP]                         │
   │  coding_python|code|.py|true|true|        │
   │  VS Code|NameError: name 'x' is not...    │
   └───────────────────────────────────────────┘
                    │
                    ▼
   ┌───────────────────────────────────────────┐
   │  Backend processes and generates offer    │
   │  "I see you have a Python error.          │
   │   Want me to help?"                       │
   └───────────────────────────────────────────┘
```

---

## App Detection System

```
Window Title Analysis:

"main.py - Visual Studio Code"
         ↓
  Contains "visual studio code"
         ↓
    App Type: "code"
         ↓
    Category: CODE_EDITOR

"Python Error - Google Chrome"
         ↓
  Contains "chrome"
         ↓
    App Type: "browser"
         ↓
    Category: WEB_BROWSER

"output - PowerShell"
         ↓
  Contains "powershell"
         ↓
    App Type: "terminal"
         ↓
    Category: TERMINAL
```

### App Categories

```
┌────────────────────────────────────────────────────┐
│  CODE EDITORS                                      │
│  vscode, pycharm, sublime, atom, notepad++, vim    │
└────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────┐
│  BROWSERS                                          │
│  chrome, firefox, edge, safari, opera, brave       │
└────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────┐
│  TERMINALS                                         │
│  powershell, cmd, bash, git bash, wsl, terminal    │
└────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────┐
│  DOCUMENTS                                         │
│  word, notepad, text editor, writer                │
└────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────┐
│  PDF VIEWERS                                       │
│  acrobat, pdf, reader, foxit, sumatra              │
└────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────┐
│  COMMUNICATION                                     │
│  discord, slack, teams, zoom, skype                │
└────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────┐
│  MEDIA PLAYERS                                     │
│  vlc, spotify, youtube, windows media player       │
└────────────────────────────────────────────────────┘
```

---

## File Type Detection

```
Window Title: "main.py - VS Code"
                 ↓
         Extract filename
                 ↓
            "main.py"
                 ↓
         Get extension
                 ↓
              ".py"
                 ↓
         File Type: Python
```

### File Categories

```
CODE FILES
├── Python      → .py
├── JavaScript  → .js, .jsx, .ts, .tsx
├── Java        → .java
├── C/C++       → .c, .cpp, .h
├── Web         → .html, .css, .php
└── Go/Rust     → .go, .rs

DATA FILES
├── JSON        → .json
├── XML         → .xml
├── YAML        → .yaml, .yml
└── CSV         → .csv

DOCUMENTS
├── Text        → .txt, .md
├── PDF         → .pdf
└── Office      → .docx, .xlsx, .pptx

CONFIG FILES
└── Config      → .config, .ini, .env, .gitignore
```

---

## Task Inference System

```
Inputs:
┌─────────────────────┐
│  App Type: "code"   │
│  File Type: ".py"   │
│  Window: "VS Code"  │
└─────────────────────┘
         ↓
    Inference
         ↓
┌─────────────────────┐
│  Task: coding_python│
└─────────────────────┘
```

### Task Decision Tree

```
                      ┌─────────────┐
                      │  Start      │
                      └─────────────┘
                            │
              ┌─────────────┴─────────────┐
              │                           │
        ┌──────────┐                ┌──────────┐
        │   Code   │                │ Browser  │
        │   App?   │                │   App?   │
        └──────────┘                └──────────┘
              │                           │
         ┌────┴────┐                 ┌────┴────┐
         │         │                 │         │
      ┌─────┐  ┌─────┐          ┌────────┐ ┌────────┐
      │ .py │  │ .js │          │ GitHub │ │ YouTube│
      └─────┘  └─────┘          └────────┘ └────────┘
         │         │                 │         │
         ▼         ▼                 ▼         ▼
   coding_python  coding_js   browsing_code  watching_video
```

### All Tasks

```
CODING TASKS
├── coding_python       → VS Code + .py
├── coding_javascript   → VS Code + .js/.tsx
├── coding             → Generic code editor
└── editing_data       → JSON/CSV/XML files

BROWSING TASKS
├── browsing           → Generic web browsing
├── watching_video     → YouTube, VLC
├── browsing_code      → GitHub, GitLab
└── researching_problem→ StackOverflow, docs

DOCUMENT TASKS
└── reading_document   → PDF, Word, text

TERMINAL TASKS
├── running_python     → Terminal + "python"
├── using_git          → Terminal + "git"
└── terminal_work      → Generic terminal
```

---

## Error Detection System

```
Screen Text:
"Traceback (most recent call last):
  File "main.py", line 42, in <module>
    print(x)
NameError: name 'x' is not defined"

         ↓
    Scan for patterns
         ↓

Pattern Matching:
✅ "error" found
✅ "traceback" found
✅ "name 'x' is not defined" found

         ↓
    Error Detected
         ↓

Extract Context:
"NameError: name 'x' is not defined"
```

### Error Patterns (Regex)

```
Primary Patterns:
├── r"error"           ✅ Most common
├── r"exception"       ✅ Exceptions
├── r"failed"          ✅ Failed operations
├── r"not found"       ✅ Missing resources
└── r"cannot"          ✅ Unable to perform

Detailed Patterns:
├── r"unable to"       ✅ Permission issues
├── r"invalid"         ✅ Invalid input
├── r"undefined"       ✅ JS/TS undefined
├── r"null reference"  ✅ Null pointers
├── r"syntax error"    ✅ Code syntax
├── r"traceback"       ✅ Python traceback
└── r"stack trace"     ✅ Stack traces
```

---

## Offer Decision System

```
┌─────────────────────────────────────────────────┐
│          SHOULD OFFER HELP?                     │
└─────────────────────────────────────────────────┘

Step 1: Error Detected?
        ├── No  → ❌ Don't offer
        └── Yes → Continue

Step 2: Time Since Last Offer?
        ├── < 5 minutes → ❌ Cooldown active
        └── ≥ 5 minutes → Continue

Step 3: Appropriate Context?
        ├── Just browsing → ❌ Not stuck
        ├── Actively coding → ✅ Might need help
        └── Terminal error → ✅ Might need help

Step 4: ✅ OFFER HELP
```

### Cooldown Timeline

```
Offer 1: 10:00 AM
   ↓
   │ ─────── 5 minute cooldown ───────
   │
   ▼
10:05 AM - Can offer again
   ↓
   │ Error detected
   ▼
Offer 2: 10:06 AM
   ↓
   │ ─────── 5 minute cooldown ───────
   │
   ▼
10:11 AM - Can offer again
```

---

## Message Format

```
[VISION_DESKTOP]
task|app|file_type|has_error|should_offer|window_title|screen_text

Example 1: Python Error
[VISION_DESKTOP]
coding_python|code|.py|true|true|main.py - VS Code|NameError: name 'x'...

Example 2: Browsing (No Error)
[VISION_DESKTOP]
browsing|browser||false|false|Google - Chrome|Search results for...

Example 3: Git Error
[VISION_DESKTOP]
using_git|terminal||true|true|PowerShell|fatal: could not read...
```

### Field Breakdown

```
┌────────────────┬──────────────────────────────────┐
│ Field          │ Example                          │
├────────────────┼──────────────────────────────────┤
│ task           │ coding_python                    │
│ app            │ code                             │
│ file_type      │ .py                              │
│ has_error      │ true/false                       │
│ should_offer   │ true/false                       │
│ window_title   │ main.py - VS Code                │
│ screen_text    │ NameError: name 'x' is not...    │
└────────────────┴──────────────────────────────────┘
```

---

## Integration with Phase 9B

```
┌─────────────────────────────────────────────────────────────┐
│                  COMBINED SYSTEM                            │
│           Phase 9B + Phase 10A                              │
└─────────────────────────────────────────────────────────────┘

Phase 9B (Companion):
  ├── Tracks silence duration
  ├── Probability gates (8-40% based on time)
  └── Spontaneous speech triggers

Phase 10A (Desktop):
  ├── Understands desktop context
  ├── Detects errors
  └── Adds context to decisions

┌───────────────────────────────────────────────────────────┐
│  Example Scenario                                         │
├───────────────────────────────────────────────────────────┤
│  Time: User silent for 8 minutes                          │
│  Phase 9B: 14% chance to speak spontaneously              │
│  Phase 10A: Detects Python error on screen                │
│                                                            │
│  Decision:                                                │
│    Phase 9B gates: 14% chance PASSED                      │
│    Phase 10A context: Python error detected               │
│                                                            │
│  Result:                                                  │
│    Alisa: "Hmm, you've been quiet for a while.            │
│            Having trouble with that Python error?"        │
│                                                            │
│  vs. Without Phase 10A:                                   │
│    Alisa: "Hmm, you've been quiet for a while."           │
│            (generic, no context)                          │
└───────────────────────────────────────────────────────────┘
```

---

## Performance Profile

```
┌─────────────────────────────────────────────────┐
│  RESOURCE USAGE                                 │
├─────────────────────────────────────────────────┤
│  CPU:        5-10%                              │
│  RAM:        ~100MB                             │
│  Interval:   10 seconds                         │
│  Impact:     Minimal                            │
└─────────────────────────────────────────────────┘

Breakdown per Capture:
┌──────────────────────┬──────────────┐
│ Operation            │ Time         │
├──────────────────────┼──────────────┤
│ Screen Capture (mss) │ ~50ms        │
│ OCR (pytesseract)    │ ~200-500ms   │
│ Pattern Matching     │ ~10ms        │
│ Decision Logic       │ ~5ms         │
├──────────────────────┼──────────────┤
│ Total per Capture    │ ~265-565ms   │
└──────────────────────┴──────────────┘

10 second interval = 2.65-5.65% active processing
```

---

## Privacy Architecture

```
┌─────────────────────────────────────────────────┐
│  PRIVACY DESIGN                                 │
└─────────────────────────────────────────────────┘

Screen Capture
     ↓
[Image Buffer]
     ↓
OCR Extraction → [Text Only]
     ↓
❌ Image Discarded (not saved, not sent anywhere)
     ↓
Text Analysis
     ↓
Context Stored Locally
     ↓
[Latest Context Only - No History]

✅ No cloud uploads
✅ No screenshot storage
✅ No persistent history
✅ All processing local
✅ Periodic only (not constant)
```

---

## Configuration Visual Map

```
vision/vision_client_screen.py
├── SCREEN_CAPTURE_INTERVAL
│   ├── 5  → More responsive (higher CPU)
│   ├── 10 → Balanced (default)
│   └── 20 → Lighter (less frequent)

vision/desktop_understanding.py
├── Cooldown Duration
│   ├── 180  → 3 min (more offers)
│   ├── 300  → 5 min (default)
│   └── 600  → 10 min (rare offers)
│
├── Error Patterns
│   ├── self.error_patterns = [...]
│   └── Add custom: r"your_pattern"
│
└── App Categories
    ├── self.app_categories = {...}
    └── Add: "design": ["photoshop", "figma"]
```

---

## System States

```
┌─────────────────────────────────────────────────┐
│  STATE 1: UNDERSTANDING SILENTLY                │
│  ├── Screen captured every 10s                  │
│  ├── Context analyzed                           │
│  ├── No errors detected                         │
│  └── ✅ Stores context quietly                  │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│  STATE 2: ERROR DETECTED (COOLDOWN ACTIVE)      │
│  ├── Screen captured                            │
│  ├── Error found                                │
│  ├── Last offer < 5 min ago                     │
│  └── ❌ Doesn't offer (respects cooldown)       │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│  STATE 3: OFFERING HELP                         │
│  ├── Screen captured                            │
│  ├── Error found                                │
│  ├── Last offer ≥ 5 min ago                     │
│  └── ✅ Offers help                             │
└─────────────────────────────────────────────────┘
```

---

## File Structure Visual

```
f:\Projects\Alisa\Alisa-AI Assistant\
│
├── vision/
│   ├── desktop_understanding.py    ◀─── Core system
│   ├── vision_client_screen.py     ◀─── Screen client
│   ├── screen_capture.py           ◀─── mss capture
│   └── screen_analyze.py           ◀─── OCR analysis
│
├── backend/app/
│   └── ws.py                        ◀─── WebSocket handler
│
├── scripts/
│   └── start_phase10a.ps1          ◀─── Startup script
│
└── docs/
    ├── PHASE_10A_IMPLEMENTATION.md  ◀─── Full guide
    ├── PHASE_10A_QUICK_REF.md       ◀─── Quick reference
    ├── PHASE_10A_GETTING_STARTED.md ◀─── Setup guide
    └── PHASE_10A_VISUAL_GUIDE.md    ◀─── This file
```

---

## Success Indicators

```
✅ Working Correctly:
   ├── Logs show "🖥️ Context: ..." every 10s
   ├── App detection accurate
   ├── File types correct
   ├── Errors detected when present
   ├── Offers rare (5+ min apart)
   └── Low CPU/RAM usage

⚠️ Needs Tuning:
   ├── Too many offers → Increase cooldown
   ├── No offers at all → Check Tesseract, verify errors
   ├── Wrong app detection → Add custom patterns
   ├── High CPU → Increase interval
   └── Missing errors → Add custom error patterns
```

---

**Visual Guide Complete** 🖥️

This guide shows how Phase 10A works internally. For usage, see Getting Started Guide.
