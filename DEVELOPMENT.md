# 🛠️ Development Guide - Nexa Assistant

## 🏗️ Architecture Overview

### Backend (FastAPI)
```
backend/app/
├── main.py          → FastAPI app, CORS, routes
├── ws.py            → WebSocket endpoint (/ws/chat)
├── llm_client.py    → LLM API integration
├── memory.py        → Short-term conversation memory
├── memory_long.py   → Long-term memory (database)
├── emotion.py       → Emotion detection from text
├── modes.py         → Conversation modes (casual, professional, etc.)
├── prompt.py        → System prompts for LLM
├── db.py            → Database setup (SQLAlchemy)
├── models.py        → Database models
└── schemas.py       → Pydantic request/response schemas
```

### Overlay (Tkinter)
```
overlay/
├── main.py                 → Entry point, WebSocket client
├── avatar_window.py        → UI layer (Tkinter)
├── avatar_controller.py    → Business logic layer
├── assets/                 → Avatar images
└── test_overlay.py         → UI test script
```

---

## 🔌 Communication Protocol

### WebSocket Messages (Backend → Overlay)

| Message Type | Format | Trigger | Overlay Action |
|--------------|--------|---------|----------------|
| **Token** | `"Hello"` | LLM streams text | Call `start_talking()` |
| **End** | `"[END]"` | LLM finishes | Call `stop_talking()` |
| **Emotion** | `"[EMOTION]happy"` | Emotion detected | Call `on_emotion("happy")` |

### Example Flow

```python
# Backend (ws.py)
async for chunk in llm_stream():
    await websocket.send_text(chunk)  # "Hello", " world", ...

emotion = detect_emotion(full_text)
await websocket.send_text(f"[EMOTION]{emotion}")

await websocket.send_text("[END]")

# Overlay (main.py)
msg = await ws.recv()
if msg == "[END]":
    safe_stop_talking()
elif msg.startswith("[EMOTION]"):
    emotion = msg.replace("[EMOTION]", "")
    safe_on_emotion(emotion)
else:
    safe_start_talking()  # Any other token
```

---

## 🎨 Adding New Avatar Expressions

### Step 1: Create Images

Add new PNG files to `overlay/assets/`:
```
assets/
├── base.png          (existing)
├── eyes_closed.png   (existing)
├── mouth_open.png    (existing)
├── happy.png         (NEW)
├── sad.png           (NEW)
└── thinking.png      (NEW)
```

### Step 2: Load Images in `avatar_window.py`

```python
# Add after existing image loading
happy_img = ImageTk.PhotoImage(
    Image.open("assets/happy.png").resize((WINDOW_SIZE, WINDOW_SIZE))
)

sad_img = ImageTk.PhotoImage(
    Image.open("assets/sad.png").resize((WINDOW_SIZE, WINDOW_SIZE))
)
```

### Step 3: Create Expression Functions

```python
def show_happy():
    canvas.itemconfig(image_on_canvas, image=happy_img)

def show_sad():
    canvas.itemconfig(image_on_canvas, image=sad_img)

def show_neutral():
    canvas.itemconfig(image_on_canvas, image=base_img)
```

### Step 4: Update `avatar_controller.py`

```python
from avatar_window import show_happy, show_sad, show_neutral

def on_emotion(emotion: str):
    emotion = emotion.lower().strip()
    
    if emotion == "happy":
        show_happy()
    elif emotion == "sad":
        show_sad()
    elif emotion == "thinking":
        show_thinking()
    else:
        show_neutral()
    
    print(f"[Avatar Emotion] {emotion}")
```

---

## 🔧 Common Modifications

### Change Avatar Size

In `overlay/avatar_window.py`:
```python
WINDOW_SIZE = 400  # Default is 300
```

### Change Backend Port

In `backend/app/main.py`:
```python
# Run with: uvicorn app.main:app --port 8080
```

In `overlay/main.py`:
```python
WS_URL = "ws://127.0.0.1:8080/ws/chat"  # Update port
```

### Change Blink Frequency

In `overlay/avatar_window.py`:
```python
def blink():
    canvas.itemconfig(image_on_canvas, image=eyes_closed_img)
    root.after(120, lambda: canvas.itemconfig(image_on_canvas, image=base_img))
    root.after(random.randint(5000, 10000), blink)  # Default: 3000-6000
```

### Change Talking Animation Speed

In `overlay/avatar_window.py`:
```python
def animate_mouth():
    if not is_talking:
        return
    canvas.itemconfig(image_on_canvas, image=mouth_open_img)
    root.after(150, lambda: canvas.itemconfig(image_on_canvas, image=base_img))  # Default: 120
    root.after(300, animate_mouth)  # Default: 260
```

---

## 🐛 Debugging

### Enable Debug Logging

**Backend:**
```python
# In backend/app/ws.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Overlay:**
```python
# In overlay/main.py
print(f"[DEBUG] Received: {msg}")
```

### Test WebSocket Manually

```python
import asyncio
import websockets

async def test():
    async with websockets.connect("ws://127.0.0.1:8000/ws/chat") as ws:
        await ws.send("Hello")
        while True:
            msg = await ws.recv()
            print(msg)
            if msg == "[END]":
                break

asyncio.run(test())
```

### Check Thread Safety

```python
# In overlay/main.py
def safe_start_talking(self):
    print(f"[Thread] {threading.current_thread().name}")
    root.after(0, start_talking)
```

---

## 📦 Adding Dependencies

### Backend

```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install new-package
pip freeze > requirements.txt
```

### Overlay

```powershell
cd overlay
.\venv\Scripts\Activate.ps1
pip install new-package
pip freeze > requirements.txt
```

---

## 🧪 Testing

### Unit Tests (Future)

```python
# tests/test_avatar_window.py
import unittest
from overlay.avatar_window import start_talking, stop_talking

class TestAvatarWindow(unittest.TestCase):
    def test_talking_state(self):
        # Test implementation
        pass
```

### Integration Tests (Future)

```python
# tests/test_integration.py
import asyncio
import websockets

async def test_full_flow():
    # 1. Connect to backend
    # 2. Send message
    # 3. Verify tokens received
    # 4. Verify [END] received
    pass
```

---

## 📚 Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Tkinter Tutorial**: https://docs.python.org/3/library/tkinter.html
- **WebSockets Docs**: https://websockets.readthedocs.io/

---

## 🎯 Roadmap

### Phase 1 ✅ (Complete)
- [x] Basic avatar overlay
- [x] WebSocket communication
- [x] Talking animation
- [x] Thread-safe integration

### Phase 2 🚧 (In Progress)
- [ ] Emotion-based expressions
- [ ] Smooth transitions
- [ ] System tray icon

### Phase 3 📋 (Planned)
- [ ] Voice input/output
- [ ] Multiple avatar themes
- [ ] Configuration UI
- [ ] Plugin system

---

Made with ❤️ for Nexa Assistant
