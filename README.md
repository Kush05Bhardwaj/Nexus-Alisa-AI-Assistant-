# Alisa - Intelligent AI Desktop Companion

**Your adaptive AI assistant with personality, presence awareness, and desktop integration.**

![Status](https://img.shields.io/badge/status-production-success)
![Python](https://img.shields.io/badge/python-3.10+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Documentation](https://img.shields.io/badge/docs-comprehensive-brightgreen)

**Version:** 3.0

---

## 🎯 What is Alisa?

Alisa is a **fully local AI companion** that combines an animated avatar, natural voice conversation, presence detection, and intelligent desktop integration. Everything runs on your machine - your conversations and data stay private.

**Key Features:**
- 🎭 Animated avatar with emotional expressions
- 🗣️ Voice input/output with multiple languages
- 👁️ Webcam presence detection and attention tracking
- 🖥️ Desktop understanding (knows what you're working on)
- 🎮 Safe desktop automation (app control, browser, keyboard/mouse)
- 🧠 Adaptive learning (remembers your habits and preferences)
- 🌙 Idle companion mode (thoughtful presence during breaks)

---

## ✨ Core Features

### 🎭 Visual & Voice
- **Animated Avatar** - 6 emotions, blinking, talking animations ([details](overlay/README.md))
- **Voice I/O** - Edge TTS (40+ voices), Faster Whisper STT, optional RVC ([details](voice/README.md))
- **Emotion System** - Expression changes based on conversation context

### 👁️ Vision & Context
- **Presence Detection** - Face tracking, attention monitoring ([details](vision/README.md))
- **Phase 10A: Desktop Understanding** - App/file/task detection, error detection ([docs](docs/PHASE_10A_GETTING_STARTED.md))
- **Smart Help** - Context-aware assistance with 5-minute cooldown

### 🎮 Automation & Learning
- **Phase 10B: Desktop Actions** - App control, browser automation, safe commands ([docs](docs/PHASE_10B_GETTING_STARTED.md))
- **Phase 10C: Habit Learning** - Work schedule, app patterns, adaptive behavior ([docs](docs/PHASE_10C_GETTING_STARTED.md))
- **Safety First** - Whitelists, blacklists, rate limits, confirmation prompts

### 🧠 Intelligence
- **Memory System** - Short-term buffer + persistent SQLite storage ([details](backend/README.md))
- **Idle Companion** - Spontaneous thoughts during breaks ([guide](docs/IDLE_THOUGHT_GUIDE.md))
- **Conversation Modes** - Teasing, calm, serious personalities

> � **[Complete Architecture Documentation](docs/SYSTEM_ARCHITECTURE.md)** | **[File-by-File Guide](docs/CODEBASE_STRUCTURE.md)**

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Windows 10/11
- Local LLM server (llama.cpp recommended)
- Optional: Webcam, Microphone, GPU

### Installation (2 Minutes)

**1. Clone Repository**
```powershell
git clone https://github.com/Kush05Bhardwaj/Nexus-Alisa-AI-Assistant-.git
cd "Alisa-AI Assistant"
```

**2. Start LLM Server** (separate terminal)
```powershell
# Example with llama.cpp
.\llama-server.exe -m .\models\Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf -c 4096 -ngl 33
```

**3. Launch Alisa**
```powershell
# One command starts everything (backend, overlay, vision, chat)
.\scripts\start_phase10c.ps1
```

**Done!** 🎉 Alisa is ready.

### Alternative Setups

```powershell
# Minimal (text only)
.\scripts\start_backend.ps1    # Terminal 1
.\scripts\start_text_chat.ps1  # Terminal 2

# Voice conversation
.\scripts\start_backend.ps1    # Terminal 1
.\scripts\start_voice.ps1      # Terminal 2

# Custom combinations
.\scripts\start_overlay.ps1    # Add avatar
.\scripts\start_vision.ps1     # Add presence detection
```

**📖 [Complete Setup Guide](scripts/README.md)** | **[Troubleshooting](scripts/README.md#-troubleshooting)**

### Manual Setup (No Scripts)

For complete control, start each component manually:

```powershell
# Terminal 1: LLM Server
cd F:\llama
.\llama-server.exe `
  -m .\models\Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf `
  -c 4096 `
  -ngl 33 `
  --split-mode layer

# Terminal 2: Backend
cd F:\Projects\Alisa\Alisa-AI Assistant\backend
.\venv\Scripts\Activate.ps1
cd ..
uvicorn backend.app.main:app --reload

# Terminal 3: Overlay (Avatar)
cd F:\Projects\Alisa\Alisa-AI Assistant\overlay
.\venv\Scripts\Activate.ps1
python main.py

# Terminal 4: Webcam Vision
cd F:\Projects\Alisa\Alisa-AI Assistant\vision
.\venv\Scripts\Activate.ps1
python vision_client.py

# Terminal 5: Desktop Understanding (Screen Vision)
cd F:\Projects\Alisa\Alisa-AI Assistant\vision
.\venv\Scripts\Activate.ps1
python vision_client_screen.py

# Terminal 6: Voice Chat
cd F:\Projects\Alisa\Alisa-AI Assistant\voice
.\venv\Scripts\Activate.ps1
python voice_chat_optimized.py

# Terminal 7: Text Chat (Alternative to voice)
cd F:\Projects\Alisa\Alisa-AI Assistant\voice
.\venv\Scripts\Activate.ps1
python text_chat.py
```

**Note:** Start terminals in order. Backend must be running before starting other components.

---

## 📁 Project Structure

```
Alisa-AI-Assistant/
├── backend/          # FastAPI server, LLM integration, all Phase features
├── overlay/          # Animated avatar window (Tkinter)
├── voice/            # Voice I/O (Edge TTS, Faster Whisper, RVC)
├── vision/           # Presence detection, desktop understanding
├── scripts/          # PowerShell startup scripts & utilities
└── docs/             # Complete documentation (12,400+ lines)
```

---

## ⚙️ Configuration

### Change Voice
```python
# voice/voice_config.py
SELECTED_VOICE = "nanami"  # Japanese anime-style
SPEECH_RATE = "+20%"
PITCH_SHIFT = "+15Hz"
```

### Customize Personality
```python
# backend/app/prompt.py
SYSTEM_PROMPT = """Your name is Alisa..."""
```

### Adjust Performance
```python
# vision/vision_config.py
apply_preset("ultra_light")  # Low CPU
apply_preset("enhanced")     # Better accuracy
```

### Add Custom Apps
```python
# backend/app/desktop_actions.py
app_paths = {
    "myapp": "C:\\Path\\To\\App.exe"
}
```

---

## 📚 Complete Documentation

### 📖 Module Documentation (Comprehensive READMEs)

Each module has detailed documentation covering setup, API, features, and troubleshooting:

| Module | Documentation | Lines | Coverage |
|--------|--------------|-------|----------|
| **Backend** | [backend/README.md](backend/README.md) |
| **Overlay** | [overlay/README.md](overlay/README.md) |
| **Voice** | [voice/README.md](voice/README.md) |
| **Vision** | [vision/README.md](vision/README.md) |
| **Scripts** | [scripts/README.md](scripts/README.md) |

### 🏗️ Architecture & Structure

- **[SYSTEM_ARCHITECTURE.md](docs/SYSTEM_ARCHITECTURE.md)** 
  - Complete system architecture
  - 4-layer design (Presentation, Communication, Core Logic, Data)
  - Data flow diagrams
  - Component interactions
  - Technology stack breakdown
  - Deployment architecture
  - Performance characteristics
  - Security model

- **[CODEBASE_STRUCTURE.md](docs/CODEBASE_STRUCTURE.md)** 
  - File-by-file documentation (all 67 files)
  - Purpose, key components, dependencies
  - Lines of code statistics
  - Quick lookup tables
  - Import patterns and conventions

---

## 🔧 System Requirements

### Minimum Requirements
- **OS:** Windows 10/11 (64-bit)
- **Python:** 3.10 or higher
- **RAM:** 4GB (backend + LLM)
- **Storage:** 2GB (models + dependencies)
- **CPU:** 4 cores (for concurrent processing)

### Recommended Configuration
- **OS:** Windows 11
- **Python:** 3.11
- **RAM:** 8GB+ (for smooth operation)
- **Storage:** 10GB+ (multiple models)
- **CPU:** 6+ cores
- **GPU:** NVIDIA GPU with CUDA (for faster LLM inference)
- **Webcam:** 720p or higher
- **Microphone:** Any USB/built-in microphone

### Optional Components
- **Tesseract OCR** - For screen text extraction
- **CUDA Toolkit** - For GPU acceleration
- **RVC Models** - For custom voice conversion

---

## 🎯 Feature Roadmap

### ✅ Completed (Phase 10C)
- [x] Core chat functionality with LLM streaming
- [x] Animated avatar overlay (6 emotions)
- [x] Voice output (Edge TTS) and input (Faster Whisper)
- [x] Emotion detection and expression system
- [x] Conversation modes (teasing, calm, serious)
- [x] Memory system (short & long-term SQLite)
- [x] Idle companion system
- [x] Desktop understanding
  - [x] Application detection
  - [x] File type recognition
  - [x] Task inference
  - [x] Error detection
  - [x] Smart help offers
- [x] Desktop actions
  - [x] App management
  - [x] Browser control
  - [x] Keyboard/mouse automation
  - [x] File operations
  - [x] Safety system (whitelist, blacklist, rate limits)
- [x] Task memory & habit learning
  - [x] Work schedule detection
  - [x] App usage pattern tracking
  - [x] Silence preference learning
  - [x] Repeated task recognition
  - [x] Adaptive behavior

### 🚧 In Progress
- [ ] Settings UI panel (web-based dashboard)
- [ ] System tray integration
- [ ] Multi-language support enhancements

### 📅 Planned Features
- [ ] Emotional Intelligence
  - [ ] Advanced emotion detection from text
  - [ ] Context-aware emotional responses
  - [ ] Emotional state tracking over time
  - [ ] Mood-based interaction patterns

- [ ] Creative Assistance
  - [ ] Code generation and refactoring
  - [ ] Writing assistance and editing
  - [ ] Brainstorming and idea generation
  - [ ] Project planning and task breakdown

- [ ] Multi-Modal Learning
  - [ ] Document analysis and summarization
  - [ ] Image understanding and description
  - [ ] Video content analysis
  - [ ] Multi-document synthesis

### 🌟 Future Enhancements
- [ ] Multiple avatar themes and character designs
- [ ] Plugin system for community extensions
- [ ] Cross-platform support (Linux, macOS)
- [ ] Mobile companion app (Android/iOS)
- [ ] Voice activity detection (no push-to-talk)
- [ ] Advanced RVC voice training pipeline
- [ ] Multi-user support with profiles
- [ ] Cloud sync for settings (optional)
- [ ] Integration with productivity tools (calendar, todo lists)
- [ ] Advanced context awareness (git status, running processes)

---

## 🤝 Contributing

**We welcome contributions!** Areas where you can help:

### 🎨 Creative Contributions
- New avatar expressions and themes
- Voice model training and sharing
- Personality preset configurations
- User interface improvements

### 💻 Technical Contributions
- Performance optimizations
- Bug fixes and stability improvements
- New conversation modes
- Platform support (Linux, macOS)
- Plugin system development

### 📚 Documentation
- Tutorial videos and guides
- Translation to other languages
- Usage examples and case studies
- API documentation improvements

### 🧪 Testing & QA
- Bug reporting with detailed steps
- Feature testing on different systems
- Performance benchmarking
- User experience feedback

### How to Contribute

1. **Fork the repository**
```bash
git clone https://github.com/YOUR_USERNAME/Nexus-Alisa-AI-Assistant-.git
cd "Alisa-AI Assistant"
```

2. **Create a feature branch**
```bash
git checkout -b feature/AmazingFeature
```

3. **Make your changes**
   - Follow code style guidelines (see DEVELOPMENT.md)
   - Add tests if applicable
   - Update documentation

4. **Commit your changes**
```bash
git commit -m 'Add some AmazingFeature'
```

5. **Push to your fork**
```bash
git push origin feature/AmazingFeature
```

6. **Open a Pull Request**
   - Describe your changes clearly
   - Reference any related issues
   - Include screenshots/videos if UI changes

### Commit Message Convention
```
<type>: <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

---

## 📄 License

**MIT License** - see [LICENSE](LICENSE) file for details.

### What this means:
- ✅ Commercial use allowed
- ✅ Modification allowed
- ✅ Distribution allowed
- ✅ Private use allowed
- ℹ️ License and copyright notice must be included
- ⚠️ No warranty provided

---

## 🙏 Acknowledgments & Credits

### Technology Stack
- **LLM Integration:** [llama.cpp](https://github.com/ggerganov/llama.cpp) - Fast CPU/GPU inference
- **Voice Synthesis:** [Microsoft Edge TTS](https://github.com/rany2/edge-tts) - High-quality text-to-speech
- **Speech Recognition:** [faster-whisper](https://github.com/guillaumekln/faster-whisper) - Optimized Whisper implementation
- **Voice Conversion:** [RVC](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI) - Real-time voice conversion
- **Computer Vision:** [OpenCV](https://opencv.org/) - Image processing and face detection
- **Web Framework:** [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- **Database:** [SQLAlchemy](https://www.sqlalchemy.org/) - SQL toolkit and ORM

### Inspiration
- **VTuber Culture** - Avatar animation and personality design
- **Anime Characters** - Tsundere personality archetype
- **AI Assistants** - Siri, Alexa, Google Assistant concepts
- **Desktop Companions** - Clippy (but actually helpful!)

### Special Thanks
- Open source community for amazing tools
- Beta testers for valuable feedback
- Contributors for improvements and bug fixes

---

## 📞 Support & Community

### Getting Help

**Documentation First:**
- Check the [docs/](docs/) folder for detailed guides
- Read module-specific READMEs for troubleshooting

**GitHub Issues:**
- Report bugs: [GitHub Issues](https://github.com/Kush05Bhardwaj/Nexus-Alisa-AI-Assistant-/issues)
- Request features: Use "enhancement" label
- Ask questions: Use "question" label

**When Reporting Issues:**
Please include:
1. Your system specs (OS, Python version, RAM, GPU)
2. Steps to reproduce the problem
3. Error messages (full traceback)
4. Relevant logs from terminal
5. What you've already tried

---

## 🛠️ Troubleshooting

**Common issues:**
- **Port 8000 in use** → `netstat -ano | findstr :8000` then kill process
- **LLM not connecting** → Verify `http://127.0.0.1:8080/health` responds
- **Webcam not found** → Check device manager, close other camera apps
- **High CPU usage** → Switch to `ultra_light` vision preset
- **Module not found** → Ensure venv is activated, reinstall requirements

### Useful Commands for Troubleshooting

**Check system status:**
```powershell
# Python version
python --version

# Check if backend is running
Invoke-WebRequest -Uri "http://127.0.0.1:8000/"

# Check if LLM is running
Invoke-WebRequest -Uri "http://127.0.0.1:8080/health"

# List audio devices
python -c "import sounddevice; print(sounddevice.query_devices())"

# Test webcam
python -c "import cv2; cap = cv2.VideoCapture(0); print('Webcam:', cap.isOpened())"
```

**View logs:**
```powershell
# Backend logs (check terminal running start_backend.ps1)
# Look for errors in red text

# Database inspection
python .\scripts\view_history.py
```

---

## 🌟 Project Status

**Current Version:** 3.0  
**Stability:** Production Ready  
**Last Updated:** January 17, 2026

### Version History

**v3.0 (January 2026)**
- Task memory and habit learning system
- Adaptive behavioral adjustments
- Work schedule detection
- Complete documentation (12,400+ lines)
- System architecture documentation
- Codebase structure documentation

**v2.5 (January 2026)**
- Desktop actions and automation
- Safety system implementation
- Permission-based execution

**v2.0 (January 2026)**
- Desktop understanding system
- Screen analysis and OCR
- Context-aware assistance

**v1.5 (December 2025)**
- Idle companion system
- Spontaneous behavior
- Presence awareness

**v1.0 (December 2025) - Core Release**
- Basic chat functionality
- Avatar overlay
- Voice I/O
- Emotion system

---

**Made with ❤️ by [Kushagra Bhardwaj](https://github.com/Kush05Bhardwaj)**

**Repository:** [Nexus-Alisa-AI-Assistant-](https://github.com/Kush05Bhardwaj/Nexus-Alisa-AI-Assistant-)

---

*Alisa is more than just an AI assistant - she's your companion, understanding your work, adapting to your habits, and growing with you over time. Welcome to the future of personal AI assistance!* 💙
