# 📁 Alisa Assistant - Complete Codebase Structure

Complete documentation of all files, their purposes, and how they work together.

---

## 📊 Project Overview

**Alisa Assistant** is a desktop AI companion with three main components:
1. **Backend** - FastAPI server with LLM integration
2. **Overlay** - Animated avatar window using Tkinter
3. **Voice** - Speech input/output with optional RVC voice conversion

---

## 🗂️ Directory Structure

```
AlisaAssistant/
├── 📂 backend/                  # FastAPI backend server
│   ├── 📂 app/                  # Application code
│   │   ├── main.py             ⭐ FastAPI entry point & routes
│   │   ├── ws.py               ⭐ WebSocket chat handler
│   │   ├── llm_client.py       ⭐ LLM streaming integration
│   │   ├── emotion.py          📊 Extract emotion from responses
│   │   ├── memory.py           💾 Short-term conversation buffer
│   │   ├── memory_long.py      💾 Long-term SQLite storage
│   │   ├── prompt.py           📝 System prompt & personality
│   │   ├── modes.py            🎭 Conversation mode management
│   │   ├── db.py               🗄️  Database configuration
│   │   ├── models.py           📋 SQLAlchemy database models
│   │   └── schemas.py          📋 Pydantic data validation
│   └── requirements.txt        📦 Backend Python dependencies
│
├── 📂 overlay/                  # Avatar overlay window
│   ├── 📂 assets/              # Avatar images
│   │   ├── base.png           🎨 Base avatar image
│   │   ├── eyes_closed.png    👁️  Blinking animation layer
│   │   └── mouth_open.png     💬 Talking animation layer
│   ├── main.py                ⭐ Overlay entry point & WebSocket client
│   ├── avatar_window.py       🖼️  Tkinter UI & animation logic
│   ├── avatar_controller.py   🎮 Business logic & state management
│   └── requirements.txt       📦 Overlay Python dependencies
│
├── 📂 voice/                    # Voice input/output system
│   ├── 📂 rvc/                 # RVC voice conversion (optional)
│   │   ├── 📂 weights/        # RVC model weights (.pth files)
│   │   ├── 📂 index/          # RVC feature index (.index files)
│   │   └── inferencer.py      🔄 RVC inference engine
│   ├── text_chat.py           ⭐ Text input + voice output chat
│   ├── voice_chat.py          ⭐ Full voice input/output chat
│   ├── voice_input.py         🎤 Speech-to-text (Whisper)
│   ├── voice_output.py        🔊 Basic TTS (pyttsx3 fallback)
│   ├── voice_output_edge.py   🔊 Edge TTS (recommended)
│   ├── voice_output_rvc.py    🔊 Edge TTS + RVC conversion
│   ├── voice_config.py        ⚙️  Voice settings & customization
│   ├── install_voice.ps1      📥 Voice dependencies installer
│   ├── requirements.txt       📦 Voice Python dependencies
│   ├── README.md              📚 Voice module documentation
│   └── VOICE_SETUP.md         📚 Voice setup guide
│
├── 📜 Startup Scripts (PowerShell)
│   ├── start_backend.ps1      🚀 Start FastAPI backend
│   ├── start_overlay.ps1      🚀 Start avatar overlay
│   ├── start_text_chat.ps1    🚀 Start text chat mode
│   └── start_voice.ps1        🚀 Start voice chat mode
│
├── 📚 Documentation
│   ├── README.md              📖 Main project README
│   ├── DEVELOPMENT.md         🛠️  Development guide
│   ├── QUICKSTART.md          ⚡ Quick start guide
│   └── CODEBASE_STRUCTURE.md  📁 This file
│
└── 🗄️  Data Files
    └── alisa_memory.db        💾 SQLite database (auto-generated)
```

---

## 📘 Backend Component Details

### Core Application Files

#### `backend/app/main.py` ⭐
**Purpose:** FastAPI application entry point

**Key Features:**
- Initializes FastAPI app
- Configures CORS for WebSocket connections
- Defines HTTP health check endpoint (`/`)
- Registers WebSocket route (`/ws/chat`)
- Initializes database on startup

**Dependencies:**
- `ws.py` - WebSocket handler
- `db.py` - Database initialization

---

#### `backend/app/ws.py` ⭐
**Purpose:** WebSocket chat handler with broadcasting

**Key Features:**
- Manages WebSocket client connections list
- Handles real-time chat messages
- Streams LLM responses token-by-token
- **Broadcasts** tokens to ALL connected clients (chat client + overlay)
- Processes `/mode` commands for conversation modes
- Manages short-term and long-term memory

**Message Flow:**
```
User Input → WebSocket → LLM Client → Token Stream
                ↓
    Broadcast to ALL clients:
    - [token] - Response text chunks
    - [EMOTION]emotion - Detected emotion
    - [END] - Response complete
    - [MODE CHANGED] - Mode switch confirmed
```

**Key Functions:**
- `broadcast_message(message, exclude=None)` - Send to all connected clients
- `websocket_chat(websocket)` - Main chat loop

**Dependencies:**
- `llm_client.py` - LLM integration
- `memory.py` - Short-term memory
- `memory_long.py` - Long-term storage
- `emotion.py` - Emotion extraction
- `modes.py` - Mode management
- `prompt.py` - System prompts

---

#### `backend/app/llm_client.py` ⭐
**Purpose:** LLM integration and token streaming

**Key Features:**
- Connects to local LLM server (llama.cpp server)
- Streams responses token-by-token (async generator)
- Handles API requests to `http://127.0.0.1:8080/v1/chat/completions`

**Configuration:**
```python
LLM_API_URL = "http://127.0.0.1:8080/v1/chat/completions"
MODEL_NAME = "llama-3.2-3b-instruct"  # or your model
```

**Key Function:**
```python
async def stream_llm_response(messages: list[dict]) -> AsyncGenerator[str, None]:
    # Yields tokens one at a time
    yield token
```

**Dependencies:**
- External LLM server (llama.cpp or compatible)

---

#### `backend/app/emotion.py` 📊
**Purpose:** Extract emotion tags from LLM responses

**How It Works:**
1. Scans response text for `<emotion=...>` tags
2. Validates against allowed emotions
3. Removes tag from text, returns clean text + emotion

**Allowed Emotions:**
- `happy` - Cheerful, excited
- `calm` - Relaxed, peaceful
- `teasing` - Playful, mischievous
- `shy` - Embarrassed, bashful
- `serious` - Focused, stern
- `sad` - Disappointed, melancholic
- `neutral` - Default state

**Key Function:**
```python
def extract_emotion(text: str) -> tuple[str, str]:
    # Returns: (emotion, clean_text)
```

---

#### `backend/app/memory.py` 💾
**Purpose:** Short-term conversation memory (in-memory buffer)

**Features:**
- Stores recent messages in memory
- Maintains conversation context
- Configurable message limit (default: 10 messages)

**Key Class:**
```python
class MemoryBuffer:
    def add(role: str, content: str)  # Add message
    def get() -> list[dict]           # Get all messages
    def clear()                        # Clear memory
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
