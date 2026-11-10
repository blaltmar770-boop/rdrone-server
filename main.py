from fastapi import FastAPI

app = FastAPI()

# قائمة السيرفرات الخاصة بك (سيرفر واحد رئيسي يستسع 100 لاعب)
servers_database = [
    {
        "name": "RdrOne Official Arabic Server",
        "players": "45/100",  # هنا يظهر عدد اللاعبين الحالي من أصل 100
        "ping": "28ms",
        "ip": "play.rdrone.com", # رابط أو آيبان السيرفر الحقيقي مستقبلاً
        "port": 7777
    }
]

@app.get("/")
def home():
    return {"status": "RdrOne Master Server is Online!"}

@app.get("/servers")
def get_servers():
    # هذا الرابط هو الذي سيسحبه لانشر RdrOne لعرض السيرفرات للمستخدمين
    return servers_database