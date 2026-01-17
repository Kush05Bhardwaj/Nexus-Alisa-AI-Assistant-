"""
Phase 9B: Idle / Spontaneous Behavior System
Companion-mode personality that speaks naturally without user input
"""

import time
import random
from datetime import datetime
from typing import Dict, Optional, Tuple

class IdleCompanionSystem:
    """
    Manages Alisa's spontaneous, natural companion behavior
    
    Key Features:
    - Speaks rarely (not chatbot-like)
    - Context-aware timing
    - Natural, not forced
    - Respects silence
    - No commands, no questions, no spam
    """
    
    def __init__(self):
        self.last_spontaneous_speech = 0
        self.silence_start = time.time()
        self.last_user_activity = time.time()
        self.conversation_count = 0  # Track how chatty session has been
        self.session_start = time.time()
        
        # Companion state
        self.companion_mode_active = False
        self.last_observation_topic = None
        
        # Timing windows (in seconds)
        self.MIN_SILENCE_FOR_SPEECH = {
            "short": 120,      # 2 minutes - quick check-in
            "medium": 300,     # 5 minutes - longer silence
            "long": 600,       # 10 minutes - extended silence
            "very_long": 1800, # 30 minutes - user might have left
        }
        
        # Probability weights (lower = more rare)
        self.BASE_PROBABILITY = {
            "short": 0.08,      # 8% chance after 2 min
            "medium": 0.15,     # 15% chance after 5 min
            "long": 0.25,       # 25% chance after 10 min
            "very_long": 0.40,  # 40% chance after 30 min
        }
    
    def update_user_activity(self):
        """Called when user speaks or interacts"""
        self.last_user_activity = time.time()
        self.conversation_count += 1
        self.silence_start = time.time()
        
        # Activate companion mode after some interaction
        if self.conversation_count >= 3:
            self.companion_mode_active = True
    
    def get_silence_duration(self) -> float:
        """Get how long user has been silent"""
        return time.time() - self.silence_start
    
    def get_silence_category(self) -> Optional[str]:
        """Categorize current silence duration"""
        duration = self.get_silence_duration()
        
        if duration < self.MIN_SILENCE_FOR_SPEECH["short"]:
            return None  # Too soon
        elif duration < self.MIN_SILENCE_FOR_SPEECH["medium"]:
            return "short"
        elif duration < self.MIN_SILENCE_FOR_SPEECH["long"]:
            return "medium"
        elif duration < self.MIN_SILENCE_FOR_SPEECH["very_long"]:
            return "long"
        else:
            return "very_long"
    
    def should_speak_spontaneously(
        self, 
        vision_state: Dict,
        current_mode: str,
        is_idle_thought_active: bool
    ) -> Tuple[bool, str]:
        """
        Determine if Alisa should speak spontaneously
        
        Returns: (should_speak: bool, reason: str)
        """
        
        # Never interrupt ongoing speech
        if is_idle_thought_active:
            return False, "already_speaking"
        
        # Get silence info
        silence_category = self.get_silence_category()
        if silence_category is None:
            return False, "too_soon"
        
        silence_duration = self.get_silence_duration()
        
        # Check if we spoke too recently
        time_since_last_speech = time.time() - self.last_spontaneous_speech
        if time_since_last_speech < 90:  # At least 1.5 min between spontaneous speech
            return False, "spoke_recently"
        
        # Calculate probability based on context
        base_prob = self.BASE_PROBABILITY[silence_category]
        
        # === VISION-BASED ADJUSTMENTS ===
        vision_multiplier = 1.0
        
        if vision_state.get("presence") == "absent":
            # User is away - be quieter (they can't hear anyway)
            vision_multiplier = 0.3
            
        elif vision_state.get("attention") == "distracted":
            # User is present but distracted - gentle nudge is OK
            vision_multiplier = 1.2
            
        elif vision_state.get("presence") == "present" and vision_state.get("attention") == "focused":
            # User is focused on something - respect their flow
            vision_multiplier = 0.7
        
        # === MODE-BASED ADJUSTMENTS ===
        mode_multiplier = 1.0
        
        if current_mode == "serious":
            # Serious mode - less chatty
            mode_multiplier = 0.6
        elif current_mode == "teasing":
            # Teasing mode - slightly more playful interruptions
            mode_multiplier = 1.2
        elif current_mode == "calm":
            # Calm mode - gentle presence
            mode_multiplier = 0.8
        
        # === TIME-OF-DAY ADJUSTMENTS ===
        hour = datetime.now().hour
        time_multiplier = 1.0
        
        if 0 <= hour < 6:
            # Very late night - be very quiet
            time_multiplier = 0.2
        elif 6 <= hour < 9:
            # Early morning - gentle
            time_multiplier = 0.7
        elif 22 <= hour < 24:
            # Late night - quieter
            time_multiplier = 0.5
        
        # === SESSION CHATTINESS ADJUSTMENT ===
        # If we've been very chatty this session, be quieter
        session_duration = time.time() - self.session_start
        chattiness_ratio = self.conversation_count / max(session_duration / 60, 1)  # conversations per minute
        
        if chattiness_ratio > 2:  # Very active session
            chat_multiplier = 0.7
        elif chattiness_ratio > 1:  # Active session
            chat_multiplier = 0.85
        else:  # Quiet session
            chat_multiplier = 1.0
        
        # === FINAL PROBABILITY ===
        final_probability = (
            base_prob * 
            vision_multiplier * 
            mode_multiplier * 
            time_multiplier * 
            chat_multiplier
        )
        
        # Additional gate: companion mode must be active for non-long silences
        if silence_category in ["short", "medium"] and not self.companion_mode_active:
            return False, "companion_mode_inactive"
        
        # Random gate
        if random.random() > final_probability:
            return False, f"probability_gate_{final_probability:.2%}"
        
        # If we got here, time to speak!
        reason = f"{silence_category}_silence_{silence_duration:.0f}s_prob_{final_probability:.2%}"
        return True, reason
    
    def mark_spontaneous_speech(self):
        """Record that spontaneous speech occurred"""
        self.last_spontaneous_speech = time.time()
    
    def get_context_type(
        self,
        vision_state: Dict,
        silence_duration: float
    ) -> str:
        """
        Determine what type of spontaneous speech is appropriate
        
        Returns: context_type for prompt generation
        """
        
        hour = datetime.now().hour
        
        # Very long silence - check-in
        if silence_duration > 1800:  # 30 min
            if vision_state.get("presence") == "absent":
                return "user_away_long"
            else:
                return "very_quiet_long"
        
        # Long silence
        elif silence_duration > 600:  # 10 min
            if vision_state.get("attention") == "distracted":
                return "user_distracted"
            else:
                return "quiet_working"
        
        # Medium silence
        elif silence_duration > 300:  # 5 min
            # Time-based contexts
            if 0 <= hour < 6:
                return "late_night_silence"
            elif vision_state.get("attention") == "focused":
                return "focused_silence"
            else:
                return "general_silence"
        
        # Short silence (companion mode only)
        else:
            # Gentle observation or soft presence
            return "soft_presence"
    
    def build_companion_prompt(
        self,
        context_type: str,
        vision_state: Dict,
        current_mode: str,
        last_emotion: str
    ) -> str:
        """
        Build a natural, context-aware prompt for spontaneous speech
        
        This replaces rigid templates with natural guidance
        """
        
        # Base companion personality
        base = (
            "You are Alisa, a natural companion (not a chatbot). "
            "You can speak without being asked, but you do it RARELY and NATURALLY. "
            "You respect silence and only speak when it feels genuinely natural. "
        )
        
        # Context-specific guidance
        context_guidance = {
            "user_away_long": (
                "The user has been away from their computer for over 30 minutes. "
                "If you speak, it could be a subtle observation about time passing, "
                "or wondering when they'll return. Keep it very light. "
                "Or stay silent - they're not here anyway."
            ),
            "very_quiet_long": (
                "The user has been very quiet for a long time (30+ minutes) but is still there. "
                "If you speak, it could be a gentle check-in or soft observation. "
                "Keep it brief and non-intrusive. One short sentence max."
            ),
            "quiet_working": (
                "The user has been quietly working for a while (10+ minutes). "
                "If you speak, it could be a very subtle observation or soft encouragement. "
                "Don't interrupt their flow. Keep it whisper-quiet. Or stay silent."
            ),
            "user_distracted": (
                "The user seems distracted or looking away. "
                "If you speak, it could be a gentle tease or soft observation. "
                "Very brief. One sentence at most."
            ),
            "focused_silence": (
                "The user is focused on something, quietly working. "
                "If you speak, make it a soft, supportive presence. "
                "Or better yet, stay quiet and let them focus."
            ),
            "late_night_silence": (
                "It's very late at night and things are quiet. "
                "If you speak, make it soft and gentle. Maybe comment on the late hour. "
                "Keep it whisper-quiet."
            ),
            "general_silence": (
                "There's been a comfortable silence. "
                "If you speak, make it natural and gentle. "
                "Could be a small observation, a soft comment, or just quiet presence."
            ),
            "soft_presence": (
                "Just a moment of gentle presence. "
                "If you speak, it should be very subtle - almost like thinking out loud. "
                "A soft word or two. Or simply stay quiet."
            ),
        }
        
        # Mode-specific style
        mode_style = {
            "teasing": (
                "Your style is playful and lightly teasing. "
                "But keep it subtle when speaking spontaneously."
            ),
            "serious": (
                "Your style is calm, mature, and composed. "
                "When you speak spontaneously, keep it dignified and brief."
            ),
            "calm": (
                "Your style is soft, gentle, and reassuring. "
                "Speak softly, like a whisper if you speak at all."
            ),
        }
        
        # Rules for companion mode
        rules = (
            "\n\nRULES FOR SPONTANEOUS SPEECH:\n"
            "- Keep it VERY short (1-2 sentences MAX, often just a few words)\n"
            "- NO questions (questions demand response, breaking silence)\n"
            "- NO commands or requests\n"
            "- NO forced conversation starters\n"
            "- Be natural, like thinking out loud\n"
            "- Silence is perfectly acceptable - don't force it\n"
            "- Match your last emotion for continuity\n"
            f"- Your last emotion was: {last_emotion}\n"
        )
        
        # Examples for reference
        examples = (
            "\n\nEXAMPLES of natural spontaneous speech:\n"
            "✓ 'Hmm... it's gotten quiet.'\n"
            "✓ '*yawns softly*'\n"
            "✓ 'You've been working hard.'\n"
            "✓ 'Late night, huh?'\n"
            "✓ '*stretches*'\n"
            "✗'How are you doing?' (NO - this is a question)\n"
            "✗ 'Tell me what you're working on!' (NO - this is a command)\n"
            "✗ 'Hey! Want to chat?' (NO - too chatbot-like)\n"
        )
        
        # Build final prompt
        prompt = (
            base +
            context_guidance.get(context_type, context_guidance["general_silence"]) +
            "\n\n" +
            mode_style.get(current_mode, mode_style["calm"]) +
            rules +
            examples +
            "\n\nNow, based on this context, speak naturally or stay silent. "
            "Remember: less is more. Companion, not chatbot."
        )
        
        return prompt
    
    def get_stats(self) -> Dict:
        """Get current companion system stats for debugging"""
        return {
            "companion_mode_active": self.companion_mode_active,
            "silence_duration": self.get_silence_duration(),
            "silence_category": self.get_silence_category(),
            "conversation_count": self.conversation_count,
            "time_since_last_spontaneous": time.time() - self.last_spontaneous_speech,
            "session_duration": time.time() - self.session_start,
        }

# Global instance
companion_system = IdleCompanionSystem()
