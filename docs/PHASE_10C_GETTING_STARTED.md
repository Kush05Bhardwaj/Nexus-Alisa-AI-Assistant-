# 🎯 Phase 10C: Task Memory & Habits - Getting Started

## Welcome to Adaptive AI

Phase 10C makes Alisa learn and adapt to your work patterns - quietly and automatically.

**No configuration needed. Just use Alisa normally, and she'll get smarter.**

---

## What You Need to Know

### The Core Idea

**Alisa watches how you work and adapts to your style.**

- Learns when you're most productive
- Knows when you prefer quiet
- Remembers your common workflows
- Adjusts her behavior accordingly

**All without asking. All without announcing.**

---

## First Time Setup

### Step 1: Start the Backend

```powershell
.\scripts\start_backend.ps1
```

That's it! Phase 10C is now active.

### Step 2: Use Alisa Normally

- Code as usual
- Chat when you want
- Take breaks
- Work your normal hours

**Alisa is observing and learning.**

### Step 3: Wait

After a few days of normal use, Alisa will have learned:
- Your peak working hours
- When you prefer silence
- Your common app workflows
- Your task patterns

---

## What Happens Behind the Scenes

### Day 1

```
You start coding at 2pm in VS Code
  ↓
Phase 10C: "Activity observed: coding_python at hour 14"
  ↓
Stored: work_schedule["14"].append(timestamp)
```

Nothing visible yet. Just observation.

### Day 3

```
You've coded at 2-3pm daily
  ↓
Phase 10C: "Peak hours detected: [14, 15]"
  ↓
Behavior: "Be extra careful interrupting at these hours"
```

Alisa becomes more respectful of your focus time.

### Day 7

```
You've been silent 45+ minutes at 9am every day
  ↓
Phase 10C: "Quiet hour detected: 9"
  ↓
Behavior: "Don't interrupt at 9am unless silence is very long"
```

Alisa learns your morning focus routine.

### Week 2

```
Pattern recognized: coding → browsing docs (5 times)
  ↓
Phase 10C: "Common workflow detected"
  ↓
Behavior: "Anticipate user may browse docs after coding"
```

Alisa can now offer contextual help proactively.

---

## How to See What's Been Learned

### Method 1: Check Logs

Watch for these messages on disconnect:

```
💾 Phase 10C: Saving learned patterns...
   📊 Session stats: 12 interactions
   🎯 Total tasks observed: 47
```

### Method 2: View Memory File

```powershell
notepad "$env:USERPROFILE\Documents\Alisa Memory\task_memory.json"
```

You'll see your learned patterns:

```json
{
  "patterns": {
    "peak_coding_hours": [14, 15, 20],
    "preferred_silence_hours": [9, 10, 22],
    "app_preferences": {
      "coding_python": "vscode",
      "browsing": "chrome"
    }
  }
}
```

### Method 3: Test Script

```powershell
python scripts/test_phase10c.py
```

Shows detailed statistics and patterns.

---

## Example Learning Scenarios

### Scenario 1: Morning Focus Learner

**Your routine**:
- 9am: Start work, focus for 45+ minutes
- 10am: Still focused, minimal interruptions
- 11am: More relaxed, chat with Alisa

**What Alisa learns** (after 1 week):
```json
{
  "preferred_silence_hours": [9, 10],
  "peak_coding_hours": [9, 10, 11]
}
```

**How she adapts**:
- 9:00am, 15 min silence: ❌ Doesn't interrupt (too early)
- 9:45am, 10 min silence: ❌ Doesn't interrupt (quiet hour)
- 11:00am, 10 min silence: ✅ May speak (end of focus period)

---

### Scenario 2: Afternoon Coder

**Your routine**:
- 2pm-4pm: Deep coding sessions
- 8pm-10pm: Evening coding
- Short breaks throughout

**What Alisa learns** (after 1 week):
```json
{
  "peak_coding_hours": [14, 15, 16, 20, 21],
  "work_schedule": {
    "14": [25 activities],
    "15": [22 activities],
    "20": [18 activities]
  }
}
```

**How she adapts**:
- 2:30pm: Extra cautious about interrupting
- 8:00pm: Respects peak hour, waits longer
- 5:00pm: Normal interruption timing

---

### Scenario 3: Workflow Optimizer

**Your routine**:
- Code in VS Code
- Hit error → Open Chrome for docs
- Back to VS Code
- Repeat 5+ times/week

**What Alisa learns**:
```json
{
  "common_workflows": [
    {
      "sequence": ["coding_python|vscode", "browsing_docs|chrome"],
      "frequency": 7,
      "avg_time_between": 180
    }
  ],
  "app_preferences": {
    "coding_python": "vscode",
    "browsing": "chrome"
  }
}
```

**How she adapts**:
- Coding → Error detected
- Alisa: "Need the docs?" (knows your pattern)
- With Phase 10B: Can proactively open Chrome

---

## Understanding Adaptive Behaviors

### 1. Interrupt Timing

**Before Phase 10C**:
```
10 minutes silence → Companion speaks
```

**After learning quiet hours**:
```
9:00am, 10 min silence → Waits (quiet hour)
2:00pm, 10 min silence → Speaks (normal hour)
```

---

### 2. Response Style

**Before Phase 10C**:
```
[Standard response length]
```

**After learning peak hours**:
```
Peak hour → Brief, focused responses
Normal hour → More detailed if needed
```

(Subtle hints added to LLM prompt)

---

### 3. Suggestions

**Before Phase 10C**:
```
Generic: "Want me to open an editor?"
```

**After learning preferences**:
```
Personalized: "Want me to open VS Code?" (knows you prefer it)
```

---

## How Long Until It Learns?

