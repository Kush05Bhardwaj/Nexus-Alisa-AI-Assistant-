# 📁 Alisa Assistant - Codebase Structure

Complete documentation of project architecture and file organization.

---

## 📊 Project Overview

**Alisa Assistant** is a modular desktop AI companion with four main components:
1. **Backend** - FastAPI server with LLM integration and memory
2. **Overlay** - Animated avatar window with emotion expressions
3. **Voice** - Speech I/O with TTS, STT, and optional RVC
4. **Vision** - Presence detection and screen analysis

---

## 🗂️ Directory Structure

```
NexaAssistant/
├── backend/                     # FastAPI backend server
│   ├── app/
│   │   ├── main.py             # FastAPI entry point & routes
│   │   ├── ws.py               # WebSocket chat handler
│   │   ├── llm_client.py       # LLM streaming integration
│   │   ├── emotion.py          # Emotion extraction from responses
│   │   ├── memory.py           # Short-term conversation buffer
│   │   ├── memory_long.py      # SQLite persistent storage
│   │   ├── prompt.py           # System prompt & personality
│   │   ├── modes.py            # Conversation mode management
│   │   ├── db.py               # Database configuration
│   │   ├── models.py           # SQLAlchemy models
│   │   └── schemas.py          # Pydantic schemas
│   ├── requirements.txt
│   └── README.md               # Backend documentation
│
├── overlay/                     # Avatar overlay window
│   ├── assets/
│   │   ├── base.png           # Neutral expression
│   │   ├── happy.png          # Happy expression
│   │   ├── teasing.png        # Teasing expression
│   │   ├── serious.png        # Serious expression
│   │   ├── calm.png           # Calm expression
│   │   ├── sad.png            # Sad expression
│   │   ├── eyes_closed.png    # Blinking layer
│   │   └── mouth_open.png     # Talking layer
│   ├── main.py                # Entry point & WebSocket client
│   ├── avatar_window.py       # Tkinter UI & animations
│   ├── avatar_controller.py   # State management
│   ├── requirements.txt
│   └── README.md              # Overlay documentation
│
├── voice/                       # Voice I/O system
│   ├── rvc/                    # RVC voice conversion (optional)
│   │   ├── inferencer.py      # RVC inference engine
│   │   ├── weights/           # Model weights (.pth)
│   │   └── index/             # Feature index (.index)
│   ├── text_chat_v2.py        # Text input + voice output
│   ├── voice_chat_optimized.py # Full voice conversation
│   ├── voice_input.py         # Speech-to-text
│   ├── voice_output_edge.py   # Edge TTS
│   ├── voice_output_rvc.py    # Edge TTS + RVC
│   ├── voice_config.py        # Voice settings
│   ├── requirements.txt
│   └── README.md              # Voice documentation
│
├── vision/                      # Vision detection system
│   ├── vision_client.py       # Webcam presence detection
│   ├── vision_client_screen.py # Screen content analysis
│   ├── webcam.py              # Webcam capture
│   ├── face_emotion.py        # Face detection & emotion
│   ├── screen_capture.py      # Screenshot capture
│   ├── screen_analyze.py      # Screen analysis
│   ├── requirements.txt
│   └── README.md              # Vision documentation
│
├── Startup Scripts (PowerShell)
│   ├── start_backend.ps1      # Start backend server
│   ├── start_overlay.ps1      # Start avatar overlay
│   ├── start_text_chat.ps1    # Text chat mode
│   ├── start_voice.ps1        # Voice chat mode
│   ├── start_vision.ps1       # Webcam vision
│   └── start_vision_screen.ps1 # Screen analysis
│
├── Documentation
│   ├── README.md              # Main project README
│   ├── CODEBASE_STRUCTURE.md  # This file
│   └── [Module READMEs]       # See each module folder
│
└── Data Files
    ├── alisa_memory.db        # SQLite conversation history
    └── view_history.py        # View conversation history
```

---

## 🔧 Backend Component

### Core Files

**`main.py`** - FastAPI application entry
- Initializes FastAPI app
- Configures CORS for WebSocket
- Health check endpoint (`/`)
- WebSocket route (`/ws/chat`)
- Database initialization

**`ws.py`** - WebSocket chat handler
- Manages client connections
- Handles chat messages
- Streams LLM responses token-by-token
- Broadcasts to all clients (chat + overlay)
- Processes `/mode` commands
- Manages memory (short + long term)

**`llm_client.py`** - LLM integration
- Connects to local LLM server
- Async token streaming
- Default: `http://127.0.0.1:8080/v1/chat/completions`

