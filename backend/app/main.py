from fastapi import FastAPI, WebSocket
from .ws import websocket_chat, idle_thought_loop
from .db import engine, Base
from pydantic import BaseModel
import asyncio
from contextlib import asynccontextmanager

# Create database tables on startup
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan events"""
    # Startup
    idle_task = asyncio.create_task(idle_thought_loop())
    print("🚀 Idle thought engine initialized")
    
    yield
    
    # Shutdown
    idle_task.cancel()
    print("🛑 Idle thought engine stopped")

app = FastAPI(title="Alisa Core Backend", lifespan=lifespan)

# Message schema for API
class MessageSchema(BaseModel):
    text: str

@app.websocket("/ws/chat")
async def chat_ws(websocket: WebSocket):
    await websocket_chat(websocket)

@app.get("/")
def root():
    return {"status": "Alisa online"}

@app.get("/history/summary")
def get_history_summary():
    """Get conversation history summary"""
    from .memory import memory
    return memory.get_summary()

@app.post("/history/clear")
def clear_history():
    """Clear conversation history (in-memory only)"""
    from .memory import memory
    memory.clear()
    return {"status": "History cleared"}

@app.post("/normalize_hinglish/")
async def normalize_hinglish(payload: MessageSchema):
    from .llm import llm_server
    prompt = f"""
    Rewrite this into natural conversational Hinglish:
    {payload.text}
    """
    response = llm_server.generate(prompt)
    return {"text": response}
