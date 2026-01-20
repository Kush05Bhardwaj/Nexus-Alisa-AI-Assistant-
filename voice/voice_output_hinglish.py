"""
Hinglish-aware TTS with RVC voice conversion
Automatically detects Hinglish and uses appropriate base voice before RVC conversion

Pipeline:
Text (Hinglish) → Auto-detect language → Base TTS (Indian/English voice) 
→ RVC Voice Conversion → Final Waifu Voice (Hinglish)
"""

import asyncio
import edge_tts
import soundfile as sf
import os
import sys
import tempfile
import time
from pathlib import Path
from pydub import AudioSegment

# Try to import overlay controller
sys.path.append(str(Path(__file__).parent.parent / "overlay"))
try:
    from avatar_controller import on_speech_start, on_speech_end
    OVERLAY_AVAILABLE = True
except ImportError:
    OVERLAY_AVAILABLE = False
    def on_speech_start():
        pass
    def on_speech_end():
        pass

# Import RVC converter
from rvc.inferencer import convert
import pygame

# Initialize pygame mixer for audio playback
pygame.mixer.init()

# Import voice configuration with Hinglish support
from voice_config import (
    get_voice_for_text, 
    get_tts_params_for_text,
    is_hinglish
)

async def tts_base(text, output_file):
    """
    Generate base TTS with automatic Hinglish detection
    Uses appropriate voice based on text content
    Converts MP3 to WAV for compatibility
    """
    # Auto-detect voice and parameters
    voice = get_voice_for_text(text)
    params = get_tts_params_for_text(text)
    
    is_hinglish_text = is_hinglish(text)
    lang_label = "🇮🇳 Hinglish" if is_hinglish_text else "🇺🇸 English"
    
    print(f"🎤 TTS: {lang_label} | Voice: {voice}")
    
    # Generate TTS to temporary MP3 file
    temp_mp3 = output_file + ".mp3"
    communicate = edge_tts.Communicate(
        text, 
        voice,
        rate=params["rate"],
        pitch=params["pitch"]
    )
    await communicate.save(temp_mp3)
    
    # Convert MP3 to WAV for pygame/RVC compatibility
    try:
        audio = AudioSegment.from_mp3(temp_mp3)
        audio.export(output_file, format="wav")
        os.unlink(temp_mp3)  # Clean up temp MP3
    except Exception as e:
        print(f"⚠️ MP3 to WAV conversion failed: {e}")
        # Fallback: just rename (might not work with pygame)
        if os.path.exists(temp_mp3):
            os.rename(temp_mp3, output_file)

async def speak_async(text):
    """
    Async version of speak with Hinglish-aware RVC conversion
    
    Pipeline:
    1. Detect if text is Hinglish
    2. Generate base TTS with appropriate voice
    3. Convert using RVC to waifu voice
    4. Play converted audio
    """
    base_wav = None
    rvc_wav = None
    
    try:
        # Create unique temporary files
        fd_base, base_wav = tempfile.mkstemp(suffix='.wav', prefix='alisa_base_')
        os.close(fd_base)
        fd_rvc, rvc_wav = tempfile.mkstemp(suffix='.wav', prefix='alisa_rvc_')
        os.close(fd_rvc)
        
        # Safe overlay notification
        if OVERLAY_AVAILABLE:
            try:
                on_speech_start()
            except:
                pass

        # Step 1: Generate base TTS with auto language detection
        await tts_base(text, base_wav)
        
        # Step 2: Convert using RVC to get waifu voice
        print(f"🎀 Converting to waifu voice...")
        convert(base_wav, rvc_wav)

        # Step 3: Play converted audio
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        # Stop previous audio
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()

        pygame.mixer.music.load(rvc_wav)
        pygame.mixer.music.play()
        
        print(f"🎵 Playing waifu voice...")
        
        # Wait for playback to finish
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        # Unload to release file
        pygame.mixer.music.unload()

        # Safe overlay notification
        if OVERLAY_AVAILABLE:
            try:
                on_speech_end()
            except:
                pass
        
        print(f"✅ Playback complete")
                
    except Exception as e:
        print(f"❌ Hinglish RVC Voice error: {e}")
        import traceback
        traceback.print_exc()
        print(f"[TEXT] {text}")
    
    finally:
        # Clean up temporary files
        for temp_file in [base_wav, rvc_wav]:
            if temp_file and os.path.exists(temp_file):
                try:
                    time.sleep(0.1)  # Small delay for file release
                    os.unlink(temp_file)
                except Exception as cleanup_error:
                    print(f"⚠️ Could not delete temp file: {cleanup_error}")

def speak(text):
    """
    Speak text using Hinglish-aware RVC waifu voice
    Thread-safe wrapper for async function
    """
    try:
        import threading
        
        def run_in_thread():
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            try:
                new_loop.run_until_complete(speak_async(text))
            finally:
                new_loop.close()
        
        thread = threading.Thread(target=run_in_thread)
        thread.start()
        thread.join()
        
    except Exception as e:
        print(f"❌ Speak thread error: {e}")

# Test function
if __name__ == "__main__":
    print("🎀 Alisa Hinglish Voice Test")
    
    # Test English
    print("\n--- Test 1: English ---")
    speak("Hello! I'm your cute AI assistant!")
    
    # Test Hinglish
    print("\n--- Test 2: Hinglish ---")
    speak("Haan yaar, main tumhari cute AI assistant hoon!")
    
    # Test mixed
    print("\n--- Test 3: Mixed ---")
    speak("Kya baat hai! You're looking great aaj!")
    
    print("\n✅ Test complete!")