**`emotion.py`** - Emotion extraction
- Extracts `<emotion=...>` tags from responses
- Validates emotions
- Returns clean text + emotion

**`memory.py`** - Short-term memory
- In-memory conversation buffer
- Stores ~10 recent messages
- Fast access for current session

**`memory_long.py`** - Long-term storage
- SQLite persistent storage
- Auto-loads last 3000 tokens on startup
- Token-aware trimming
- Conversation history management

**`prompt.py`** - System prompt
- Alisa's personality definition
- Customizable character traits

**`modes.py`** - Conversation modes
- `default`, `study`, `chill`, `creative`
- Mode-specific behaviors

### WebSocket Protocol

**Client → Server:**
```json
{"message": "Hello!"}
{"message": "/mode study"}
```

**Server → Client:**
```
[token]              # Response chunks
[EMOTION]happy       # Emotion update
[END]                # Response complete
[MODE CHANGED]       # Mode switch
[VISION]data         # Vision updates
```

---

## 🎭 Overlay Component

### Core Files

**`main.py`** - Entry point
- WebSocket client to backend
- Receives emotion/talk signals
- Forwards to avatar controller

**`avatar_window.py`** - Tkinter UI
- Transparent window
- Image compositing
- Animation rendering
- Drag functionality

**`avatar_controller.py`** - Business logic
- State management
- Emotion switching
- Talking animation
- Blinking animation

### Animation System

**Layers:**
1. Base (emotion expression)
2. Eyes (blink overlay)
3. Mouth (talk overlay)

**Triggers:**
- `[EMOTION]<name>` - Switch expression
- `[TALK_START]` - Start mouth animation
- `[TALK_END]` - Stop mouth animation

---

## 🎙️ Voice Component

### Core Files

**`text_chat_v2.py`** - Text + voice mode
- Text input from terminal
- Voice output via Edge TTS
- WebSocket backend communication

**`voice_chat_optimized.py`** - Full voice mode
- Speech input via Whisper
- Voice output via Edge TTS
- Continuous conversation loop

**`voice_input.py`** - Speech-to-text
- Faster Whisper integration
- Microphone recording
- Models: tiny, base, small, medium, large

**`voice_output_edge.py`** - Edge TTS
- Microsoft Edge TTS API
- Multiple voice options
- Customizable rate/pitch

**`voice_output_rvc.py`** - Edge TTS + RVC
- RVC voice conversion
- Custom anime voice
- Pitch shifting

**`voice_config.py`** - Settings
- Voice selection
- Speech rate/pitch
- RVC parameters

### RVC Structure

**`rvc/inferencer.py`** - RVC engine
**`rvc/weights/`** - Model files (.pth)
**`rvc/index/`** - Feature index (.index)

---

## 👁️ Vision Component

### Core Files

**`vision_client.py`** - Webcam mode
- Face detection
- Presence tracking
- Attention estimation
- Sends updates to backend

**`vision_client_screen.py`** - Screen mode
- Screenshot capture
- Content analysis
- Context understanding

**`webcam.py`** - Camera capture
- OpenCV webcam interface
- Frame processing
- Face detection

**`face_emotion.py`** - Emotion detection
- Haar Cascade face detection
- Basic emotion estimation
- Ready for CNN integration

**`screen_capture.py`** - Screenshot
- Screen capture utility
- Multi-monitor support

**`screen_analyze.py`** - Analysis
- Screen content understanding
- Application detection

---

## 🚀 Startup Scripts

**`start_backend.ps1`**
- Activates venv
- Starts uvicorn server

**`start_overlay.ps1`**
- Starts avatar overlay

**`start_text_chat.ps1`**
- Starts text chat with voice

**`start_voice.ps1`**
- Starts full voice conversation

**`start_vision.ps1`**
- Starts webcam vision

**`start_vision_screen.ps1`**
- Starts screen analysis

---

## 💾 Data Files

**`alisa_memory.db`** - SQLite database
- Conversation history
- Auto-created on first run
- Persistent across sessions

**`view_history.py`** - Utility script
- View conversation history
- Debug memory system

---

## 🔄 Communication Flow

```
User Input
    ↓
Voice/Text Client → WebSocket → Backend → LLM Server
                        ↓
                   Broadcast
                    ↙    ↘
            Client      Overlay
            (voice)     (animation)
```

---

## 📦 Dependencies

### Backend
- fastapi, uvicorn
- websockets
- sqlalchemy
- aiohttp
- pydantic

