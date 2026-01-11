def extract_emotion(text: str):
    if text.startswith("<emotion="):
        tag = text.split(">")[0]
        emotion = tag.replace("<emotion=", "")
        clean_text = text.split(">", 1)[1].strip()
        return emotion, clean_text
    return "neutral", text
