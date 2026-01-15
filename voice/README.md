# 🎙️ Voice Module - Alisa Assistant

Voice input/output capabilities for Alisa Assistant with RVC voice conversion.

## 📁 Structure

```
voice/
├── voice_chat.py           # Main voice chat loop
├── voice_input.py          # Speech-to-text (Whisper)
├── voice_output.py         # Text-to-speech (pyttsx3)
├── voice_output_rvc.py     # TTS with RVC voice conversion
├── rvc/                    # RVC (Retrieval-based Voice Conversion)
│   ├── inferencer.py       # RVC inference engine
│   ├── weights/            # Voice model weights
│   └── index/              # Voice index files
└── requirements.txt        # Voice dependencies
```

## 🚀 Setup

### 1. Install Dependencies

```powershell
cd voice
pip install -r requirements.txt
```

### 2. Additional Requirements

**For GPU acceleration (recommended):**
```powershell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**For faster-whisper CUDA support:**
```powershell
pip install nvidia-cublas-cu11
pip install nvidia-cudnn-cu11
```

## 🎮 Usage

### Basic Voice Chat

```python
from voice_chat import voice_chat
import asyncio

asyncio.run(voice_chat())
```

### Voice Input Only

```python
from voice_input import record_audio, speech_to_text

record_audio()
text = speech_to_text()
print(f"You said: {text}")
```

### Voice Output (Basic)

```python
from voice_output import speak

speak("Hello, I am Alisa!")
```

### Voice Output (RVC Enhanced)

```python
from voice_output_rvc import speak

speak("Hello with Alisa's voice!")
```

## 🔧 Configuration

### Voice Input Settings

Edit `voice_input.py`:
```python
SAMPLE_RATE = 16000  # Audio sample rate
DURATION = 5         # Recording duration (seconds)

# Whisper model size: tiny, base, small, medium, large
model = WhisperModel("small", device="cuda", compute_type="float16")
```

### Voice Output Settings

Edit `voice_output.py`:
```python
engine.setProperty("rate", 170)  # Speech rate
```

Edit `voice_output_rvc.py`:
```python
VOICE = "en-US-JennyNeural"  # Edge-TTS voice
```

## 🎯 Features

### ✅ Implemented
- Speech-to-text using Faster Whisper
- Text-to-speech using pyttsx3
- Text-to-speech using Edge-TTS
- RVC voice conversion for custom voice
- Voice chat loop with WebSocket backend

### 🚧 Planned
- Voice activity detection (VAD)
- Interrupt handling
- Background noise reduction
- Multiple voice profiles

## 🔊 RVC (Voice Conversion)

The RVC module converts generated speech to a custom voice character.

### How it works:
1. Generate base speech with Edge-TTS (`base.wav`)
2. Convert to custom voice with RVC (`alisa.wav`)
3. Play converted audio

### Adding Custom Voice:
1. Place your RVC model in `rvc/weights/`
2. Place index files in `rvc/index/`
3. Update `rvc/inferencer.py` with model paths

## 🐛 Troubleshooting

**"Could not find CUDA" error**
- Install CUDA toolkit or use CPU mode
- Change `device="cuda"` to `device="cpu"` in voice_input.py

**"No audio input device found"**
- Check microphone is connected
- Run `python -m sounddevice` to list devices

**"RVC conversion failed"**
- Check model files exist in `rvc/weights/` and `rvc/index/`
- Verify model compatibility

**Poor speech recognition**
- Increase DURATION in voice_input.py
- Use larger Whisper model (medium/large)
- Reduce background noise

## 📝 Dependencies

| Package | Purpose |
|---------|---------|
| `edge-tts` | Text-to-speech API |
| `soundfile` | Audio file I/O |
| `librosa` | Audio processing |
| `numpy` | Numerical operations |
| `sounddevice` | Audio recording |
| `scipy` | Signal processing |
| `faster-whisper` | Speech-to-text |
| `pyttsx3` | Offline TTS |
| `simpleaudio` | Audio playback |

## 🎤 Voice Chat Flow

```
User speaks → Record Audio → Whisper (STT) → WebSocket → Backend LLM
                                                              ↓
User hears ← Play Audio ← RVC Convert ← Edge-TTS (TTS) ← Response
```

---

Made with ❤️ for Alisa Assistant
