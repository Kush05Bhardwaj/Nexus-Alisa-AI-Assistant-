# 🎭 Phase 9B Quick Reference

## What is Phase 9B?

**Idle / Spontaneous Behavior System**  
Alisa speaks without user input - rarely and naturally.

## Key Features

✅ **Speaks rarely** - Companion, not chatbot  
✅ **Context-aware** - Understands vision, time, mode  
✅ **No questions** - Respects silence  
✅ **Natural timing** - Multiple probability gates  
✅ **Session adaptive** - Quieter if been chatty  

## How Often Does She Speak?

| Silence | Base Chance | Example |
|---------|-------------|---------|
| < 2 min | 0% | Never |
| 2-5 min | 8% | Very rare |
| 5-10 min | 15% | Rare |
| 10-30 min | 25% | Occasional |
| 30+ min | 40% | More likely |

**Note**: Actual probability is modified by vision, mode, time, and session chattiness.

## Example Probabilities

### User coding quietly, 8 minutes silence, afternoon, serious mode
- Base: 25%
- × Focused: 0.7 = 17.5%
- × Serious: 0.6 = 10.5%
- **Final: 10.5% chance**

### User away, 35 minutes, late night, teasing mode
- Base: 40%
- × Away: 0.3 = 12%
- × Teasing: 1.2 = 14.4%
- × Late night: 0.5 = 7.2%
- **Final: 7.2% chance**

### User present, 3 AM, 15 minutes silence, calm mode
- Base: 25%
- × Focused: 0.7 = 17.5%
- × Calm: 0.8 = 14%
- × Very late: 0.2 = 2.8%
- **Final: 2.8% chance**

## Quick Settings

### Make More Chatty
Edit `backend/app/idle_companion.py`:
```python
"short": 0.15,    # was 0.08
"medium": 0.25,   # was 0.15
"long": 0.35,     # was 0.25
```

### Make Quieter
```python
"short": 0.03,    # was 0.08
"medium": 0.08,   # was 0.15
"long": 0.15,     # was 0.25
```

### Speak Sooner
```python
"short": 60,      # was 120 (1 min)
"medium": 180,    # was 300 (3 min)
```

### Speak Later
```python
"short": 180,     # was 120 (3 min)
"medium": 600,    # was 300 (10 min)
```

## Good vs Bad Examples

### ✅ Good Spontaneous Speech
- "Hmm..."
- "*yawns*"
- "It's gotten quiet."
- "Working late, huh?"
- "*stretches*"

### ❌ Bad Spontaneous Speech
- "How are you?" (question)
- "Tell me what you're doing!" (command)
- "Hey! Want to talk?" (chatbot-like)

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Too chatty | Reduce BASE_PROBABILITY |
| Too quiet | Increase BASE_PROBABILITY |
| Not speaking at all | Check companion_mode is active (needs 3+ interactions) |
| Speaking too often | Increase MIN_SILENCE_FOR_SPEECH |

## Monitoring

Look for these logs:
```
🎯 Phase 9B trigger: long_silence_720s_prob_18%
💭 Phase 9B - Companion speech (quiet_working, 720s silence)...
✅ Companion speech (calm): You've been working quietly...
🔇 Phase 9B silent: probability_gate_12%
```

## System Status

Check if it's working:
- Look for "🧠 Phase 9B - Companion System initialized" on startup
- User must interact 3+ times to activate companion mode
- At least 2 minutes silence before any speech
- Multiple probability gates must pass

## Files

- **Implementation**: `backend/app/idle_companion.py`
- **Integration**: `backend/app/ws.py`
- **Documentation**: `docs/PHASE_9B_IMPLEMENTATION.md`

## Philosophy

**Companion, not chatbot**  
Speaks rarely, naturally, respectfully.  
Silence is golden. Less is more.
