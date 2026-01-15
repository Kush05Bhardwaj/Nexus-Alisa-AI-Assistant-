from fastapi import FastAPI, WebSocket
from .ws import websocket_chat

app = FastAPI(title="Alisa Core Backend")

@app.websocket("/ws/chat")
async def chat_ws(websocket: WebSocket):
    await websocket_chat(websocket)

@app.get("/")
def root():
    return {"status": "Alisa online"}