### Overlay
- tkinter (built-in)
- Pillow
- websockets

### Voice
- faster-whisper
- edge-tts
- sounddevice
- soundfile
- websockets

### Vision
- opencv-python
- numpy
- Pillow
- websockets
- mss (for screen capture)

---

## 🎯 Key Features by Component

**Backend:**
- LLM streaming
- Persistent memory
- Emotion detection
- Multi-mode conversations
- WebSocket broadcasting

**Overlay:**
- 6 emotion expressions
- Smooth animations
- Transparent window
- Audio-synced mouth

**Voice:**
- Speech-to-text (Whisper)
- Text-to-speech (Edge TTS)
- RVC voice conversion
- Multiple voices

**Vision:**
- Presence detection
- Attention tracking
- Face emotion estimation
- Screen analysis

---

For detailed module documentation, see:
- [Backend README](backend/README.md)
- [Overlay README](overlay/README.md)
- [Voice README](voice/README.md)
- [Vision README](vision/README.md)
```

---

#### `backend/app/memory_long.py` 💾
**Purpose:** Long-term memory persistence (SQLite database)

**Features:**
- Saves conversations to database
- Retrieves recent memories
- Associates emotions with messages

**Key Functions:**
```python
save_memory(emotion: str, text: str)     # Save to DB
fetch_recent_memories(limit: int) -> list # Retrieve memories
```

**Database Schema:**
- Table: `memories`
- Fields: `id`, `emotion`, `text`, `timestamp`

---

#### `backend/app/prompt.py` 📝
**Purpose:** System prompt and character personality

**Content:**
- Alisa's personality definition
- Tsundere character traits
- Conversation guidelines
- Emotion usage examples

**Key Function:**
```python
def build_prompt(mode: str, memories: list) -> list[dict]:
    # Returns messages array with system prompt
```

**Personality Highlights:**
- Tsundere anime-style character
- Caring but hides it with teasing
- Uses emotion tags in responses
- Adapts to different conversation modes

---

#### `backend/app/modes.py` 🎭
**Purpose:** Conversation mode management

**Available Modes:**
- `default` - Standard tsundere personality
- `study` - Focused, educational assistant
- `chill` - Relaxed, casual conversation
- `creative` - Imaginative, storytelling mode

**Key Functions:**
```python
set_mode(mode_name: str) -> bool       # Switch mode
get_mode_prompt() -> str                # Get current mode prompt
```

**Mode Switching:**
- User types `/mode study` in chat
- Backend switches personality
- Returns `[MODE CHANGED]` message

---

#### `backend/app/db.py` 🗄️
**Purpose:** Database configuration and initialization

**Features:**
- SQLAlchemy engine setup
- Session management
- Database initialization
- Table creation

**Database:** SQLite (`alisa_memory.db`)

---

#### `backend/app/models.py` 📋
**Purpose:** SQLAlchemy ORM models

**Models:**
- `Memory` - Long-term memory storage
  - `id`: Integer primary key
  - `emotion`: String
  - `text`: String
  - `timestamp`: DateTime

---

#### `backend/app/schemas.py` 📋
**Purpose:** Pydantic data validation schemas

**Schemas:**
- `MemoryCreate` - Validate new memories
- `MemoryResponse` - Format memory responses

---

## 📘 Overlay Component Details

### `overlay/main.py` ⭐
**Purpose:** Overlay entry point and WebSocket client

**Key Features:**
- Connects to backend WebSocket (`ws://127.0.0.1:8000/ws/chat`)
- Listens for broadcasted messages
- Updates avatar state based on messages
- Runs in background thread (async)
- Thread-safe UI updates via `root.after()`

**Message Handling:**
```python
[token]         → Start talking animation
[END]           → Stop talking animation
[EMOTION]emotion → Update emotion (future feature)
```

**Architecture:**
```
Background Thread (async):
  WebSocket Client → Message Queue

Main Thread (Tkinter):
  Avatar Window → Animation Loop
```

---

### `overlay/avatar_window.py` 🖼️
**Purpose:** Tkinter UI and animation rendering

**Key Features:**
- Transparent, always-on-top window
- Draggable avatar
- Layered image system (base + eyes + mouth)
- Talking animation (mouth flap)
- Blinking animation (periodic)
- Right-click to close

**Image Layers:**
1. **Base** - Main avatar image
2. **Eyes Closed** - Blinking overlay
3. **Mouth Open** - Talking overlay

