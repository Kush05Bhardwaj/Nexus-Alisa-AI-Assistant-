def extract_emotion(text: str):
    """
    Extract emotion tag from LLM response.
    Backend guard: If LLM forgets the emotion tag, add neutral as fallback.
    This ensures overlay and voice systems never break due to missing emotion.
    """
    # List of valid emotions
    valid_emotions = ["teasing", "calm", "serious", "happy", "sad", "neutral"]
    
    # Case 1: Proper format with tag
    if text.startswith("<emotion="):
        tag = text.split(">")[0]
        emotion = tag.replace("<emotion=", "")
        clean_text = text.split(">", 1)[1].strip()
        return emotion, clean_text
    
    # Case 2: LLM output ONLY an emotion word (broken response)
    # If the entire response is just an emotion word, treat it as neutral with that text
    text_stripped = text.strip().lower()
    if text_stripped in valid_emotions:
        # LLM broke - just outputted emotion word
        # Treat as neutral and keep the word in output (it's weird but visible)
        return "neutral", text.strip()
    
    # Case 3: LLM put emotion word at start without tag (fallback)
    for emotion in valid_emotions:
        # Check if starts with emotion word followed by space or newline
        if text.lower().startswith(emotion + " "):
            clean_text = text[len(emotion):].strip()
            # Only extract if there's actual content after the emotion
            if clean_text:
                return emotion, clean_text
        if text.lower().startswith(emotion + "\n"):
            clean_text = text[len(emotion):].strip()
            if clean_text:
                return emotion, clean_text
    
    # Case 4: No emotion detected, add neutral
    return "neutral", text.strip()
