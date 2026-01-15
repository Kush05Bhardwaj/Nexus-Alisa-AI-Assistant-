# 🎙️ Voice - Alisa Assistant

Voice input/output system with speech recognition, text-to-speech, and optional RVC voice conversion.

## 📋 Overview

The voice module provides:
- Speech-to-text (STT) using Faster Whisper
- Text-to-speech (TTS) with Edge TTS
- Optional RVC voice conversion for anime-style voice
- Audio-synced overlay animations
- Multiple chat interfaces (text input + voice output, full voice chat)

## 🚀 Quick Start

### Install Dependencies
```powershell
cd voice
pip install -r requirements.txt
```

### Optional: GPU Acceleration
For faster processing with NVIDIA GPU:
```powershell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### Start Voice Chat
```powershell
# Text input with voice output
python text_chat_v2.py

# Full voice conversation
python voice_chat_optimized.py
```

Or use startup scripts from project root:
```powershell
.\start_text_chat.ps1    # Text + voice
.\start_voice.ps1        # Full voice
```

## 📁 Structure

```
voice/
├── text_chat_v2.py              # Text input + voice output
├── voice_chat_optimized.py      # Full voice conversation
├── voice_input.py               # Speech-to-text
├── voice_output_edge.py         # Edge TTS (recommended)
├── voice_output_rvc.py          # Edge TTS + RVC conversion
├── voice_config.py              # Voice settings
├── rvc/                         # RVC voice conversion
│   ├── inferencer.py            # RVC inference engine
│   ├── weights/                 # Model weights (.pth)
│   └── index/                   # Feature index (.index)
└── requirements.txt
```

## 🎤 Speech-to-Text (STT)

### Using Faster Whisper
```python
from voice_input import record_audio, speech_to_text

# Record from microphone
record_audio()

# Convert to text
text = speech_to_text()
print(f"You said: {text}")
```

### Configuration
Edit `voice_input.py`:
```python
SAMPLE_RATE = 16000              # Audio sample rate
CHANNELS = 1                     # Mono audio
CHUNK_SIZE = 1024                # Buffer size

# Whisper model: tiny, base, small, medium, large
# Smaller = faster, less accurate
# Larger = slower, more accurate
MODEL_SIZE = "small"
DEVICE = "cuda"                  # or "cpu"
COMPUTE_TYPE = "float16"         # or "int8" for CPU
```

### Models & Performance
| Model  | Speed | Accuracy | VRAM  |
|--------|-------|----------|-------|
| tiny   | ⚡⚡⚡  | ⭐       | ~1GB  |
| base   | ⚡⚡   | ⭐⭐     | ~1GB  |
| small  | ⚡     | ⭐⭐⭐   | ~2GB  |
| medium | 🐌    | ⭐⭐⭐⭐ | ~5GB  |
| large  | 🐌🐌  | ⭐⭐⭐⭐⭐| ~10GB |

## 🔊 Text-to-Speech (TTS)

### Using Edge TTS (Recommended)
```python
from voice_output_edge import speak

speak("Hello, I am Alisa!")
```

### Available Voices
Edit `voice_config.py`:
```python
# Current selection
SELECTED_VOICE = "ja-JP-NanamiNeural"

# Available options:
VOICE_OPTIONS = {
    "nanami": "ja-JP-NanamiNeural",      # Japanese female (recommended)
    "ayaka": "ja-JP-AoiNeural",          # Japanese female
    "naoki": "ja-JP-KeitaNeural",        # Japanese male
    "xiaoxiao": "zh-CN-XiaoxiaoNeural",  # Chinese female
    "jenny": "en-US-JennyNeural",        # English female
    "aria": "en-US-AriaNeural",          # English female
}
```

### Voice Customization
Edit `voice_config.py`:
```python
SPEECH_RATE = "+15%"     # Speed: -50% to +100%
PITCH_SHIFT = "+5Hz"     # Pitch: -50Hz to +50Hz
VOLUME = "+0%"           # Volume: -50% to +50%
```

### Test Voices
```powershell
python -c "from voice_output_edge import test_all_voices; test_all_voices()"
```

## 🎨 RVC Voice Conversion (Optional)

### What is RVC?
RVC (Retrieval-based Voice Conversion) transforms Edge TTS output to sound like your custom voice model.

### Setup RVC
1. Place model files in `rvc/`:
   - `weights/alisa.pth` - Model weights
   - `index/alisa.index` - Feature index

2. Use RVC voice output:
```python
from voice_output_rvc import speak

speak("Hello with Alisa's custom voice!")
```

### RVC Configuration
Edit `voice_output_rvc.py`:
```python
MODEL_PATH = "rvc/weights/alisa.pth"
INDEX_PATH = "rvc/index/alisa.index"
PITCH_SHIFT = 0          # Semitones: -12 to +12
INDEX_RATE = 0.75        # Feature matching: 0.0 to 1.0
PROTECT_RATE = 0.33      # Breath protection: 0.0 to 0.5
```

### Training Your Own RVC Model
See: [RVC Training Guide](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI)

## 💬 Chat Interfaces

### Text Chat with Voice Output
```powershell
python text_chat_v2.py
```
- Type messages in terminal
- Hear Alisa's voice responses
- See avatar animations (if overlay running)

### Full Voice Conversation
```powershell
python voice_chat_optimized.py
```
- Speak to Alisa (push-to-talk or voice activation)
- Get voice responses
- Natural conversation flow

## ⚙️ Advanced Configuration

### Microphone Selection
Edit `voice_input.py`:
```python
# List available devices
import sounddevice as sd
print(sd.query_devices())

# Select device by index
DEVICE_INDEX = 0  # Change to your microphone
```

### Audio Quality
```python
# STT Quality
SAMPLE_RATE = 16000      # Standard for Whisper

# TTS Quality
# Edge TTS automatically uses high quality
```

### Silence Detection
Edit `voice_input.py`:
```python
SILENCE_THRESHOLD = 500   # Lower = more sensitive
SILENCE_DURATION = 2.0    # Seconds of silence before stopping
```

## 🔧 Dependencies

Key packages:
- `faster-whisper` - Speech recognition
- `edge-tts` - Text-to-speech
- `sounddevice` - Audio I/O
- `soundfile` - Audio file handling
- `websockets` - Backend communication
- `fairseq` - RVC inference (optional)
- `pyworld` - Audio processing (optional)

## 🛠️ Troubleshooting

**Microphone not working:**
- Check device permissions
- List devices: `python -c "import sounddevice; print(sounddevice.query_devices())"`
- Update `DEVICE_INDEX` in `voice_input.py`

**TTS not working:**
- Check internet connection (Edge TTS requires online)
- Try different voice in `voice_config.py`

**RVC errors:**
- Ensure model files exist in `rvc/weights/` and `rvc/index/`
- Check PyTorch installation
- Verify CUDA for GPU support

**Poor voice quality:**
- Increase Whisper model size (small → medium)
- Adjust microphone gain
- Reduce background noise

**Slow performance:**
- Use smaller Whisper model (medium → small)
- Use CPU instead of GPU if VRAM limited
- Disable RVC if not needed

## 📊 Performance Tips

**Fast Response:**
- Use `tiny` or `base` Whisper model
- Use Edge TTS without RVC
- Use GPU if available

**High Quality:**
- Use `medium` or `large` Whisper model
- Enable RVC voice conversion
- Adjust `INDEX_RATE` for better voice match

**Low Resource:**
- Use `tiny` Whisper with CPU
- Disable RVC
- Use `int8` compute type
