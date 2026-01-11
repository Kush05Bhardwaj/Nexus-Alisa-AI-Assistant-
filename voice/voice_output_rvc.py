import asyncio
import edge_tts
import soundfile as sf
import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / "overlay"))
from avatar_controller import on_speech_start, on_speech_end
from rvc.inferencer import convert
import simpleaudio as sa

BASE_WAV = "base.wav"
RVC_WAV = "alisa.wav"

VOICE = "en-US-JennyNeural"  # neutral base voice

async def tts_base(text):
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(BASE_WAV)

def speak(text):
    on_speech_start()

    asyncio.run(tts_base(text))
    convert(BASE_WAV, RVC_WAV)

    wave_obj = sa.WaveObject.from_wave_file(RVC_WAV)
    play_obj = wave_obj.play()
    play_obj.wait_done()

    on_speech_end()
