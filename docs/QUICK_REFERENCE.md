# 📚 Quick Reference - Alisa Assistant

Quick reference guide for common tasks and commands.

## 🚀 Starting Components

```powershell
# Start all components (in separate terminals)
.\start_backend.ps1      # Backend server (required)
.\start_overlay.ps1      # Avatar overlay (optional)
.\start_vision.ps1       # Vision detection (optional)
.\start_text_chat.ps1    # Text chat mode
# OR
.\start_voice.ps1        # Voice chat mode
```

## 📖 Documentation Map

| Task | Documentation |
|------|---------------|
| **Get Started** | `README.md` |
| **Understand Structure** | `CODEBASE_STRUCTURE.md` |
| **Develop/Contribute** | `DEVELOPMENT.md` |
| **Backend Details** | `backend/README.md` |
| **Overlay Details** | `overlay/README.md` |
| **Voice Details** | `voice/README.md` |
| **Vision Details** | `vision/README.md` |

## ⚙️ Configuration Files

| Component | Config File | Purpose |
|-----------|-------------|---------|
| Backend LLM | `backend/app/llm_client.py` | LLM server URL & model |
| Backend Personality | `backend/app/prompt.py` | System prompt |
| Backend Modes | `backend/app/modes.py` | Conversation modes |
| Voice Settings | `voice/voice_config.py` | Voice, rate, pitch |
| Vision Settings | `vision/webcam.py` | Camera, detection |
| Overlay Animations | `overlay/avatar_controller.py` | Animation timing |

## 💬 In-Chat Commands

```
/mode default      # Standard tsundere
/mode study        # Study assistant
/mode chill        # Casual chat
/mode creative     # Storytelling
```

## 🔧 Common Tasks

### View Conversation History
```powershell
python view_history.py
```

### Clear Conversation History
```powershell
# Delete the database file
Remove-Item alisa_memory.db
```

### Change Voice
Edit `voice/voice_config.py`:
```python
SELECTED_VOICE = "ja-JP-NanamiNeural"  # Japanese (default)
# or
SELECTED_VOICE = "en-US-JennyNeural"   # English
```

### Adjust Voice Speed
Edit `voice/voice_config.py`:
```python
SPEECH_RATE = "+0%"    # Normal
SPEECH_RATE = "+20%"   # Faster
SPEECH_RATE = "-20%"   # Slower
```

### Test Microphone
```powershell
cd voice
python -c "import sounddevice; print(sounddevice.query_devices())"
```

### Test Webcam
```powershell
cd vision
python webcam.py
```

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Backend won't start | Check if port 8000 is free |
| LLM not responding | Verify LLM server on port 8080 |
| No voice output | Check internet connection (Edge TTS) |
| No microphone input | Check device permissions |
| Overlay not showing | Verify images in `overlay/assets/` |
| Webcam not working | Check camera permissions |

## 📦 Dependencies Installation

```powershell
# Backend
cd backend
pip install -r requirements.txt

# Overlay
cd overlay
pip install -r requirements.txt

# Voice
cd voice
pip install -r requirements.txt

# Vision
cd vision
pip install -r requirements.txt
```

## 🎨 Customization Quick Links

- **Change Personality**: `backend/app/prompt.py`
- **Add Emotions**: `overlay/assets/` + `backend/app/emotion.py`
- **Modify Animations**: `overlay/avatar_controller.py`
- **Voice Settings**: `voice/voice_config.py`
- **Vision Sensitivity**: `vision/webcam.py`

## 🔌 API Endpoints

- **Health Check**: `GET http://127.0.0.1:8000/`
- **WebSocket Chat**: `ws://127.0.0.1:8000/ws/chat`

## 📊 Performance Tuning

### For Speed
- Use smaller Whisper model: `voice/voice_input.py` → `MODEL_SIZE = "tiny"`
- Reduce vision FPS: `vision/webcam.py` → `FPS = 15`
- Disable RVC: Use `voice_output_edge.py` instead of `voice_output_rvc.py`

### For Quality
- Use larger Whisper model: `voice/voice_input.py` → `MODEL_SIZE = "medium"`
- Enable RVC: Use `voice_output_rvc.py`
- Increase vision resolution: `vision/webcam.py` → `FRAME_WIDTH = 1280`

## 🎯 Keyboard Shortcuts

### Text Chat
- `Ctrl+C` - Stop chat
- `Enter` - Send message

### Voice Chat
- `Space` - Push to talk (if enabled)
- `Ctrl+C` - Stop chat

## 📱 Quick Status Checks

```powershell
# Check if backend is running
curl http://127.0.0.1:8000

# Check Python version
python --version

# Check installed packages
pip list
```

## 🔗 Useful Links

- **GitHub**: https://github.com/Kush05Bhardwaj/Nexus-Alisa-AI-Assistant-
- **Edge TTS Voices**: https://speech.microsoft.com/portal/voicegallery
- **Whisper Models**: https://github.com/openai/whisper
- **RVC Project**: https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI

---

**Keep this file handy for quick reference! 📌**
