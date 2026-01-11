import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
from faster_whisper import WhisperModel

SAMPLE_RATE = 16000
DURATION = 5  # seconds

model = WhisperModel("small", device="cuda", compute_type="float16")

def record_audio():
    print("🎙️ Listening...")
    audio = sd.rec(
        int(DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="int16"
    )
    sd.wait()
    wav.write("input.wav", SAMPLE_RATE, audio)
    print("🎤 Done recording")

def speech_to_text():
    segments, _ = model.transcribe("input.wav")
    text = " ".join(seg.text for seg in segments)
    print("📝 You said:", text)
    return text

if __name__ == "__main__":
    record_audio()
    speech_to_text()
