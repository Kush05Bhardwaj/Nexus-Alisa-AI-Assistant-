# Nexa Assistant - AI Desktop Companion

An intelligent desktop assistant with real-time avatar overlay and LLM backend.

## 🏗️ Project Structure

```
NexaAssistant/
├── backend/                    # FastAPI backend server
│   ├── app/
│   │   ├── main.py            # FastAPI app entry point
│   │   ├── ws.py              # WebSocket endpoints
│   │   ├── llm_client.py      # LLM integration
│   │   ├── memory.py          # Short-term memory
│   │   ├── memory_long.py     # Long-term memory
│   │   ├── emotion.py         # Emotion detection
│   │   ├── modes.py           # Conversation modes
│   │   ├── prompt.py          # System prompts
│   │   ├── db.py              # Database setup
│   │   ├── models.py          # SQLAlchemy models
│   │   └── schemas.py         # Pydantic schemas
│   └── requirements.txt       # Backend dependencies
│
├── overlay/                    # Avatar overlay frontend
│   ├── assets/                # Avatar images
│   │   ├── base.png
│   │   ├── eyes_closed.png
│   │   └── mouth_open.png
│   ├── main.py                # Overlay entry point ⭐
│   ├── avatar_window.py       # Tkinter UI layer
│   ├── avatar_controller.py   # Business logic layer
│   └── requirements.txt       # Overlay dependencies
│
├── voice/                      # Voice input/output (NEW!)
│   ├── voice_chat.py          # Main voice chat loop
│   ├── voice_input.py         # Speech-to-text (Whisper)
│   ├── voice_output.py        # Text-to-speech (pyttsx3)
│   ├── voice_output_rvc.py    # TTS with RVC conversion
│   ├── rvc/                   # RVC voice conversion
│   │   ├── inferencer.py
│   │   ├── weights/
│   │   └── index/
│   ├── requirements.txt       # Voice dependencies
│   └── README.md              # Voice module docs
│
├── alisa_memory.db            # SQLite database
└── README.md                  # This file
```

## 🚀 Quick Start

### 1. Setup Backend

```powershell
# Navigate to backend folder
cd NexaAssistant\backend

# Create virtual environment
python -m venv venv

# Activate venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run backend server
uvicorn app.main:app --reload
```

Backend will be available at: `http://127.0.0.1:8000`

### 2. Setup Overlay

```powershell
# Navigate to overlay folder (in new terminal)
cd NexaAssistant\overlay

# Create virtual environment
python -m venv venv

# Activate venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run overlay
python main.py
```

## 🎮 How It Works

### Communication Flow

```
User Input → Backend WebSocket → LLM Processing → Token Streaming
                    ↓
              [Token] / [END] / [EMOTION]
                    ↓
         Overlay WebSocket Client
                    ↓
         Avatar Animation (talking/idle)
```

### Backend → Overlay Messages

- **Streaming tokens** → Avatar starts talking (mouth animation)
- **`[END]`** → Avatar stops talking
- **`[EMOTION]<emotion>`** → Avatar changes expression (future feature)

## 🎯 Features

### ✅ Implemented
- Real-time WebSocket communication
- LLM token streaming
- Avatar talking animation
- Avatar blinking animation
- Draggable overlay window
- Short-term conversation memory
- Long-term memory storage
- Emotion detection (backend)

### 🚧 Planned
- Emotion-based avatar expressions
- Voice input/output
- System tray integration
- Settings panel
- Multiple avatar themes

## 🔧 Development

### Backend Architecture

- **FastAPI** - Web framework
- **WebSocket** - Real-time communication
- **SQLAlchemy** - ORM for database
- **LLM Client** - Integration with AI models

### Overlay Architecture

- **Tkinter** - GUI framework
- **PIL/Pillow** - Image handling
- **WebSockets** - Async client
- **Threading** - Thread-safe UI updates

### Key Design Patterns

1. **Separation of Concerns**
   - UI Layer (`avatar_window.py`)
   - Logic Layer (`avatar_controller.py`)
   - Network Layer (`main.py`)

2. **Thread Safety**
   - WebSocket runs in background thread (async)
   - Tkinter runs in main thread
   - Communication via `root.after()` for thread-safe updates

## 📝 API Endpoints

- `GET /` - Health check
- `WS /ws/chat` - WebSocket chat endpoint

## 🐛 Troubleshooting

**Overlay won't connect to backend**
- Make sure backend is running on port 8000
- Check firewall settings
- Verify WebSocket URL in `overlay/main.py`

**Avatar images not loading**
- Make sure you're running from `overlay/` directory
- Verify `assets/` folder contains PNG files
- Check file paths in `avatar_window.py`

**Backend errors**
- Check backend logs for errors
- Verify all dependencies are installed
- Ensure database file has write permissions

## 📄 License

MIT License

## 👥 Contributing

Contributions welcome! Please feel free to submit a Pull Request.
