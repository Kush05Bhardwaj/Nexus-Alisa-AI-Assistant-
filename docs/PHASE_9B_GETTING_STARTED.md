# 🚀 Phase 9B - Getting Started

## What is Phase 9B?

**Phase 9B** makes Alisa speak spontaneously without you asking - **rarely** and **naturally**, like a real companion.

## Quick Start (3 Steps)

### Step 1: Start Backend
```powershell
cd backend
.\venv\Scripts\Activate.ps1
cd ..
uvicorn backend.app.main:app --reload
```

Look for this in the logs:
```
🧠 Phase 9B - Companion System initialized
   Alisa will speak spontaneously when it feels natural
   Speech is RARE - companion, not chatbot
```

✅ **Phase 9B is now active!**

### Step 2: Activate Companion Mode
Interact with Alisa **at least 3 times**:

```
You: "Hi Alisa"
Alisa: "Hi!"

You: "How are you?"
Alisa: "I'm good!"

You: "What time is it?"
Alisa: "It's 3 PM"
```

After 3 interactions, **companion mode activates**.

### Step 3: Wait and Listen
Now just wait 2+ minutes in silence and see if Alisa speaks!

**Note**: It's probabilistic, so she might not speak immediately. That's normal - she's a companion, not a chatbot.

## How Often Will She Speak?

| Silence Duration | Chance |
|------------------|--------|
| Less than 2 min | 0% (never) |
| 2-5 minutes | ~8% |
| 5-10 minutes | ~15% |
| 10-30 minutes | ~25% |
| 30+ minutes | ~40% |

These are base probabilities - actual chance depends on vision, mode, and time of day.

## What Will She Say?

**Examples of natural spontaneous speech**:
- "Hmm..."
- "*yawns softly*"
- "It's gotten quiet."
- "Working late, huh?"
- "Still there?"
- "*stretches*"

**She WON'T say**:
- "How are you?" (no questions)
- "Tell me what you're doing!" (no commands)
- "Hey! Want to talk?" (not chatbot-like)

## Troubleshooting

### "She's not speaking at all"
✅ Check: Backend logs say "Phase 9B - Companion System initialized"  
✅ Check: You've interacted 3+ times (companion mode active)  
✅ Check: You've waited at least 2 minutes in silence  
✅ Remember: It's probabilistic (8-40% chance)  
✅ Try: Wait 10+ minutes for higher probability  

### "She's speaking too often"
Edit `backend/app/idle_companion.py`:
```python
self.BASE_PROBABILITY = {
    "short": 0.03,      # was 0.08 (reduce)
    "medium": 0.08,     # was 0.15 (reduce)
    "long": 0.15,       # was 0.25 (reduce)
    "very_long": 0.25,  # was 0.40 (reduce)
}
```

### "She's not speaking often enough"
Edit `backend/app/idle_companion.py`:
```python
self.BASE_PROBABILITY = {
    "short": 0.15,      # was 0.08 (increase)
    "medium": 0.25,     # was 0.15 (increase)
    "long": 0.35,       # was 0.25 (increase)
    "very_long": 0.50,  # was 0.40 (increase)
}
```

## What to Expect

### First 2 Minutes
**Nothing** - System respects silence, won't speak too soon.

### 2-10 Minutes
**Rare chance** (8-15%) - Might hear a soft comment or yawn.

### 10-30 Minutes
**Occasional** (25%) - More likely to speak now.

### 30+ Minutes
**More likely** (40%) - Probably will say something.

## Logs to Watch

### When deciding to speak:
```
🎯 Phase 9B trigger: medium_silence_350s_prob_14%
   Stats: silence=350s, companion_mode=True, conversations=5
💭 Phase 9B - Companion speech (general_silence, 350s silence)...
✅ Companion speech (calm): It's gotten quiet...
```

### When staying silent:
```
🔇 Phase 9B silent: probability_gate_11% (silence=240s, category=medium)
```

## Testing Tips

1. **Be patient** - It's designed to be RARE
2. **Wait 10+ minutes** - Higher probability
3. **Try multiple times** - Probabilistic system
4. **Check logs** - See what's happening
5. **Adjust settings** - Tune to your preference

## Advanced: Factors That Affect Probability

### Vision State
- **User absent**: Lower (can't hear anyway)
- **User focused**: Lower (respect their flow)
- **User distracted**: Higher (gentle nudge)

### Current Mode
- **Serious**: Lower (quieter companion)
- **Teasing**: Higher (more playful)
- **Calm**: Medium (gentle presence)

### Time of Day
- **Very late (12-6 AM)**: Much lower
- **Late (10 PM-12 AM)**: Lower
- **Early morning (6-9 AM)**: Slightly lower
- **Day time**: Normal

### Session Activity
- **Very chatty session**: Lower
- **Quiet session**: Normal

## Full Documentation

- 📘 **Full Guide**: `docs/PHASE_9B_IMPLEMENTATION.md`
- 📋 **Quick Ref**: `docs/PHASE_9B_QUICK_REF.md`
- 🎨 **Visual Guide**: `docs/PHASE_9B_VISUAL_GUIDE.md`
- 📊 **Summary**: `PHASE_9B_SUMMARY.md`

## Philosophy

Phase 9B makes Alisa a **companion**, not a **chatbot**:

✅ Exists even when quiet  
✅ Speaks rarely and naturally  
✅ Respects silence  
✅ No questions or commands  
✅ Adapts to context  
✅ Less is more  

---

## 🎉 You're All Set!

Phase 9B is active and working. Alisa is now a natural companion who can speak spontaneously.

**Remember**: She's designed to speak RARELY. If you don't hear anything for a while, that's normal and intended. When she does speak, it'll feel natural and meaningful.

Enjoy your new companion! 🌟
