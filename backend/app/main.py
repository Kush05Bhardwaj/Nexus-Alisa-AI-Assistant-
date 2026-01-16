from fastapi import FastAPI, WebSocket
from .ws import websocket_chat, idle_thought_loop
from .db import engine, Base
import asyncio

# Create database tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Alisa Core Backend")

# Global task for idle thought loop
idle_task = None

@app.on_event("startup")
async def startup_event():
    """Start background tasks when app starts"""
    global idle_task
    idle_task = asyncio.create_task(idle_thought_loop())
    print("🚀 Idle thought engine initialized")

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up background tasks when app stops"""
    global idle_task
    if idle_task:
        idle_task.cancel()
        print("🛑 Idle thought engine stopped")

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
