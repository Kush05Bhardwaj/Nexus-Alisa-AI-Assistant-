from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from .db import Base

class Memory(Base):
    __tablename__ = "memory"

    id = Column(Integer, primary_key=True)
    emotion = Column(String)
    content = Column(Text)

class ConversationHistory(Base):
    """Persistent conversation history storage"""
    __tablename__ = "conversation_history"
    
    id = Column(Integer, primary_key=True, index=True)
    role = Column(String, nullable=False)  # "user" or "assistant"
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    session_id = Column(String, default="default")  # For multi-user support later
