from pydantic import BaseModel
from typing import Optional, List

class ChatMessage(BaseModel):
    prompt: str
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 2048
    stop: Optional[List[str]] = []

class ChatResponse(BaseModel):
    type: str
    content: Optional[str] = None

class HealthCheck(BaseModel):
    status: str
