from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

app = FastAPI()

# قائمة لتتبع اتصالات اللاعبين النشطة عبر الـ WebSocket
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, data: str):
        for connection in self.active_connections:
            await connection.send_text(data)

manager = ConnectionManager()

# قائمة اللاعبين المتصلين لعرضهم في اللانشر
connected_players = []

@app.get("/")
def home():
    return {"status": "RdrOne Master Server is Online & Live!"}

# 1. هذا هو المسار الضروري ليظهر السيرفر في قائمة اللانشر
@app.get("/servers")
def get_servers():
    current_players_count = len(connected_players)
    servers_database = [
        {
            "name": "RdrOne Official Arabic Server",
            "players": f"{current_players_count}/100",
            "ping": "24ms",
            "ip": "play.rdrone.com",
            "port": 7777
        }
    ]
    return servers_database

@app.post("/connect")
def player_connect(data: dict):
    name = data.get("name")
    if name and name not in connected_players:
        connected_players.append(name)
    return {"message": "Connected", "total_players": len(connected_players)}

@app.post("/disconnect")
def player_disconnect(data: dict):
    name = data.get("name")
    if name in connected_players:
        connected_players.remove(name)
    return {"message": "Disconnected"}

# 2. مسار الـ WebSocket المخصص لحركة اللاعبين لاحقاً
@app.websocket("/ws/{player_name}")
async def websocket_endpoint(websocket: WebSocket, player_name: str):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"{player_name}:{data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"System:{player_name} disconnected.")
