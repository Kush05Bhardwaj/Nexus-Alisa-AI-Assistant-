"""
Quick test for Hinglish voice in text chat mode
"""
import asyncio
from voice_output_hinglish import speak_async

async def test():
    print("🧪 Testing Hinglish Voice for Text Chat\n")
    
    tests = [
        ("English test", "Hello! How are you doing today?"),
        ("Hinglish test", "Namaste! Kya haal hai? Main tumhari assistant hoon!"),
        ("Mixed test", "Hey yaar! Let's work together aaj!"),
    ]
    
    for name, text in tests:
        print(f"\n--- {name} ---")
        print(f"Text: {text}")
        await speak_async(text)
        print("✓ Done\n")
        await asyncio.sleep(0.5)
    
    print("✅ All tests complete!")

if __name__ == "__main__":
    asyncio.run(test())
