def extract_emotion(text: str):
    """
    Extract emotion tag from LLM response.
    Backend guard: If LLM forgets the emotion tag, add neutral as fallback.
    This ensures overlay and voice systems never break due to missing emotion.
    """
    if not text.startswith("<emotion="):
        # Backend guard: LLM forgot emotion tag, add it
        text = "<emotion=neutral>\n" + text
    
    tag = text.split(">")[0]
    emotion = tag.replace("<emotion=", "")
    clean_text = text.split(">", 1)[1].strip()
    return emotion, clean_text
