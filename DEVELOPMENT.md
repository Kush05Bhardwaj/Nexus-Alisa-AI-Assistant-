# 🚀 Development Guide - Alisa Assistant

Guide for developers contributing to or extending Alisa Assistant.

## 📋 Project Architecture

Alisa is built with a modular architecture:
- **Backend** - FastAPI WebSocket server
- **Overlay** - Tkinter desktop application
- **Voice** - Audio I/O system
- **Vision** - Computer vision system

All components communicate via WebSocket.

## 🛠️ Development Setup

### Prerequisites
- Python 3.10+
- Git
- Windows 10/11
- NVIDIA GPU (optional, for faster processing)

### Clone & Setup
```powershell
git clone https://github.com/Kush05Bhardwaj/Nexus-Alisa-AI-Assistant-.git
cd NexaAssistant
```

### Install Each Component
```powershell
# Backend
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
cd ..

# Overlay
cd overlay
pip install -r requirements.txt
cd ..

# Voice
cd voice
pip install -r requirements.txt
cd ..

# Vision
cd vision
pip install -r requirements.txt
cd ..
```

## 🧪 Testing

### Test Backend
```powershell
cd backend
pytest
# Or manual test
uvicorn app.main:app --reload
# Visit http://127.0.0.1:8000
```

### Test Overlay
```powershell
cd overlay
python test_animations.py
python check_images.py
```

### Test Voice
```powershell
cd voice
python -c "from voice_output_edge import speak; speak('Test')"
```

### Test Vision
```powershell
cd vision
python webcam.py
```

## 📝 Code Style

### Python Style
- Follow PEP 8
- Use type hints
- Document functions with docstrings
- Keep functions focused and small

### File Organization
```python
# Imports
import standard_library
import third_party
from local_module import something

# Constants
CONSTANT_VALUE = 42

# Classes
class MyClass:
    pass

# Functions
def my_function():
    pass

# Main execution
if __name__ == "__main__":
    main()
```

## 🔌 Adding Features

### Add New Emotion
1. Create image: `overlay/assets/newemotion.png`
2. Update `backend/app/emotion.py`:
```python
ALLOWED_EMOTIONS = [..., "newemotion"]
```
3. Update `overlay/avatar_controller.py`:
```python
self.emotions = {..., "newemotion": "newemotion.png"}
```

### Add New Conversation Mode
Edit `backend/app/modes.py`:
```python
MODES = {
    "newmode": {
        "name": "New Mode",
        "description": "Description",
        "system_prompt_addition": "Additional instructions"
    }
}
```

### Add New Voice
Edit `voice/voice_config.py`:
```python
VOICE_OPTIONS = {
    "newvoice": "language-CountryCode-VoiceNameNeural"
}
```

## 🎨 Customization

### Change Personality
Edit `backend/app/prompt.py`:
```python
SYSTEM_PROMPT = """
Your custom personality here...
"""
```

### Adjust Animation Timing
Edit `overlay/avatar_controller.py`:
```python
BLINK_INTERVAL = (2000, 5000)  # ms
TALK_TOGGLE_INTERVAL = 150      # ms
```

### Voice Settings
Edit `voice/voice_config.py`:
```python
SPEECH_RATE = "+20%"
PITCH_SHIFT = "+10Hz"
```

## 🐛 Debugging

### Enable Debug Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### WebSocket Debugging
```powershell
# Install wscat
npm install -g wscat

# Connect to backend
wscat -c ws://127.0.0.1:8000/ws/chat

# Send test message
> {"message": "Hello"}
```

### Database Inspection
```powershell
python view_history.py
```

Or use SQLite browser:
```powershell
sqlite3 alisa_memory.db
> SELECT * FROM messages;
```

## 📦 Dependencies Management

### Update Dependencies
```powershell
cd backend
pip freeze > requirements.txt

cd ../overlay
pip freeze > requirements.txt

# etc...
```

### Add New Dependency
```powershell
pip install new-package
pip freeze > requirements.txt
```

## 🚀 Building & Deployment

### Create Standalone Executable
Using PyInstaller:
```powershell
pip install pyinstaller

# Backend
cd backend
pyinstaller --onefile app/main.py

# Overlay
cd overlay
pyinstaller --onefile --windowed main.py
```

### Docker (Future)
```dockerfile
# Example Dockerfile for backend
FROM python:3.10
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
```

## 🔄 Git Workflow

### Branch Strategy
- `master` - Stable releases
- `develop` - Development branch
- `feature/feature-name` - Feature branches
- `fix/bug-name` - Bug fix branches

### Commit Messages
```
feat: Add new emotion detection
fix: Fix overlay transparency issue
docs: Update README
refactor: Improve memory management
test: Add voice output tests
```

### Pull Request Process
1. Fork repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit PR with description

## 📊 Performance Optimization

### Backend
- Use async/await for I/O operations
- Cache frequently accessed data
- Optimize database queries
- Use connection pooling

### Overlay
- Minimize image reloading
- Use image caching
- Optimize animation frame rate

### Voice
- Use smaller Whisper models for speed
- Cache TTS output when possible
- Process audio in chunks

### Vision
- Reduce frame processing rate
- Use smaller image resolutions
- Skip frames when appropriate

## 🔒 Security

### Best Practices
- Never commit API keys or secrets
- Use environment variables for config
- Validate all user input
- Sanitize file paths
- Keep dependencies updated

### Environment Variables
Create `.env` file:
```
LLM_API_URL=http://127.0.0.1:8080
DATABASE_PATH=./alisa_memory.db
```

Load in code:
```python
from dotenv import load_dotenv
import os

load_dotenv()
api_url = os.getenv("LLM_API_URL")
```

## 📚 Documentation

### Update Documentation When:
- Adding new features
- Changing APIs
- Fixing bugs
- Modifying configuration

### Documentation Files
- `README.md` - Overview & quick start
- `CODEBASE_STRUCTURE.md` - File structure
- Module READMEs - Component details
- Code comments - Implementation details

## 🤝 Contributing Guidelines

### Code Review Checklist
- [ ] Code follows style guide
- [ ] Tests pass
- [ ] Documentation updated
- [ ] No unnecessary files
- [ ] Backwards compatible
- [ ] Performance tested

### Questions?
- Open an issue on GitHub
- Check existing documentation
- Review code comments

## 📞 Contact

- GitHub: [@Kush05Bhardwaj](https://github.com/Kush05Bhardwaj)
- Repository: [Nexus-Alisa-AI-Assistant](https://github.com/Kush05Bhardwaj/Nexus-Alisa-AI-Assistant-)

---

**Happy Coding! 🎉**
