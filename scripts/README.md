# 🚀 Alisa Scripts

This folder contains all startup scripts and utilities for the Alisa AI Assistant project.

## 🎮 Startup Scripts (PowerShell)

### Core System
- **`start_backend.ps1`** - Start the FastAPI backend server
  - Default: `http://127.0.0.1:8000`
  - WebSocket: `ws://127.0.0.1:8000/ws/chat`

### Interface Options
- **`start_text_chat.ps1`** - Start text-based chat interface
- **`start_voice_chat.ps1`** - Start voice chat with speech recognition
- **`start_overlay.ps1`** - Start avatar overlay window

### Vision Features
- **`start_vision.ps1`** - Start webcam face detection
- **`start_vision_screen.ps1`** - Start screen capture analysis

### Voice Only
- **`start_voice.ps1`** - Start voice-only mode (no text)

## 🧪 Utility Scripts (Python)

- **`test_idle_system.py`** - Test suite for idle thought engine
  - Verifies chat system isn't broken
  - Tests idle detection logic
  - Monitors for idle thoughts
  
- **`view_history.py`** - View conversation history from database

## 📋 Usage

### Quick Start (Recommended)
```powershell
# Terminal 1: Start backend
.\scripts\start_backend.ps1

# Terminal 2: Start text chat
.\scripts\start_text_chat.ps1

# Terminal 3 (optional): Start overlay
.\scripts\start_overlay.ps1
```

### Full Experience
```powershell
# Terminal 1: Backend
.\scripts\start_backend.ps1

# Terminal 2: Voice chat
.\scripts\start_voice_chat.ps1

# Terminal 3: Overlay
.\scripts\start_overlay.ps1

# Terminal 4: Vision (face detection)
.\scripts\start_vision.ps1
```

### Testing
```powershell
# Make sure backend is running first
.\scripts\start_backend.ps1

# In another terminal, run tests
python .\scripts\test_idle_system.py
```

## 🔧 Path Notes

All scripts are now in the `scripts/` folder. If you get path errors, make sure to:
1. Run scripts from the project root: `.\scripts\script_name.ps1`
2. Or navigate to scripts folder first: `cd scripts; .\script_name.ps1`

## 📂 Related Folders
- **`../docs/`** - Documentation and guides
- **`../backend/`** - Backend server code
- **`../overlay/`** - Avatar overlay system
- **`../vision/`** - Computer vision features
- **`../voice/`** - Voice input/output system

---

**Last Updated:** January 16, 2026
