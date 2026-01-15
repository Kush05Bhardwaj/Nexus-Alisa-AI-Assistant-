import cv2
import numpy as np

try:
    import mediapipe as mp
    
    # Initialize MediaPipe Face Detection
    mp_face_detection = mp.solutions.face_detection.FaceDetection(
        model_selection=0,
        min_detection_confidence=0.6
    )
    
    # Initialize MediaPipe Face Mesh for attention detection
    mp_face_mesh = mp.solutions.face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )
    
    MEDIAPIPE_AVAILABLE = True
    print("✅ MediaPipe loaded successfully")
    
except Exception as e:
    MEDIAPIPE_AVAILABLE = False
    print(f"⚠️ MediaPipe not available: {e}")
    print("   Face detection will be disabled")

def detect_face_and_emotion(frame):
    """
    Detect face presence, emotion, and attention (looking at screen or away)
    Returns: (face_present, emotion, attention_state)
    """
    if not MEDIAPIPE_AVAILABLE:
        return None, "neutral", "unknown"
    
    try:
        # Convert BGR to RGB
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Detect face
        result = mp_face_detection.process(rgb)

        if not result.detections:
            return None, "no_face", "away"

        # Detect if user is looking at screen using face mesh
        mesh_result = mp_face_mesh.process(rgb)
        attention = "away"
        
        if mesh_result.multi_face_landmarks:
            landmarks = mesh_result.multi_face_landmarks[0]
            
            # Use eye landmarks to detect gaze direction
            # Left eye: landmarks 33, 133
            # Right eye: landmarks 362, 263
            # Nose tip: landmark 1
            
            left_eye = landmarks.landmark[33]
            right_eye = landmarks.landmark[362]
            nose = landmarks.landmark[1]
            
            # Simple heuristic: if face is relatively frontal, user is looking at screen
            # Check if eyes are at similar depth (z-coordinate)
            eye_depth_diff = abs(left_eye.z - right_eye.z)
            
            # If face is frontal (eyes at similar depth), user is likely looking at screen
            if eye_depth_diff < 0.02:
                attention = "focused"
            else:
                attention = "away"
        
        # Simple emotion detection (can be enhanced with a proper emotion CNN)
        # For now, just return neutral - you can add emotion detection here later
        emotion = "neutral"
        
        return "face", emotion, attention
        
    except Exception as e:
        print(f"⚠️ Error in face detection: {e}")
        return None, "neutral", "unknown"

    emotion = "neutral"
    
    return "face", emotion, attention
