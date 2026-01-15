from .db import SessionLocal
from .models import ConversationHistory
from datetime import datetime

class MemoryBuffer:
    """
    Conversation history manager with persistent storage and token limits.
    Keeps recent messages in memory and persists to database.
    """
    def __init__(self, max_turns=10, max_tokens=3000, session_id="default"):
        """
        Args:
            max_turns: Maximum number of conversation turns to keep in memory
            max_tokens: Approximate token limit (roughly 4 chars = 1 token)
            session_id: Session identifier for multi-user support
        """
        self.max_turns = max_turns
        self.max_tokens = max_tokens
        self.session_id = session_id
        self.messages = []
        self._load_from_db()

    def _estimate_tokens(self, text):
        """Rough token estimation: ~4 characters per token"""
        return len(text) // 4

    def _load_from_db(self):
        """Load recent conversation history from database"""
        try:
            db = SessionLocal()
            # Load recent messages for this session
            rows = (
                db.query(ConversationHistory)
                .filter(ConversationHistory.session_id == self.session_id)
                .order_by(ConversationHistory.timestamp.desc())
                .limit(self.max_turns * 2)  # User + assistant = 2 messages per turn
                .all()
            )
            # Reverse to get chronological order
            self.messages = [
                {"role": row.role, "content": row.content}
                for row in reversed(rows)
            ]
            db.close()
            print(f"📚 Loaded {len(self.messages)} messages from history")
        except Exception as e:
            print(f"⚠️ Could not load history from DB: {e}")
            self.messages = []

    def add(self, role, content):
        """Add a message to history and persist to database"""
        message = {"role": role, "content": content}
        self.messages.append(message)
        
        # Persist to database
        try:
            db = SessionLocal()
            db.add(ConversationHistory(
                role=role,
                content=content,
                session_id=self.session_id,
                timestamp=datetime.utcnow()
            ))
            db.commit()
            db.close()
        except Exception as e:
            print(f"⚠️ Could not save to DB: {e}")
        
        # Trim by token count
        self._trim_by_tokens()
        
        # Also trim by turn count as backup
        if len(self.messages) > self.max_turns * 2:
            self.messages = self.messages[-self.max_turns * 2:]

    def _trim_by_tokens(self):
        """Keep messages within token limit by removing oldest"""
        while len(self.messages) > 2:  # Keep at least 1 turn
            total_tokens = sum(self._estimate_tokens(m["content"]) for m in self.messages)
            if total_tokens <= self.max_tokens:
                break
            # Remove oldest message
            self.messages.pop(0)

    def get(self):
        """Get current conversation history"""
        return self.messages

    def clear(self):
        """Clear conversation history (in-memory only, keeps DB)"""
        self.messages = []
        print("🗑️ Conversation history cleared")
    
    def get_summary(self):
        """Get a summary of current conversation state"""
        total_messages = len(self.messages)
        total_tokens = sum(self._estimate_tokens(m["content"]) for m in self.messages)
        return {
            "messages": total_messages,
            "turns": total_messages // 2,
            "estimated_tokens": total_tokens,
            "max_tokens": self.max_tokens
        }
