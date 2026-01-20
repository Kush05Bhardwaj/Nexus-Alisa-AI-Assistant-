"""
Test different voice configurations for Hinglish
Compare pitch/rate/voice combinations to find the cutest!
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from voice_output_hinglish import speak

test_text_hinglish = "Namaste! Main tumhari AI assistant hoon. Kya main help kar sakti hoon?"
test_text_mixed = "Hey! Aaj ka din bahut acha hai, let's get started!"

print("🎀 WAIFU VOICE COMPARISON TEST 🎀\n")
print("Testing different configurations for cuteness...\n")

# Test configurations
configs = [
    {
        "name": "Config 1: Swara (Hindi) + High Pitch",
        "voice": "swara",
        "rate": "+20%",
        "pitch": "+15Hz",
    },
    {
        "name": "Config 2: Swara (Hindi) + VERY High Pitch", 
        "voice": "swara",
        "rate": "+25%",
        "pitch": "+20Hz",
    },
    {
        "name": "Config 3: Neerja (Indian English) + High Pitch",
        "voice": "neerja",
        "rate": "+20%", 
        "pitch": "+15Hz",
    },
    {
        "name": "Config 4: Neerja + VERY High Pitch",
        "voice": "neerja",
        "rate": "+25%",
        "pitch": "+20Hz",
    },
]

def update_config(voice, rate, pitch):
    """Temporarily update voice config"""
    import voice_config
    # Update the globals
    voice_config.HINGLISH_VOICE = voice
    voice_config.HINGLISH_SPEECH_RATE = rate
    voice_config.HINGLISH_PITCH_SHIFT = pitch
    # Force reload
    from importlib import reload
    reload(voice_config)

if __name__ == "__main__":
    print("Text: " + test_text_hinglish)
    print("\n" + "=" * 70 + "\n")
    
    for i, config in enumerate(configs, 1):
        print(f"\n🎤 Test {i}/4: {config['name']}")
        print(f"   Voice: {config['voice']} | Rate: {config['rate']} | Pitch: {config['pitch']}")
        print(f"   Playing...")
        
        # Update configuration
        import voice_config
        voice_config.HINGLISH_VOICE = config['voice']
        voice_config.HINGLISH_SPEECH_RATE = config['rate']
        voice_config.HINGLISH_PITCH_SHIFT = config['pitch']
        
        # Speak
        speak(test_text_hinglish)
        
        print(f"   ✓ Done\n")
        
        if i < len(configs):
            input("   Press Enter for next test...")
    
    print("\n" + "=" * 70)
    print("\n✅ All tests complete!")
    print("\nNow update voice_config.py with your favorite settings! 🎀")
