from sqlalchemy import Column, Integer, String, Text
from .db import Base

class Memory(Base):
    __tablename__ = "memory"

    id = Column(Integer, primary_key=True)
    emotion = Column(String)
    content = Column(Text)
