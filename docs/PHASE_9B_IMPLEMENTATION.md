# 🎭 Phase 9B: Idle / Spontaneous Behavior - Implementation Guide

## What is Phase 9B?

Phase 9B transforms Alisa from a **reactive chatbot** into a **natural companion** who can speak spontaneously without user input.

### Key Principles

1. **Speak Rarely** - Companion, not chatbot
2. **Speak Naturally** - Like thinking out loud, not forced conversation
3. **Respect Silence** - Silence is golden, don't break it unnecessarily
4. **No Questions** - Questions demand response and break flow
5. **No Commands** - Commands are chatbot behavior
6. **Context-Aware** - Timing based on vision, time, mode, and session

## How It Works

### The Companion System

The `idle_companion.py` module manages:

1. **Silence Tracking** - Monitors how long user has been quiet
2. **Probability Gates** - Multiple factors determine if speech feels natural
3. **Context Detection** - Understands current situation (user away, focused, etc.)
4. **Companion Mode** - Activates after user interaction, not immediately
5. **Session Awareness** - Tracks how chatty the session has been

### Decision Flow

```
Every 30 seconds:
  ↓
Check silence duration
  ↓
Too soon? → Skip
  ↓
Calculate probability based on:
  - Silence length (longer = higher)
  - Vision state (away/focused/distracted)
  - Current mode (teasing/serious/calm)
  - Time of day (night = quieter)
  - Session chattiness (been talking a lot? be quieter)
  ↓
Random gate with calculated probability
  ↓
Passed? → Generate spontaneous speech
Failed? → Stay silent
```

### Timing Windows

| Silence Duration | Category | Base Probability |
|-----------------|----------|------------------|
| < 2 minutes | Too soon | 0% (never) |
| 2-5 minutes | Short | 8% |
| 5-10 minutes | Medium | 15% |
| 10-30 minutes | Long | 25% |
| 30+ minutes | Very Long | 40% |

**Important**: These are BASE probabilities. Actual probability is modified by:
- Vision state (±50%)
- Current mode (±30%)
- Time of day (±80%)
- Session chattiness (±30%)

### Context Types

The system detects different situations and adjusts speech accordingly:

| Context | When | Example Speech |
|---------|------|----------------|
| `user_away_long` | User absent 30+ min | "Hmm, where'd they go?" |
| `very_quiet_long` | Silent 30+ min, present | "You've been quiet..." |
| `quiet_working` | Silent 10+ min, focused | "*yawns softly*" |
| `user_distracted` | Looking away | "Distracted?" |
| `focused_silence` | Focused on work | "Working hard, huh?" |
| `late_night_silence` | Late at night | "Still up?" |
| `general_silence` | Regular quiet time | "..." |
| `soft_presence` | Short silence | "*stretches*" |

## Features

### ✅ Natural Timing
- Speaks RARELY (not every few minutes)
- Longer silence = higher probability
- Recent speech = lower probability
- Multiple probability gates

