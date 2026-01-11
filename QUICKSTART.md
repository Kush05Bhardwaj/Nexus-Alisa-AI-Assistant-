# 🎯 Quick Start Guide - Nexa Assistant

## ⚡ Fastest Way to Run

### Windows (PowerShell)

**Option 1: Visual Chat (Text + Avatar)**

**Terminal 1 - Start Backend:**
```powershell
cd f:\Projects\Nexa\NexaAssistant
.\start_backend.ps1
```

**Terminal 2 - Start Overlay:**
```powershell
cd f:\Projects\Nexa\NexaAssistant
.\start_overlay.ps1
```

**Option 2: Voice Chat (Voice + Avatar)**

**Terminal 1 - Start Backend:**
```powershell
cd f:\Projects\Nexa\NexaAssistant
.\start_backend.ps1
```

**Terminal 2 - Start Overlay:**
```powershell
cd f:\Projects\Nexa\NexaAssistant
.\start_overlay.ps1
```

**Terminal 3 - Start Voice Chat:**
```powershell
cd f:\Projects\Nexa\NexaAssistant
.\start_voice.ps1
```

That's it! The PowerShell scripts handle everything automatically:
- ✅ Create virtual environments (if needed)
- ✅ Install dependencies (if needed)
- ✅ Activate environments
- ✅ Start servers

---

## 📁 Project Structure (Clean!)

```
NexaAssistant/
│
├── 📂 backend/              Backend server (FastAPI)
│   ├── app/                 Application code
│   │   ├── main.py         Entry point
│   │   ├── ws.py           WebSocket handler
│   │   ├── llm_client.py   LLM integration
│   │   └── ...
│   ├── venv/               Virtual environment
│   └── requirements.txt    Dependencies
│
├── 📂 overlay/              Frontend overlay (Tkinter)
│   ├── assets/             Avatar images
│   │   ├── base.png
│   │   ├── eyes_closed.png
│   │   └── mouth_open.png
│   ├── main.py            🎯 Entry point (RUN THIS)
│   ├── avatar_window.py    UI layer
│   ├── avatar_controller.py Logic layer
│   ├── test_overlay.py     Test script
│   ├── venv/              Virtual environment
│   └── requirements.txt    Dependencies
│
├── � voice/                Voice I/O (NEW!)
│   ├── voice_chat.py       🎙️ Voice chat loop
│   ├── voice_input.py      Speech-to-text
│   ├── voice_output.py     Text-to-speech
│   ├── voice_output_rvc.py TTS with RVC
│   ├── rvc/               RVC conversion
│   ├── venv/              Virtual environment
│   ├── requirements.txt    Dependencies
│   └── README.md          Voice docs
│
├── �📄 alisa_memory.db       Database
├── 📄 README.md             Full documentation
├── 📄 .gitignore            Git ignore rules
├── 🚀 start_backend.ps1     Backend startup script
├── 🚀 start_overlay.ps1     Overlay startup script
└── 🚀 start_voice.ps1       Voice chat startup script (NEW!)
```

---

## 🧪 Testing

### Test Overlay UI Only (No Backend Required)

```powershell
cd f:\Projects\Nexa\NexaAssistant\overlay
.\venv\Scripts\Activate.ps1
python test_overlay.py
```

This will:
- Show the avatar window
- Test blinking animation
- Test talking animation
- No backend connection needed

### Test with Backend

1. Start backend: `.\start_backend.ps1`
2. Start overlay: `.\start_overlay.ps1`
3. Use a chat client to send messages to `ws://127.0.0.1:8000/ws/chat`

---

## 🎮 How It Works

```
┌─────────────┐                    ┌──────────────┐
│   Backend   │                    │   Overlay    │
│  (FastAPI)  │◄────WebSocket─────►│  (Tkinter)   │
└─────────────┘                    └──────────────┘
       │                                   │
       │ 1. User sends message             │
       │ 2. LLM streams tokens             │
       ├──────────► "Hello"                │
       ├──────────► " how"          │ ▶️ START TALKING
       ├──────────► " are"                 │
       ├──────────► " you?"                │
       ├──────────► "[END]"         │ ⏸️ STOP TALKING
       │                                   │
```

---

## 🔧 Manual Setup (If Scripts Don't Work)

### Backend

```powershell
cd NexaAssistant\backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Overlay

```powershell
cd NexaAssistant\overlay
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

---

## ❓ Troubleshooting

| Problem | Solution |
|---------|----------|
| **"Could not connect to backend"** | Make sure backend is running first (`start_backend.ps1`) |
| **Images not loading** | Run from `overlay/` directory, check `assets/` folder exists |
| **PowerShell script won't run** | Run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| **Port 8000 already in use** | Kill the process or change port in `backend/app/main.py` |

---

## 🎯 Next Features to Add

- [ ] Emotion-based expressions (happy, sad, thinking)
- [ ] Voice input/output integration
- [ ] System tray icon
- [ ] Multi-avatar themes
- [ ] Configuration panel

---

## 📝 File Purposes

| File | Purpose |
|------|---------|
| `overlay/main.py` | Main entry point - integrates WebSocket + UI |
| `overlay/avatar_window.py` | Tkinter UI, animations, drag functionality |
| `overlay/avatar_controller.py` | Business logic, maps events to actions |
| `overlay/test_overlay.py` | Test UI without backend |
| `backend/app/ws.py` | WebSocket endpoint, sends tokens/emotions |
| `backend/app/main.py` | FastAPI app configuration |

---

Made with ❤️ for Nexa Assistant
