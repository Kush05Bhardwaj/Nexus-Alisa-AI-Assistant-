"""
Discover all available Edge TTS voices for Hinglish
Shows age, gender, and language info
"""
import asyncio
import edge_tts

async def list_voices():
    """List all available voices with details"""
    voices = await edge_tts.list_voices()
    
    # Filter for Indian/Hindi voices
    print("🇮🇳 INDIAN & HINDI VOICES\n")
    print("=" * 80)
    
    indian_voices = [v for v in voices if v['Locale'].startswith(('en-IN', 'hi-IN'))]
    
    for voice in sorted(indian_voices, key=lambda x: (x['Locale'], x['Gender'])):
        name = voice['ShortName']
        gender = voice['Gender']
        locale = voice['Locale']
        
        # Try to get age/style info from voice name
        age_hint = "👧 Young" if "Neural" in name else "👤 Standard"
        
        print(f"\n📢 {name}")
        print(f"   Language: {locale}")
        print(f"   Gender: {gender}")
        print(f"   Style: {age_hint}")
    
    print("\n" + "=" * 80)
    print("\n🎌 JAPANESE VOICES (for comparison)\n")
    print("=" * 80)
    
    japanese_voices = [v for v in voices if v['Locale'].startswith('ja-JP')]
    
    for voice in sorted(japanese_voices, key=lambda x: x['Gender']):
        if voice['Gender'] == 'Female':
            name = voice['ShortName']
            print(f"\n📢 {name}")
            print(f"   (These are naturally higher-pitched for anime-style)")

if __name__ == "__main__":
    asyncio.run(list_voices())
