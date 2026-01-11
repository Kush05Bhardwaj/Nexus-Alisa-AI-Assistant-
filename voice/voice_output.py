import pyttsx3
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / "overlay"))
from avatar_controller import on_speech_start, on_speech_end

engine = pyttsx3.init()
engine.setProperty("rate", 170)

def speak(text: str):
    on_speech_start()
    engine.say(text)
    engine.runAndWait()
    on_speech_end()