| Pattern | Time to Learn | Observations Needed |
|---------|---------------|---------------------|
| **Peak hours** | 3-5 days | ~15 activities at same hours |
| **Quiet hours** | 5-7 days | ~5 long silences at same hour |
| **App preferences** | 2-3 days | ~10 uses of same app for task |
| **Workflows** | 1-2 weeks | 3+ repeated sequences |

**General rule**: Use Alisa normally for a week, and she'll know your patterns.

---

## Tips for Best Learning

### ✅ Do This

1. **Use Alisa regularly** - Daily use helps her learn faster
2. **Keep your routine** - Consistent patterns are easier to learn
3. **Work naturally** - Don't change your habits for her
4. **Let her observe** - She learns by watching, not asking

### ❌ Don't Do This

1. **Don't reset memory** - Unless you want her to forget
2. **Don't vary hours wildly** - Makes pattern detection harder
3. **Don't expect instant learning** - Give it a few days
4. **Don't disable features** - Phase 9B/10A provide context

---

## Privacy & Data

### What's Tracked

✅ **When** you work (timestamps by hour)  
✅ **What apps** you use for which tasks  
✅ **How long** silences last  
✅ **Task transitions** (coding → browsing)  

### What's NOT Tracked

❌ **File contents** - Never read  
❌ **Typed text** - Never recorded  
❌ **URLs** - Not stored  
❌ **Personal data** - Not collected  
❌ **Screenshots** - Never taken  

### Where It's Stored

**Location**: `C:\Users\[You]\Documents\Alisa Memory\task_memory.json`

**Format**: Plain JSON (you can read/edit it)

**Control**: You own the file - delete anytime

**Backup**: Saved on every session end

---

## Troubleshooting

### "Nothing seems to be learned"

**Check**:
1. Is backend running? (Phase 10C needs it)
2. Has it been a few days? (Needs time to learn)
3. Are you using Alisa regularly? (Needs observations)

**Test**:
```powershell
python scripts/test_phase10c.py
```

---

### "Memory file doesn't exist"

**This is normal** on first run!

The file is created after your first session ends.

**To force creation**:
1. Use Alisa for a few minutes
2. Disconnect properly (not Ctrl+C)
3. Check: `Documents\Alisa Memory\task_memory.json`

---

### "Patterns seem wrong"

**Causes**:
- Not enough data yet (wait a few more days)
- Irregular schedule (harder to detect patterns)
- Memory file corrupted (delete and restart)

**Reset**:
```powershell
del "$env:USERPROFILE\Documents\Alisa Memory\task_memory.json"
# Then restart backend
```

---

## Advanced Usage

### Viewing Detailed Patterns

```python
from backend.app.task_memory import TaskMemorySystem

tm = TaskMemorySystem()
tm.load_memory()

# See all patterns
print(tm.patterns)

# See work schedule
print(tm.work_schedule)

# See app preferences
print(tm.app_usage)
```

---

### Manual Pattern Analysis

```python
# Analyze current data
patterns = tm.analyze_patterns()

print(f"Peak hours: {patterns['peak_coding_hours']}")
print(f"Quiet hours: {patterns['preferred_silence_hours']}")
print(f"Tasks observed: {patterns['total_tasks_observed']}")
```

---

### Testing Interrupt Logic

```python
# Test if interruption is OK right now
should, reason = tm.should_interrupt_now(600)  # 10 min silence
print(f"Should interrupt: {should}")
print(f"Reason: {reason}")
```

---

## Integration with Other Phases

### With Phase 9B (Companion)

Phase 10C **enhances** companion mode:

```
Phase 9B: "Should I speak? (10 min silence)"
    ↓
Phase 10C: "User prefers quiet at this hour"
    ↓
Result: Stay quiet
```

**Benefit**: More respectful interruptions

---

### With Phase 10A (Desktop Understanding)

Phase 10C **learns from** desktop context:

```
Phase 10A: "User coding Python in VS Code"
    ↓
Phase 10C: "Record activity: coding_python at hour 14"
    ↓
Over time: "Hour 14 is peak coding hour"
```

**Benefit**: Understanding enables learning

---

### With Phase 10B (Desktop Actions)

Phase 10C **informs** action suggestions:

```
Phase 10C: "User always opens Chrome after coding"
    ↓
User finishes coding
    ↓
Phase 10B: "Want me to open Chrome?" (proactive)
```

**Benefit**: Predictive automation

---

## What to Expect

### Week 1
- Observation mode
- Building data
- Minimal adaptation

### Week 2
- Patterns emerging
- Basic adaptation
- Respectful timing

### Week 3+
- Well-tuned behavior
- Predictive suggestions
- Feels personalized

---

## Success Indicators

You'll know Phase 10C is working when:

✅ **Alisa seems to "get" your schedule**  
✅ **Interruptions feel less intrusive**  
✅ **Suggestions are more relevant**  
✅ **She respects your focus time**  
✅ **Behavior feels natural**  

**The best learning is invisible learning.**

---

## Next Steps

### After Setup

1. **Use Alisa normally** for a week
2. **Check logs** occasionally to see learning progress
3. **View memory file** to see what's been learned
4. **Enjoy** more personalized behavior

### Going Further

- Read `PHASE_10C_IMPLEMENTATION.md` for technical details
- Check `PHASE_10C_QUICK_REF.md` for API reference
- See `PHASE_10C_VISUAL_GUIDE.md` for architecture

---

## Summary

Phase 10C is **fully automatic**:

✅ No configuration  
✅ No manual training  
✅ No explicit commands  
✅ Just observe and adapt  

**Start using Alisa, and she'll learn your patterns.**

**The final evolution has begun.**

---

**Ready to start? Just run the backend and work normally!**

```powershell
.\scripts\start_backend.ps1
```

Alisa is now learning. 🎯
