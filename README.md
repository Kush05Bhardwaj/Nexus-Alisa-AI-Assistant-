# 🌟 Alisa Assistant - AI Desktop Companion

Meet **Alisa**, your cute tsundere AI desktop companion! An intelligent assistant featuring real-time avatar overlay, voice chat, and LLM integration.

![Status](https://img.shields.io/badge/status-active-success)
![Python](https://img.shields.io/badge/python-3.10+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## ✨ Features

🎭 **Animated Avatar Overlay**
- Transparent, always-on-top window
- Talking and blinking animations
- Draggable and interactive

🗣️ **Voice Chat System**
- Text-to-speech with customizable voices
- Speech-to-text (Whisper integration)
- Optional RVC voice conversion for anime-style voice

🧠 **Smart AI Backend**
- Real-time LLM streaming responses
- Short and long-term memory
- Multiple conversation modes
- Emotion detection and expression

💬 **Flexible Chat Modes**
- Text chat with voice output
- Full voice conversation
- WebSocket-based real-time communication

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Windows (for PowerShell scripts)
- Local LLM server (llama.cpp recommended)

### 1️⃣ Clone Repository
```powershell
git clone https://github.com/Kush05Bhardwaj/Nexus-Alisa-AI-Assistant-.git
cd AlisaAssistant
```

### 2️⃣ Start Backend
```powershell
.\start_backend.ps1
```
*Backend runs on `http://127.0.0.1:8000`*

### 3️⃣ Start Overlay (Optional)
```powershell
.\start_overlay.ps1
```
*Shows animated avatar on screen*

### 4️⃣ Start Chat
```powershell
# Text chat with voice output (recommended for beginners)
.\start_text_chat.ps1

# OR full voice chat (requires microphone)
.\start_voice.ps1
```

**That's it!** 🎉 Type or speak to Alisa and she'll respond with voice!

---

## 📁 Project Structure

```
AlisaAssistant/
├── 📂 backend/          # FastAPI server with LLM integration
├── 📂 overlay/          # Animated avatar window (Tkinter)
├── 📂 voice/            # Voice I/O and TTS/STT
├── 🚀 start_*.ps1       # Easy startup scripts
└── 📚 docs/             # Documentation
```

📖 **For detailed file-by-file documentation, see [CODEBASE_STRUCTURE.md](CODEBASE_STRUCTURE.md)**

---

## 🎮 How It Works

```
┌─────────────┐
│    User     │ Types/Speaks
└──────┬──────┘
       │
       ▼
┌─────────────────────┐         ┌──────────────┐
│   Chat Client       │         │  LLM Server  │
│ (text/voice chat)   │◄───────►│ (llama.cpp)  │
└──────┬──────────────┘         └──────────────┘
       │ WebSocket
       ▼
┌─────────────────────┐
│  Backend Server     │ Broadcasts to:
│  (FastAPI/WS)       ├─→ Chat Client (displays + speaks)
└─────────────────────┘ └─→ Overlay (avatar animations)
```

**Key Components:**
1. **Backend** - Processes messages, streams LLM responses
2. **Overlay** - Displays animated avatar, syncs with speech
3. **Voice** - Handles TTS/STT, customizable voices

---

## 🎯 Usage Examples

### Text Chat Mode (Easiest)
```powershell
.\start_text_chat.ps1
```
- Type messages in terminal
- Hear Alisa's voice responses
- See avatar animations (if overlay running)

### Voice Chat Mode
```powershell
.\start_voice.ps1
```
- Speak to Alisa
- Get voice responses
- Natural conversation flow

### Change Conversation Mode
```
You: /mode study
Alisa: ✓ Mode changed successfully!
```

**Available Modes:**
- `default` - Standard tsundere personality
- `study` - Focused educational assistant
- `chill` - Relaxed casual chat
- `creative` - Imaginative storytelling

### Customize Voice
Edit `voice/voice_config.py`:
```python
SELECTED_VOICE = "ana"      # Options: ana, nanami, xiaoxiao, etc.
SPEECH_RATE = "+15%"         # Speed adjustment
PITCH_SHIFT = "+10Hz"        # Pitch adjustment
```

Test voices:
```powershell
cd voice
python test_voice.py
```

---

## 🛠️ Installation (Manual)

If startup scripts don't work, install manually:

### Backend
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Overlay
```powershell
cd overlay
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

### Voice
```powershell
cd voice
.\install_voice.ps1
# OR manually:
pip install -r requirements.txt
```

---

## 📚 Documentation

- **[CODEBASE_STRUCTURE.md](CODEBASE_STRUCTURE.md)** - Complete file-by-file documentation
- **[QUICKSTART.md](QUICKSTART.md)** - Quick setup guide
- **[DEVELOPMENT.md](DEVELOPMENT.md)** - Developer guide
- **[voice/VOICE_SETUP.md](voice/VOICE_SETUP.md)** - Voice customization guide

---

## 🔧 Configuration

### LLM Server
Edit `backend/app/llm_client.py`:
```python
LLM_API_URL = "http://127.0.0.1:8080/v1/chat/completions"
MODEL_NAME = "llama-3.2-3b-instruct"  # Your model
```

### Voice Settings
Edit `voice/voice_config.py`:
```python
SELECTED_VOICE = "ana"  # Voice selection
SPEECH_RATE = "+15%"    # Talking speed
PITCH_SHIFT = "+10Hz"   # Voice pitch
```

### WebSocket Connection
Edit `overlay/main.py` and `voice/text_chat.py`:
```python
WS_URL = "ws://127.0.0.1:8000/ws/chat"
```

---

## 🎨 Customization

### Change Avatar
Replace images in `overlay/assets/`:
- `base.png` - Main avatar
- `eyes_closed.png` - Blinking layer
- `mouth_open.png` - Talking layer

**Requirements:**
- PNG with transparency
- Same dimensions (e.g., 400x400px)
- Aligned layers

### Add New Emotion
1. Edit `backend/app/emotion.py` - Add emotion to `ALLOWED_EMOTIONS`
2. Edit `backend/app/prompt.py` - Document in system prompt
3. Edit `voice/text_chat.py` - Add to cleaning list

### Train Custom RVC Voice
1. Train RVC model for anime voice
2. Place `.pth` file in `voice/rvc/weights/`
3. Place `.index` file in `voice/rvc/index/`
4. Use `voice_output_rvc.py` instead of `voice_output_edge.py`

---

## 🐛 Troubleshooting

**Backend won't start**
- Check if port 8000 is in use
- Verify LLM server is running
- Check dependencies are installed

**Overlay won't connect**
- Start backend first
- Check WebSocket URL in `overlay/main.py`
- Verify backend is on port 8000

**No voice output**
- Run `.\voice\install_voice.ps1`
- Check audio output device
- Verify pygame is installed

**Avatar not animating**
- Make sure overlay is running
- Check assets folder has all PNG files
- Verify overlay connects to backend (check console)

**Voice quality issues**
- Try different voices in `voice_config.py`
- Adjust speech rate and pitch
- Consider using RVC for better quality

---

## 🚀 Roadmap

- [x] Basic chat functionality
- [x] Avatar overlay with animations
- [x] Voice output (TTS)
- [x] Voice input (STT)
- [x] Emotion detection
- [x] Conversation modes
- [x] Memory system
- [ ] Emotion-based avatar expressions
- [ ] System tray integration
- [ ] Settings UI panel
- [ ] Multiple avatar themes
- [ ] Plugin system

---

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- Add more avatar expressions
- Improve voice quality
- Add new conversation modes
- Create additional themes
- Optimize performance
- Write more documentation

**Steps:**
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

MIT License - see LICENSE file for details

---

## 🙏 Acknowledgments

- LLM integration powered by llama.cpp
- Voice synthesis via Microsoft Edge TTS
- Speech recognition via faster-whisper
- RVC voice conversion technology
- Avatar animations inspired by VTuber culture

---

## 📞 Support

**Issues:** Report bugs on [GitHub Issues](https://github.com/Kush05Bhardwaj/Nexus-Alisa-AI-Assistant-/issues)

**Questions:** Check `CODEBASE_STRUCTURE.md` for detailed documentation

---

<div align="center">

**Made with ❤️ by the Alisa Assistant Team**

🌟 Star this repo if you like it! 🌟

</div>
