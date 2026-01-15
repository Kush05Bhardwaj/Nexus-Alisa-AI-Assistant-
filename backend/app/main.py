from fastapi import FastAPI, WebSocket
from .ws import websocket_chat
from .db import engine, Base

# Create database tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Alisa Core Backend")

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
