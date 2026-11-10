from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# قائمة اللاعبين المتصلين حالياً بالفععل
connected_players = []

class PlayerConnection(implements := BaseModel):
    name: str
    server_name: str

@app.get("/")
def home():
    return {"status": "RdrOne Master Server is Online & Live!"}

# جلب قائمة السيرفرات مع حساب عدد اللاعبين الحقيقيين تلقائياً
@app.get("/servers")
def get_servers():
    current_players_count = len(connected_players)
    
    servers_database = [
        {
            "name": "RdrOne Official Arabic Server",
            "players": f"{current_players_count}/100",  # العدد أصبح حقيقياً وحياً!
            "ping": "24ms",  # يمكن ربطه بقياس حقيقي لاحقاً
            "ip": "play.rdrone.com",
            "port": 7777
        }
    ]
    return servers_database

# نقطة استقبال اللاعبين عندما يضغطون على زر Connect
@app.post("/connect")
def player_connect(data: PlayerConnection):
    if data.name not in connected_players:
        connected_players.append(data.name)
    return {"message": f"Player {data.name} joined successfully!", "total_players": len(connected_players)}

# نقطة خروج اللاعبين
@app.post("/disconnect")
def player_disconnect(data: PlayerConnection):
    if data.name in connected_players:
        connected_players.remove(data.name)
    return {"message": f"Player {data.name} left."}
