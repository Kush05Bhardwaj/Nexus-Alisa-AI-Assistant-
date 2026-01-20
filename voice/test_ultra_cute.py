"""
Advanced Hinglish TTS with SSML pitch control
For MAXIMUM waifu cuteness using SSML prosody tags
"""
import asyncio
import edge_tts
import os
import tempfile
from pydub import AudioSegment
from pathlib import Path

async def speak_hinglish_ultra_cute(text, output_wav):
    """
    Generate ultra-cute Hinglish voice using SSML
    SSML allows more fine-grained control over prosody
    """
    
    # Wrap text in SSML with prosody tags for maximum cuteness
    ssml = f"""
    <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="hi-IN">
        <voice name="hi-IN-SwaraNeural">
            <prosody pitch="+25%" rate="1.3" volume="loud">
                {text}
            </prosody>
        </voice>
    </speak>
    """
    
    # Generate with SSML
    communicate = edge_tts.Communicate(ssml)
    
    # Save to temp MP3
    temp_mp3 = output_wav + ".mp3"
    await communicate.save(temp_mp3)
    
    # Convert to WAV
    audio = AudioSegment.from_mp3(temp_mp3)
    
    # Optional: Pitch shift in post-processing for extra cuteness
    # Shift up by 2 semitones (anime-style)
    octaves = 0.15  # Positive = higher pitch
    new_sample_rate = int(audio.frame_rate * (2.0 ** octaves))
    pitched_audio = audio._spawn(audio.raw_data, overrides={'frame_rate': new_sample_rate})
    pitched_audio = pitched_audio.set_frame_rate(44100)  # Standard rate
    
    # Export
    pitched_audio.export(output_wav, format="wav")
    
    # Cleanup
    os.unlink(temp_mp3)
    
    print(f"🎀 Ultra-cute voice generated!")

async def test_ultra_cute():
    """Test the ultra-cute voice"""
    output = "ultra_cute_test.wav"
    
    await speak_hinglish_ultra_cute(
        "Namaste! Main tumhari cute AI assistant hoon! Kya help chahiye?",
        output
    )
    
    # Play it
    import pygame
    pygame.mixer.init()
    pygame.mixer.music.load(output)
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    print("✅ Playback complete!")
    
    # Keep the file for comparison
    print(f"\n💾 Saved to: {output}")
    print("Compare with regular voice to hear the difference!")

if __name__ == "__main__":
    print("🎀 ULTRA-CUTE HINGLISH VOICE TEST 🎀\n")
    asyncio.run(test_ultra_cute())
