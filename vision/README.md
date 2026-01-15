# 👁️ Vision - Alisa Assistant

Vision system for presence detection, attention tracking, and screen analysis.

## 📋 Overview

The vision module provides:
- **Webcam-based presence detection** - Knows when you're there
- **Attention tracking** - Detects if you're looking at screen
- **Face emotion estimation** - Recognizes your emotional state
- **Screen content analysis** - Understands what you're working on
- **Privacy-first** - All processing local, no cloud uploads

## 🚀 Quick Start

### Install Dependencies
```powershell
cd vision
pip install -r requirements.txt
```

### Start Vision System

**Webcam mode (presence + attention):**
```powershell
python vision_client.py
```

**Screen analysis mode:**
```powershell
python vision_client_screen.py
```

Or use startup scripts from project root:
```powershell
.\start_vision.ps1          # Webcam mode
.\start_vision_screen.ps1   # Screen analysis mode
```

## 📁 Structure

```
vision/
├── vision_client.py         # Webcam presence detection
├── vision_client_screen.py  # Screen content analysis
├── webcam.py                # Webcam capture & processing
├── face_emotion.py          # Face detection & emotion
├── screen_capture.py        # Screenshot capture
├── screen_analyze.py        # Screen content analysis
└── requirements.txt
```

## 👤 Presence Detection

### How It Works
1. Captures webcam frames
2. Detects faces using Haar Cascades
3. Estimates attention (looking at screen vs away)
4. Sends presence updates to backend
5. Backend adjusts Alisa's behavior accordingly

### Using Vision Client
```python
from vision_client import main
import asyncio

asyncio.run(main())
```

### Presence States
- `present` - User detected, looking at screen
- `away` - User detected but looking away
- `absent` - No user detected

### Backend Integration
Vision data sent via WebSocket:
```json
{
  "type": "vision_update",
  "data": {
    "present": true,
    "attention": 0.85,
    "emotion": "neutral"
  }
}
```

## 😊 Emotion Detection

### Supported Emotions
- `neutral` - Default state
- `happy` - Smiling
- `sad` - Frowning
- `surprised` - Eyes wide
- `focused` - Concentrated

### How It Works
1. Detects face landmarks
2. Analyzes facial features
3. Estimates emotion (basic heuristics)
4. Ready for CNN model integration

### Using Emotion Detection
```python
from face_emotion import FaceEmotionDetector

detector = FaceEmotionDetector()
frame = capture_webcam_frame()
emotion = detector.detect_emotion(frame)
print(f"Detected emotion: {emotion}")
```

### Future: Deep Learning
Current system uses basic heuristics. Can be upgraded with:
- FER (Facial Expression Recognition) models
- Custom CNN trained on emotion datasets
- Real-time emotion tracking

## 🖥️ Screen Analysis

### How It Works
1. Captures periodic screenshots
2. Analyzes content using vision LLM
3. Understands context (coding, browsing, gaming, etc.)
4. Provides relevant assistance

### Using Screen Analysis
```python
from vision_client_screen import main
import asyncio

asyncio.run(main())
```

### Analysis Frequency
Edit `vision_client_screen.py`:
```python
ANALYSIS_INTERVAL = 30  # Seconds between screen captures
```

### Screen Context Detection
- Identifies active applications
- Recognizes code editors, browsers, documents
- Understands what you're working on
- Provides contextual assistance

## ⚙️ Configuration

### Webcam Settings
Edit `webcam.py`:
```python
CAMERA_INDEX = 0           # Webcam device index
FRAME_WIDTH = 640          # Capture width
FRAME_HEIGHT = 480         # Capture height
FPS = 30                   # Frames per second
```

### Face Detection Sensitivity
Edit `face_emotion.py`:
```python
SCALE_FACTOR = 1.1         # Detection scale (1.1 = balanced)
MIN_NEIGHBORS = 5          # Min detections (5 = balanced)
MIN_SIZE = (30, 30)        # Minimum face size
```

### Attention Threshold
Edit `webcam.py`:
```python
ATTENTION_THRESHOLD = 0.6  # 0.0 to 1.0 (0.6 = balanced)
```

### Backend Connection
Edit `vision_client.py`:
```python
BACKEND_WS_URL = "ws://127.0.0.1:8000/ws/chat"
UPDATE_INTERVAL = 2.0      # Seconds between updates
```

## 🔒 Privacy & Security

### Local Processing
- All vision processing happens locally
- No images sent to cloud services
- No data collection or storage

### Data Handling
- Webcam frames processed in-memory
- Not saved to disk (unless debugging)
- Minimal data sent to backend (presence/emotion only)

### Permissions
- Webcam access required (system permission)
- Screen capture access (Windows 10/11)
- No network access except local backend

## 🛠️ Advanced Usage

### Custom Emotion Models
To integrate custom CNN model:

1. Train model (TensorFlow/PyTorch)
2. Update `face_emotion.py`:
```python
class FaceEmotionDetector:
    def __init__(self):
        self.model = load_model("your_model.h5")
    
    def detect_emotion(self, frame):
        # Your model inference
        return emotion
```

### Multi-Camera Support
Edit `webcam.py`:
```python
# List available cameras
import cv2
for i in range(10):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"Camera {i} available")
    cap.release()

# Use specific camera
CAMERA_INDEX = 1  # Change to your camera
```

### Performance Optimization
```python
# Reduce resolution for faster processing
FRAME_WIDTH = 320
FRAME_HEIGHT = 240

# Lower FPS for less CPU usage
FPS = 15

# Skip frames for processing
PROCESS_EVERY_N_FRAMES = 3
```

## 🔧 Dependencies

Key packages:
- `opencv-python` - Computer vision
- `numpy` - Array processing
- `Pillow` - Image handling
- `websockets` - Backend communication
- `mss` - Screen capture (for screen analysis)

## 🐛 Troubleshooting

**Webcam not detected:**
- Check camera permissions in Windows settings
- Try different `CAMERA_INDEX` values
- Verify camera works in other apps

**Face detection not working:**
- Ensure good lighting
- Face should be front-facing
- Adjust `SCALE_FACTOR` and `MIN_NEIGHBORS`
- Check if Haar Cascade files exist

**High CPU usage:**
- Lower resolution (`FRAME_WIDTH`, `FRAME_HEIGHT`)
- Reduce FPS
- Process fewer frames (`PROCESS_EVERY_N_FRAMES`)

**Backend not receiving updates:**
- Check if backend is running on port 8000
- Verify `BACKEND_WS_URL` in `vision_client.py`
- Check WebSocket connection status

**Screen capture errors:**
- Windows 10/11 required
- Check screen capture permissions
- Disable GPU hardware acceleration if issues

## 📊 Performance Metrics

### Webcam Mode
- ~30 FPS capture
- ~15 FPS face detection
- ~50ms latency
- ~200MB RAM usage

### Screen Analysis Mode
- Capture every 30 seconds
- ~1 second analysis time
- ~300MB RAM usage

## 🎯 Future Enhancements

**Planned Features:**
- [ ] Deep learning emotion recognition
- [ ] Gesture detection
- [ ] Eye gaze tracking
- [ ] Multi-face support
- [ ] Activity recognition
- [ ] Object detection
- [ ] OCR for screen text
- [ ] Voice-vision multimodal understanding

**Model Integration:**
- Custom CNN for emotions
- YOLO for object detection
- MediaPipe for pose estimation
- GPT-4V for advanced screen analysis
