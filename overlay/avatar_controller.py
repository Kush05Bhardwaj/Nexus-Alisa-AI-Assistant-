"""
Avatar Controller - Thread-safe API for controlling avatar
This module provides functions that can be called from other threads (like voice output)
to safely control the avatar animations in the main Tkinter thread.
"""

from avatar_window import start_talking, stop_talking, set_emotion

_last_emotion = "neutral"

def on_speech_start():
    """Called when TTS starts speaking - triggers talking animation"""
    start_talking()
    print("🎤 Avatar started talking")

def on_speech_end():
    """Called when TTS finishes speaking - stops talking animation"""
    stop_talking()
    print("🤐 Avatar stopped talking")

def on_emotion(emotion: str):
    """Called when emotion is detected - changes avatar expression"""
    global _last_emotion
    if emotion != _last_emotion:
        _last_emotion = emotion
        set_emotion(emotion)
        print(f"😊 Avatar emotion changed to: {emotion}")