**Animations:**
- **Talking:** Toggles mouth layer rapidly
- **Blinking:** Closes eyes briefly every 3-5 seconds

**Key Methods:**
```python
start_talking()  # Begin mouth animation
stop_talking()   # End mouth animation
_animate()       # Main animation loop
_blink()         # Blinking timer
```

---

### `overlay/avatar_controller.py` 🎮
**Purpose:** Business logic and state management

**Key Features:**
- Exposes simple API for main.py
- Manages avatar state (talking/idle)
- Thread-safe state updates

**API:**
```python
on_speech_start()  # Called when LLM starts responding
on_speech_end()    # Called when LLM finishes
```

**State Management:**
- `talking` - Boolean flag
- Prevents state conflicts

---

### `overlay/assets/` 🎨
**Purpose:** Avatar image resources

**Required Files:**
- `base.png` - Main avatar image (transparent background)
- `eyes_closed.png` - Eyes closed overlay
- `mouth_open.png` - Mouth open overlay

**Image Requirements:**
- PNG format with transparency
- Same dimensions (e.g., 400x400px)
- Aligned so overlays match base image

---

## 📘 Voice Component Details

### `voice/text_chat.py` ⭐
**Purpose:** Text input + voice output chat mode

**Use Case:** Type messages, hear voice responses (no microphone needed)

**Key Features:**
- Connects to backend WebSocket
- Displays streaming text responses
- Removes emotion tags before speaking
- Broadcasts to overlay for animations
- Chooses best available voice module

**Voice Priority:**
1. `voice_output_edge.py` (Edge TTS - recommended)
2. `voice_output_rvc.py` (Edge TTS + RVC)
3. `voice_output.py` (pyttsx3 fallback)

**Text Cleaning:**
```python
def clean_text_for_speech(text: str) -> str:
    # Removes <emotion=...> tags
    # Removes emotion words from start
    # Returns clean text for TTS
```

**Commands:**
- `/mode <name>` - Change conversation mode
- `exit` / `quit` - End chat

---

### `voice/voice_chat.py` ⭐
**Purpose:** Full voice input/output chat

**Use Case:** Speak to Alisa, hear voice responses

**Key Features:**
- Voice input via Whisper STT
- Voice output via Edge TTS or RVC
- WebSocket integration
- Push-to-talk or continuous listening

**Dependencies:**
- `voice_input.py` - Speech recognition
- `voice_output_edge.py` - TTS output

---

### `voice/voice_input.py` 🎤
**Purpose:** Speech-to-text using Whisper

**Key Features:**
- Records audio from microphone
- Uses faster-whisper for transcription
- Configurable model size
- Noise filtering

**Key Function:**
```python
def listen() -> str:
    # Returns transcribed text
```

**Whisper Models:**
- `tiny` - Fastest, less accurate
- `base` - Balanced (default)
- `small` - Better accuracy
- `medium` - High accuracy, slower

---

### `voice/voice_output.py` 🔊
**Purpose:** Basic TTS fallback (pyttsx3)

**Use Case:** When Edge TTS or RVC is unavailable

**Key Features:**
- Uses Windows built-in voices
- Selects female voice if available
- Fast, no internet required
- Lower quality than Edge TTS

**Key Function:**
```python
def speak(text: str):
    # Speaks using pyttsx3
```

---

### `voice/voice_output_edge.py` 🔊 (Recommended)
**Purpose:** High-quality TTS using Edge TTS

**Key Features:**
- Uses Microsoft Edge TTS API (free)
- Natural-sounding voices
- Customizable voice selection
- Configurable pitch and speech rate
- Saves audio as MP3
- Plays with pygame mixer

**Voice Selection:**
- Configured in `voice_config.py`
- Default: `en-US-AnaNeural` (young, energetic)
- Supports multiple languages

**Key Function:**
```python
async def speak_async(text: str):
    # Generates and plays TTS audio
```

**Process:**
1. Generate MP3 with Edge TTS
2. Save to `alisa_voice.mp3`
3. Play with pygame
4. Trigger overlay animations

---

### `voice/voice_output_rvc.py` 🔊
**Purpose:** Edge TTS + RVC voice conversion

**Use Case:** Convert Edge TTS to custom trained anime voice

**Key Features:**
- Uses Edge TTS as base
- Applies RVC voice conversion
- Customizable voice model
- Higher quality, more processing

**Requirements:**
- RVC model weights in `rvc/weights/alisa.pth`
- RVC index in `rvc/index/alisa.index`

