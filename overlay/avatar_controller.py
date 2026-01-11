from avatar_window import start_talking, stop_talking

def on_speech_start():
    start_talking()

def on_speech_end():
    stop_talking()

def on_emotion(emotion: str):
    # Phase 6+: map emotion → expression
    print(f"[Avatar Emotion] {emotion}")
