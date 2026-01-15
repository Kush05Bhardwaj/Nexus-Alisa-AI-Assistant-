# 🎭 Overlay - Alisa Assistant

Animated avatar overlay window with transparent background and emotion-based animations.

## 📋 Overview

The overlay displays Alisa's animated avatar on your desktop with:
- Transparent, always-on-top window
- 6 emotion expressions (neutral, happy, teasing, serious, calm, sad)
- Smooth talking and blinking animations
- Draggable and interactive
- Audio-synced mouth movements
- Real-time emotion updates via WebSocket

## 🚀 Quick Start

### Install Dependencies
```powershell
cd overlay
pip install -r requirements.txt
```

### Start Overlay
```powershell
python main.py
```

Or use the startup script from project root:
```powershell
.\start_overlay.ps1
```

## 📁 Structure

```
overlay/
├── main.py                  # Entry point & WebSocket client
├── avatar_window.py         # Tkinter UI & animation logic
├── avatar_controller.py     # State management & business logic
├── assets/                  # Avatar images
│   ├── base.png            # Base avatar (neutral)
│   ├── happy.png           # Happy expression
│   ├── teasing.png         # Teasing expression
│   ├── serious.png         # Serious expression
│   ├── calm.png            # Calm expression
│   ├── sad.png             # Sad expression
│   ├── eyes_closed.png     # Blinking layer
│   └── mouth_open.png      # Talking layer
└── requirements.txt
```

## 🎨 Emotion System

### Available Emotions
- `neutral` - Default state
- `happy` - Cheerful, excited
- `teasing` - Playful, mischievous
- `serious` - Focused, stern
- `calm` - Relaxed, peaceful
- `sad` - Disappointed, melancholic

### How Emotions Work
1. Backend detects `<emotion=...>` tags in LLM responses
2. Emotion sent via WebSocket as `[EMOTION]<name>`
3. Overlay receives and switches expression
4. Expression persists until next emotion update

## 💬 Animation System

### Talking Animation
- Triggered by `[TALK_START]` message
- Toggles `mouth_open.png` layer
- Syncs with voice output
- Stops on `[TALK_END]` or after timeout

### Blinking Animation
- Automatic random blinking every 2-5 seconds
- Uses `eyes_closed.png` layer
- 150ms blink duration
- Continues during talking

### Layer Compositing
```
Base Layer (emotion expression)
  ↓
Eyes Layer (blink animation)
  ↓
Mouth Layer (talking animation)
  ↓
Final Composite
```

## 🔌 WebSocket Protocol

### Server → Overlay
```
[EMOTION]happy        # Change emotion
[TALK_START]          # Start talking animation
[TALK_END]            # Stop talking animation
```

## ⚙️ Configuration

### Window Settings
Edit `avatar_window.py`:
```python
WINDOW_WIDTH = 300
WINDOW_HEIGHT = 400
INITIAL_X = 100    # Starting X position
INITIAL_Y = 100    # Starting Y position
```

### Animation Timing
Edit `avatar_controller.py`:
```python
BLINK_INTERVAL = (2000, 5000)    # Random blink delay (ms)
BLINK_DURATION = 150              # Blink duration (ms)
TALK_TOGGLE_INTERVAL = 150        # Mouth animation speed (ms)
```

### Backend Connection
Edit `main.py`:
```python
BACKEND_WS_URL = "ws://127.0.0.1:8000/ws/chat"
```

## 🎨 Custom Avatars

### Image Requirements
- PNG format with transparency
- Recommended size: 512x512 or 1024x1024
- Consistent aspect ratio across all emotions
- Transparent background

### Adding New Emotions
1. Create new expression image: `assets/newemotion.png`
2. Update `avatar_controller.py`:
```python
self.emotions = {
    "neutral": "base.png",
    "newemotion": "newemotion.png",
    # ... other emotions
}
```
3. Update backend `emotion.py` to recognize the emotion

### Animation Layers
- `eyes_closed.png` - Only closed eyes, rest transparent
- `mouth_open.png` - Only open mouth, rest transparent
- Layers composited over base emotion image

## 🔧 Dependencies

Key packages:
- `tkinter` - GUI framework (included with Python)
- `Pillow` - Image processing
- `websockets` - WebSocket client

## 🛠️ Development

### Test Animations
```powershell
python test_animations.py
```

### Check Images
```powershell
python check_images.py
```

## 🎮 Usage Tips

**Dragging:**
- Click and drag the avatar to move it around your screen

**Closing:**
- Close the window or press Ctrl+C in terminal

**Multiple Monitors:**
- Avatar position saved per session
- May need adjustment when switching monitor setups

## 🐛 Troubleshooting

**Overlay not showing:**
- Check if images exist in `assets/` folder
- Verify tkinter is installed: `python -m tkinter`

**Animations not working:**
- Ensure backend WebSocket is running
- Check `BACKEND_WS_URL` in `main.py`

**Transparent background not working:**
- Windows 10/11 required for transparency
- Update graphics drivers

**Avatar appears black:**
- Verify PNG images have proper transparency
- Check image file corruption
