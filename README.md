# 🌟 Alisa Assistant - AI Desktop Companion

Your cute tsundere AI desktop companion with real-time avatar overlay, voice chat, vision detection, and LLM integration.

![Status](https://img.shields.io/badge/status-active-success)
![Python](https://img.shields.io/badge/python-3.10+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## ✨ Features

- 🎭 **Animated Avatar** - Transparent overlay with 6 emotions and smooth animations
- 🗣️ **Voice System** - Speech-to-text, text-to-speech, optional RVC voice conversion
- 👁️ **Vision Detection** - Webcam presence tracking, attention detection, emotion estimation
- 🧠 **Smart AI Backend** - LLM streaming, persistent memory, emotion-aware responses
- 💾 **Conversation Memory** - SQLite storage with auto-loading and token management

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Windows (for PowerShell scripts)
- Local LLM server (llama.cpp recommended on `http://127.0.0.1:8080`)

### Installation

1. **Clone Repository**
```powershell
git clone https://github.com/Kush05Bhardwaj/Nexus-Alisa-AI-Assistant-.git
cd NexaAssistant
```

2. **Start Backend**
```powershell
.\start_backend.ps1
```

3. **Start Components** (in separate terminals)
```powershell
.\start_overlay.ps1      # Avatar overlay (optional)
.\start_vision.ps1       # Vision detection (optional)
.\start_text_chat.ps1    # Text chat with voice output
# OR
.\start_voice.ps1        # Full voice conversation
```

That's it! 🎉

---

## 📁 Project Structure

```
NexaAssistant/
├── backend/          # FastAPI server + LLM integration
├── overlay/          # Animated avatar window
├── voice/            # Voice I/O + TTS/STT
├── vision/           # Presence detection + screen analysis
└── start_*.ps1       # Startup scripts
```

**Detailed documentation in each module:**
- [Backend README](backend/README.md)
- [Overlay README](overlay/README.md)
- [Voice README](voice/README.md)
- [Vision README](vision/README.md)

---

## � Usage

### Text Chat Mode
```powershell
.\start_text_chat.ps1
```
- Type messages
- Hear voice responses
- See avatar animations

### Voice Chat Mode
```powershell
.\start_voice.ps1
```
- Speak naturally
- Get voice responses
- Full conversation

### Change Conversation Mode
```
/mode study      # Study assistant
/mode chill      # Casual chat
/mode creative   # Storytelling
/mode default    # Standard tsundere
```

### View Conversation History
```powershell
python view_history.py
```

---

## ⚙️ Configuration

### LLM Server
Edit `backend/app/llm_client.py`:
```python
LLM_API_URL = "http://127.0.0.1:8080/v1/chat/completions"
MODEL_NAME = "llama-3.2-3b-instruct"
```

### Voice Settings
Edit `voice/voice_config.py`:
```python
SELECTED_VOICE = "ja-JP-NanamiNeural"  # Change voice
SPEECH_RATE = "+15%"                    # Adjust speed
PITCH_SHIFT = "+5Hz"                    # Adjust pitch
```

### System Prompt
Edit `backend/app/prompt.py` to customize personality

---

## 🛠️ Manual Installation

If startup scripts don't work:

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
pip install -r requirements.txt
python main.py
```

### Voice
```powershell
cd voice
pip install -r requirements.txt
python text_chat_v2.py
```

### Vision
```powershell
cd vision
pip install -r requirements.txt
python vision_client.py
```

---

## 📚 Documentation

- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Command cheat sheet
- [CODEBASE_STRUCTURE.md](CODEBASE_STRUCTURE.md) - Complete file structure
- [DEVELOPMENT.md](DEVELOPMENT.md) - Developer guide
- [Backend README](backend/README.md) - API & memory system
- [Overlay README](overlay/README.md) - Avatar animations
- [Voice README](voice/README.md) - TTS/STT & RVC
- [Vision README](vision/README.md) - Presence detection

---

## 🔧 Requirements

- Python 3.10+
- Windows 10/11
- 4GB RAM minimum (8GB+ recommended)
- GPU recommended (for voice & vision)
- Webcam (for vision features)
- Microphone (for voice chat)

---

## 🐛 Troubleshooting

**Backend not starting:**
- Check if port 8000 is available
- Verify LLM server is running on port 8080

**Overlay not showing:**
- Check if images exist in `overlay/assets/`
- Windows 10/11 required for transparency

**Voice not working:**
- Check microphone permissions
- Test with: `python -c "import sounddevice; print(sounddevice.query_devices())"`

**Vision not working:**
- Check webcam permissions
- Verify OpenCV installation

---

## 📄 License

MIT License - See LICENSE file

---

## 🙏 Credits

- LLM: llama.cpp
- Voice: Edge TTS, Faster Whisper
- RVC: Retrieval-based Voice Conversion
- Vision: OpenCV, MediaPipe

---

**Made with ❤️ for Alisa**
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

## � Conversation History

Alisa remembers your conversations across restarts!

**View recent conversations:**
```powershell
python view_history.py
```

**View more messages:**
```powershell
python view_history.py -n 50
```

**Clear history:**
```powershell
python view_history.py --clear
```

**Check memory usage:**
```powershell
curl http://127.0.0.1:8000/history/summary
```

📖 **Full documentation:** [CONVERSATION_HISTORY.md](CONVERSATION_HISTORY.md)

---

## �📄 License

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
