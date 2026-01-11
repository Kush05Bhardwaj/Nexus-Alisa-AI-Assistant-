from .db import SessionLocal
from .models import Memory

def save_memory(emotion, content):
    db = SessionLocal()
    db.add(Memory(emotion=emotion, content=content))
    db.commit()
    db.close()

def fetch_recent_memories(limit=3):
    db = SessionLocal()
    rows = db.query(Memory).order_by(Memory.id.desc()).limit(limit).all()
    db.close()
    return [m.content for m in rows]