**Key Function:**
```python
def speak(text: str):
    # TTS → RVC conversion → playback
```

**Process:**
1. Generate TTS (`base.wav`)
2. Convert with RVC (`alisa.wav`)
3. Play converted audio
4. Trigger overlay animations

---

### `voice/rvc/inferencer.py` 🔄
**Purpose:** RVC voice conversion engine

**Key Features:**
- Loads RVC model and index
- Performs voice conversion
- Pitch shifting
- Feature extraction

**Key Function:**
```python
def convert(input_wav: str, output_wav: str):
    # Converts voice using RVC model
```

**Configuration:**
- Model path: `rvc/weights/alisa.pth`
- Index path: `rvc/index/alisa.index`
- Pitch shift: configurable
- F0 method: harvest/crepe

---

### `voice/voice_config.py` ⚙️
**Purpose:** Voice settings and customization

**Configurable Options:**

```python
# Voice selection
SELECTED_VOICE = "ana"  # ana, nanami, xiaoxiao, etc.

# TTS prosody
SPEECH_RATE = "+15%"    # Speed
PITCH_SHIFT = "+10Hz"   # Pitch

# Emotion-based prosody (future)
EMOTION_PROSODY = {
    "happy": {"rate": "+15%", "pitch": "+8Hz"},
    "sad": {"rate": "-10%", "pitch": "-5Hz"},
    ...
}
```

**Available Voices:**
- **English:** `ana`, `jenny`, `aria`, `michelle`
- **Japanese:** `nanami`, `aoi`
- **Chinese:** `xiaoxiao`, `xiaoyi`

**Key Function:**
```python
def get_voice() -> str:
    # Returns Edge TTS voice ID
```

---

## 📘 Startup Scripts

### `start_backend.ps1` 🚀
**Purpose:** Start FastAPI backend server

**What It Does:**
1. Activates virtual environment
2. Changes to backend directory
3. Runs `uvicorn app.main:app --reload`

**Port:** 8000
**Auto-reload:** Enabled (for development)

---

### `start_overlay.ps1` 🚀
**Purpose:** Start avatar overlay window

**What It Does:**
1. Activates virtual environment
2. Changes to overlay directory
3. Runs `python main.py`

**Requires:** Backend running on port 8000

---

### `start_text_chat.ps1` 🚀
**Purpose:** Start text chat with voice output

**What It Does:**
1. Activates virtual environment
2. Changes to voice directory
3. Runs `python text_chat.py`

**Requires:** Backend running
**Optional:** Overlay running (for avatar animations)

---

### `start_voice.ps1` 🚀
**Purpose:** Start voice chat mode

**What It Does:**
1. Activates virtual environment
2. Changes to voice directory
3. Runs `python voice_chat.py`

**Requires:**
- Backend running
- Microphone available
- Whisper model downloaded

---

## 🔗 Component Interactions

### Full System Flow

```
┌─────────────┐
│    User     │
└──────┬──────┘
       │ (types/speaks)
       ▼
┌─────────────────────┐
│   Chat Client       │
│  (text_chat.py)     │
│  (voice_chat.py)    │
└──────┬──────────────┘
       │ WebSocket
       ▼
┌─────────────────────┐         ┌──────────────┐
│  Backend Server     │◄───────►│ LLM Server   │
│  (main.py/ws.py)    │ HTTP    │ (llama.cpp)  │
└──────┬──────────────┘         └──────────────┘
       │ Broadcast
       ├─────────────┐
       ▼             ▼
┌─────────────┐ ┌──────────────┐
│ Chat Client │ │   Overlay    │
│  (receives) │ │ (animations) │
└──────┬──────┘ └──────────────┘
       │
       ▼
┌─────────────┐
│   Voice     │
│  (speaks)   │
└─────────────┘
```

### WebSocket Message Flow

```
User Input → Backend → LLM → Backend
                              ↓
                      Broadcast to ALL:
                      ├─→ Chat Client (displays + speaks)
                      └─→ Overlay (animates)
```

### Startup Sequence

**Recommended Order:**
1. **Backend** (`start_backend.ps1`) - Must be first
2. **Overlay** (`start_overlay.ps1`) - Optional, for avatar
3. **Chat Client** (`start_text_chat.ps1` or `start_voice.ps1`)

**Minimum:**
- Backend + Chat Client (no avatar)

**Full Experience:**
- Backend + Overlay + Chat Client

---

## 🛠️ Development Guide

### Adding New Features

