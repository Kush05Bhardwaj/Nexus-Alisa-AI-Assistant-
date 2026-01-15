# 🔧 Backend - Alisa Assistant

FastAPI backend server with LLM integration, conversation memory, and WebSocket communication.

## 📋 Overview

The backend serves as the central brain of Alisa, handling:
- LLM integration and response streaming
- Persistent conversation memory (SQLite)
- WebSocket-based real-time communication
- Emotion detection and expression
- Multiple conversation modes
- Vision system integration

## 🚀 Quick Start

### Install Dependencies
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Start Server
```powershell
uvicorn app.main:app --reload
```

Server runs on: `http://127.0.0.1:8000`

## 📁 Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI entry point
│   ├── ws.py                # WebSocket chat handler
│   ├── llm_client.py        # LLM streaming integration
│   ├── emotion.py           # Emotion extraction
│   ├── memory.py            # Short-term memory buffer
│   ├── memory_long.py       # SQLite persistent storage
│   ├── prompt.py            # System prompt & personality
│   ├── modes.py             # Conversation modes
│   ├── db.py                # Database configuration
│   ├── models.py            # SQLAlchemy models
│   └── schemas.py           # Pydantic schemas
└── requirements.txt
```

## 🔌 API Endpoints

### Health Check
```
GET /
Returns: {"status": "ok", "message": "Alisa Backend Running"}
```

### WebSocket Chat
```
WS /ws/chat
Handles real-time chat with token streaming
```

## 💬 WebSocket Protocol

### Client → Server
```json
{"message": "Hello Alisa!"}
{"message": "/mode study"}
```

### Server → Client
```
[token]               # Response text chunks
[EMOTION]happy        # Detected emotion
[END]                 # Response complete
[MODE CHANGED]        # Mode switch confirmed
[VISION]data          # Vision system updates
```

## 🎭 Conversation Modes

- `default` - Tsundere personality
- `study` - Educational assistant
- `chill` - Casual conversation
- `creative` - Storytelling mode

**Switch modes:** Send `/mode <name>` via WebSocket

## 💾 Memory System

### Short-term Memory
- In-memory buffer for current session
- Stores last ~10 messages
- Managed by `memory.py`

### Long-term Memory
- SQLite database (`alisa_memory.db`)
- Persistent across restarts
- Auto-loads last 3000 tokens on startup
- Token-aware trimming
- Managed by `memory_long.py`

## ⚙️ Configuration

### LLM Server
Edit `app/llm_client.py`:
```python
LLM_API_URL = "http://127.0.0.1:8080/v1/chat/completions"
MODEL_NAME = "llama-3.2-3b-instruct"
```

### System Prompt
Edit `app/prompt.py` to customize Alisa's personality

### Database
SQLite database auto-created at:
- `backend/alisa_memory.db`

## 🔧 Dependencies

Key packages:
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `websockets` - WebSocket support
- `sqlalchemy` - Database ORM
- `aiohttp` - Async HTTP client
- `pydantic` - Data validation

## 🛠️ Development

### View Conversation History
```powershell
python view_history.py
```

### Clear Memory
```python
from app.memory_long import clear_history
clear_history()
```

### Database Migrations
Database schema auto-created on first run via SQLAlchemy models.

## 📊 Performance

- Token streaming for real-time responses
- Async/await for concurrent connections
- Token-based memory trimming (~3000 tokens)
- Connection pooling for database

## 🐛 Troubleshooting

**LLM not responding:**
- Check if LLM server is running on port 8080
- Verify `LLM_API_URL` in `llm_client.py`

**Database errors:**
- Delete `alisa_memory.db` to reset
- Check write permissions

**WebSocket disconnects:**
- Check CORS settings in `main.py`
- Verify client connection handling