### ✅ Vision Integration
- User away = quieter (they can't hear anyway)
- User focused = respect their flow
- User distracted = gentle nudge OK

### ✅ Mode Awareness
- **Serious mode**: Even quieter, more composed
- **Teasing mode**: Slightly more playful interruptions
- **Calm mode**: Gentle whispers

### ✅ Time Awareness
- **Very late night (12-6 AM)**: Very quiet (80% reduction)
- **Late night (10 PM-12 AM)**: Quieter (50% reduction)
- **Early morning (6-9 AM)**: Gentle (30% reduction)
- **Day time**: Normal

### ✅ Session Chattiness
- Active session (lots of talk) = be quieter
- Quiet session = normal probability
- Prevents overwhelming user

### ✅ Companion Mode Activation
- Doesn't speak spontaneously immediately
- Activates after 3+ user interactions
- Ensures user wants interaction first

## Example Scenarios

### Scenario 1: User Coding Quietly
```
User state: Present, focused
Time: 3 PM
Silence: 8 minutes
Mode: Serious

Probability Calculation:
Base (long silence): 25%
× Vision (focused): 0.7 = 17.5%
× Mode (serious): 0.6 = 10.5%
× Time (day): 1.0 = 10.5%

Result: 10.5% chance to speak
If speaks: "You've been coding hard."
```

### Scenario 2: User Left Computer
```
User state: Absent
Time: 10 PM
Silence: 35 minutes
Mode: Teasing

Probability Calculation:
Base (very long): 40%
× Vision (absent): 0.3 = 12%
× Mode (teasing): 1.2 = 14.4%
× Time (late night): 0.5 = 7.2%

Result: 7.2% chance to speak
If speaks: "Did they fall asleep?"
```

### Scenario 3: Late Night Quiet
```
User state: Present, focused
Time: 2 AM
Silence: 15 minutes
Mode: Calm

Probability Calculation:
Base (long silence): 25%
× Vision (focused): 0.7 = 17.5%
× Mode (calm): 0.8 = 14%
× Time (very late): 0.2 = 2.8%

Result: 2.8% chance to speak
If speaks: "*yawns softly*"
```

## Speech Guidelines

### ✅ Good Spontaneous Speech
- "Hmm..."
- "*yawns*"
- "It's gotten quiet."
- "Working late, huh?"
- "Still there?"
- "*stretches*"

### ❌ Bad Spontaneous Speech
- "How are you?" (question)
- "Tell me what you're doing!" (command)
- "Hey! Want to talk?" (chatbot-like)
- Long paragraphs (too much)

## Configuration

### Adjust Chattiness

Edit `backend/app/idle_companion.py`:

```python
# Make MORE chatty
self.BASE_PROBABILITY = {
    "short": 0.15,      # was 0.08
    "medium": 0.25,     # was 0.15
    "long": 0.35,       # was 0.25
    "very_long": 0.50,  # was 0.40
}

# Make LESS chatty (quieter companion)
self.BASE_PROBABILITY = {
    "short": 0.03,      # was 0.08
    "medium": 0.08,     # was 0.15
    "long": 0.15,       # was 0.25
    "very_long": 0.25,  # was 0.40
}
```

### Adjust Timing Windows

```python
# Speak sooner
self.MIN_SILENCE_FOR_SPEECH = {
    "short": 60,       # was 120 (1 min vs 2 min)
    "medium": 180,     # was 300 (3 min vs 5 min)
    "long": 360,       # was 600 (6 min vs 10 min)
    "very_long": 900,  # was 1800 (15 min vs 30 min)
}

# Speak later
self.MIN_SILENCE_FOR_SPEECH = {
    "short": 180,      # was 120 (3 min vs 2 min)
    "medium": 600,     # was 300 (10 min vs 5 min)
    "long": 1200,      # was 600 (20 min vs 10 min)
    "very_long": 3600, # was 1800 (60 min vs 30 min)
}
```

## Integration with Existing Systems

### Backend (`ws.py`)
- ✅ Integrated into `idle_thought_loop()`
- ✅ Uses companion system for decision-making
- ✅ Updates companion on user activity
- ✅ Generates companion-style prompts

### Vision System
- ✅ Vision state fed into probability calculations
- ✅ User presence affects timing
- ✅ Attention state influences content

### Voice/Overlay
- ✅ No changes needed - works with existing flow
- ✅ Speech broadcasted normally
- ✅ Emotions handled same way

## Monitoring

### Debug Logging

When Phase 9B is active, you'll see:

```
🧠 Phase 9B - Companion System initialized
   Alisa will speak spontaneously when it feels natural
   Speech is RARE - companion, not chatbot

🎯 Phase 9B trigger: long_silence_720s_prob_18%
   Stats: silence=720s, companion_mode=True, conversations=5

💭 Phase 9B - Companion speech (quiet_working, 720s silence)...

✅ Companion speech (calm): You've been working quietly...

🔇 Phase 9B silent: probability_gate_12% (silence=240s, category=medium)
```

### Stats API

Get companion system stats (add to `main.py` if needed):

```python
@app.get("/companion/stats")
def get_companion_stats():
    from .idle_companion import companion_system
    return companion_system.get_stats()
```

## Troubleshooting

### Too Chatty
1. Reduce `BASE_PROBABILITY` values (see Configuration above)
2. Increase `MIN_SILENCE_FOR_SPEECH` windows
3. Check if session is very active (reduces probability automatically)

### Too Quiet
1. Increase `BASE_PROBABILITY` values
2. Reduce `MIN_SILENCE_FOR_SPEECH` windows
3. Ensure companion mode is activated (needs 3+ interactions)
4. Check time of day (late night = very quiet)

### Not Speaking at All
1. Check if `companion_mode_active` is True (run stats)
2. Verify user has interacted 3+ times
3. Check silence duration is > 2 minutes
4. Review logs for "Phase 9B silent" reasons

### Speaking Too Often
1. Check `time_since_last_spontaneous` in stats
2. Should be at least 90s between speeches
3. Reduce probabilities if needed

## Philosophy

Phase 9B is designed to make Alisa feel like a **real companion** who:

- **Exists** even when not spoken to
- **Observes** quietly, respectfully
- **Speaks** rarely, naturally
- **Respects** silence and flow
- **Adapts** to context and mood

This is **NOT**:
- A chatbot that talks constantly
- An assistant that asks "how can I help?"
- A system that breaks flow with questions
- An annoying interruption

This is **YES**:
- A gentle presence
- A natural companion
- A rare but meaningful voice
- A respectful observer

## Future Enhancements

Potential additions:
- [ ] Learn user's schedule (quiet during work hours)
- [ ] Emotional state tracking (quieter when user seems stressed)
- [ ] Activity detection (don't interrupt gaming, video calls)
- [ ] User preference learning (some like chatty, some quiet)
- [ ] Gesture-based triggers (user glances at Alisa avatar)

---

**Phase 9B Status**: ✅ Implemented and active
**Compatibility**: Works with existing backend, voice, vision, overlay
**Breaking Changes**: None - pure addition