#### Add New Emotion
1. Edit `backend/app/emotion.py` - Add to `ALLOWED_EMOTIONS`
2. Edit `backend/app/prompt.py` - Document in system prompt
3. Edit `voice/text_chat.py` - Add to emotion cleaning list
4. Edit `overlay/avatar_window.py` - Add emotion expression (future)

#### Add New Voice
1. Edit `voice/voice_config.py` - Add to `VOICE_OPTIONS`
2. Test with `python voice/test_voice.py`

#### Add New Conversation Mode
1. Edit `backend/app/modes.py` - Add mode definition
2. Edit `backend/app/prompt.py` - Add mode-specific prompt
3. Test with `/mode <new_mode>` command

### Code Style
- **Backend:** FastAPI async patterns
- **Overlay:** Tkinter main thread safety
- **Voice:** Thread-safe audio handling
- **Comments:** Emoji + clear descriptions

### Testing
- **Backend:** Run backend, test with WebSocket client
- **Overlay:** Run overlay, check animations
- **Voice:** Run `test_voice.py` for voice testing
- **Integration:** Run full stack, test all features

---

## 📚 External Dependencies

### Backend
- FastAPI - Web framework
- Uvicorn - ASGI server
- SQLAlchemy - ORM
- Pydantic - Validation
- httpx - HTTP client
- websockets - WebSocket server

### Overlay
- Pillow (PIL) - Image handling
- websockets - WebSocket client

### Voice
- edge-tts - Microsoft Edge TTS
- faster-whisper - Speech recognition
- sounddevice - Audio input
- pygame - Audio playback
- soundfile - Audio file handling
- librosa - Audio processing (RVC)
- scipy - Signal processing (RVC)

### RVC (Optional)
- torch - Deep learning
- fairseq - RVC models
- librosa - Audio features
- scipy - Signal processing

---

## 🔧 Configuration Files

### `backend/app/llm_client.py`
```python
LLM_API_URL = "http://127.0.0.1:8080/v1/chat/completions"
MODEL_NAME = "your-model-name"
```

### `voice/voice_config.py`
```python
SELECTED_VOICE = "ana"
SPEECH_RATE = "+15%"
PITCH_SHIFT = "+10Hz"
```

### `overlay/main.py`
```python
WS_URL = "ws://127.0.0.1:8000/ws/chat"
```

---

## 📝 Data Storage

### SQLite Database (`alisa_memory.db`)
**Location:** Project root

**Tables:**
- `memories`
  - `id` (INTEGER PRIMARY KEY)
  - `emotion` (TEXT)
  - `text` (TEXT)
  - `timestamp` (DATETIME)

**Purpose:** Long-term conversation memory

---

## 🎯 Quick Reference

### Start System
```powershell
# Terminal 1 - Backend
.\start_backend.ps1

# Terminal 2 - Overlay (optional)
.\start_overlay.ps1

# Terminal 3 - Chat
.\start_text_chat.ps1  # or start_voice.ps1
```

### Install Dependencies
```powershell
# Backend
cd backend; pip install -r requirements.txt

# Overlay
cd overlay; pip install -r requirements.txt

# Voice
cd voice; .\install_voice.ps1  # or pip install -r requirements.txt
```

### Change Voice
```powershell
# Edit voice/voice_config.py
SELECTED_VOICE = "ana"  # or nanami, xiaoxiao, etc.

# Test
cd voice; python test_voice.py
```

### Change LLM
```python
# Edit backend/app/llm_client.py
LLM_API_URL = "http://your-llm-server:port/v1/chat/completions"
MODEL_NAME = "your-model-name"
```

---

## 🐛 Common Issues

### "Backend not running"
- Make sure `start_backend.ps1` is running
- Check port 8000 is not in use

### "Overlay won't connect"
- Start backend first
- Check WebSocket URL in `overlay/main.py`

### "No voice output"
- Install voice dependencies: `.\voice\install_voice.ps1`
- Check audio output device

### "RVC conversion fails"
- Make sure model files are in `voice/rvc/weights/` and `voice/rvc/index/`
- Fall back to Edge TTS (edit imports in `text_chat.py`)

---

## 📖 Additional Resources

- **Main README:** `README.md` - Project overview
- **Development Guide:** `DEVELOPMENT.md` - Developer docs
- **Quick Start:** `QUICKSTART.md` - Fast setup guide
- **Voice Setup:** `voice/VOICE_SETUP.md` - Voice configuration

---

**Last Updated:** January 14, 2026
**Version:** 1.0.0
**Maintainer:** Alisa Assistant Team
