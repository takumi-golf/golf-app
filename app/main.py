from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from config import DATABASE_URL
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# データベース接続の設定
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# データベースモデルの定義
class Club(Base):
    __tablename__ = "clubs"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String)
    model = Column(String)
    type = Column(String)
    loft = Column(Float)
    shaft = Column(String)
    shaft_flex = Column(String)
    price = Column(Integer)
    features = Column(String)
    trajectory = Column(String)
    spin = Column(String)
    forgiveness = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Pydanticモデルの定義
class UserData(BaseModel):
    height: int
    weight: int
    age: int
    gender: str
    handicap: Optional[int] = None
    average_score: Optional[int] = None
    head_speed: Optional[float] = None
    ball_speed: Optional[float] = None
    launch_angle: Optional[float] = None
    swing_issue: Optional[str] = None
    budget_preference: str

class ClubResponse(BaseModel):
    id: int
    brand: str
    model: str
    type: str
    loft: float
    shaft: str
    shaft_flex: str
    price: int
    features: str
    trajectory: str
    spin: str
    forgiveness: str

    class Config:
        orm_mode = True

app = FastAPI()

# CORSミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静的ファイルの設定
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# データベース接続情報
DB_CONFIG = {
    "dbname": "golf_db",
    "user": "postgres",
    "password": "WecA4JagjpsziLi2_N9g",
    "host": "localhost",
    "port": "5432"
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

@app.get("/")
async def root():
    return FileResponse("app/templates/index.html")

@app.get("/api/manufacturers")
async def get_manufacturers():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM manufacturers")
        manufacturers = cur.fetchall()
        cur.close()
        conn.close()
        return [{"id": m[0], "name": m[1], "created_at": m[2]} for m in manufacturers]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/clubs")
async def get_clubs():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT c.id, m.name, c.model, c.head_volume, c.price, c.features
            FROM clubs c
            JOIN manufacturers m ON c.manufacturer_id = m.id
        """)
        clubs = cur.fetchall()
        cur.close()
        conn.close()
        return [{
            "id": c[0],
            "manufacturer": c[1],
            "model": c[2],
            "head_volume": c[3],
            "price": c[4],
            "features": c[5]
        } for c in clubs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/lofts")
async def get_lofts():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT l.id, c.model, l.loft
            FROM lofts l
            JOIN clubs c ON l.club_id = c.id
            ORDER BY c.model, l.loft
        """)
        lofts = cur.fetchall()
        cur.close()
        conn.close()
        return [{"id": l[0], "model": l[1], "loft": l[2]} for l in lofts]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/shafts")
async def get_shafts():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT s.id, c.model, s.shaft
            FROM shafts s
            JOIN clubs c ON s.club_id = c.id
            ORDER BY c.model, s.shaft
        """)
        shafts = cur.fetchall()
        cur.close()
        conn.close()
        return [{"id": s[0], "model": s[1], "shaft": s[2]} for s in shafts]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/flexes")
async def get_flexes():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT f.id, c.model, f.flex
            FROM flexes f
            JOIN clubs c ON f.club_id = c.id
            ORDER BY c.model, f.flex
        """)
        flexes = cur.fetchall()
        cur.close()
        conn.close()
        return [{"id": f[0], "model": f[1], "flex": f[2]} for f in flexes]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/clubs", response_model=List[ClubResponse])
def get_clubs_from_db():
    db = SessionLocal()
    try:
        clubs = db.query(Club).all()
        return clubs
    finally:
        db.close()

@app.get("/api/clubs/{club_id}", response_model=ClubResponse)
def get_club(club_id: int):
    db = SessionLocal()
    try:
        club = db.query(Club).filter(Club.id == club_id).first()
        if club is None:
            raise HTTPException(status_code=404, detail="Club not found")
        return club
    finally:
        db.close()

@app.post("/recommend")
async def recommend_clubs(user_data: UserData) -> Dict[str, Any]:
    db = SessionLocal()
    try:
        # データベースからクラブを取得
        clubs = db.query(Club).all()
        
        # ユーザーのデータに基づいてクラブを選択
        recommended_clubs = {
            "total_price": 0,
            "driver": {
                "recommended_models": []
            },
            "woods": [],
            "irons": [],
            "wedges": [],
            "putter": None
        }
        
        # ドライバーの選択
        driver = next((club for club in clubs if club.type == "driver"), None)
        if driver:
            recommended_clubs["driver"]["recommended_models"].append({
                "brand": driver.brand,
                "model": driver.model,
                "price": driver.price,
                "shaft": driver.shaft,
                "shaft_flex": driver.shaft_flex,
                "features": driver.features
            })
            recommended_clubs["total_price"] += driver.price
        
        # フェアウェイウッドの選択
        woods = [club for club in clubs if club.type == "wood"]
        for wood in woods:
            recommended_clubs["woods"].append({
                "brand": wood.brand,
                "model": wood.model,
                "price": wood.price,
                "loft": wood.loft,
                "shaft": wood.shaft,
                "shaft_flex": wood.shaft_flex,
                "features": wood.features
            })
            recommended_clubs["total_price"] += wood.price
        
        # アイアンの選択
        irons = [club for club in clubs if club.type == "iron"]
        for iron in irons:
            recommended_clubs["irons"].append({
                "brand": iron.brand,
                "model": iron.model,
                "price": iron.price,
                "club": f"アイアン{int(iron.loft)}",
                "shaft": iron.shaft,
                "shaft_flex": iron.shaft_flex,
                "features": iron.features
            })
            recommended_clubs["total_price"] += iron.price
        
        # ウェッジの選択
        wedges = [club for club in clubs if club.type == "wedge"]
        for wedge in wedges:
            recommended_clubs["wedges"].append({
                "brand": wedge.brand,
                "model": wedge.model,
                "price": wedge.price,
                "club": f"ウェッジ{int(wedge.loft)}",
                "shaft": wedge.shaft,
                "shaft_flex": wedge.shaft_flex,
                "features": wedge.features
            })
            recommended_clubs["total_price"] += wedge.price
        
        # パターの選択
        putter = next((club for club in clubs if club.type == "putter"), None)
        if putter:
            recommended_clubs["putter"] = {
                "brand": putter.brand,
                "model": putter.model,
                "price": putter.price,
                "features": putter.features
            }
            recommended_clubs["total_price"] += putter.price
        
        return recommended_clubs
    finally:
        db.close()

# 環境変数の読み込み
load_dotenv()

# ボットの初期化
app = App(token=os.getenv("SLACK_BOT_TOKEN"))

# メッセージの処理
@app.message(".*")
def handle_message(message, say):
    # メッセージの内容を取得
    text = message.get('text', '')
    user = message.get('user', '')
    channel = message.get('channel', '')
    
    # メッセージに対する応答
    response = f"<@{user}> メッセージを受け取りました: {text}"
    say(response)

# ボットへのメンションに対する処理
@app.event("app_mention")
def handle_mention(event, say):
    text = event.get('text', '')
    user = event.get('user', '')
    say(f"<@{user}> メンションありがとうございます！")

if __name__ == "__main__":
    # Socket Modeハンドラーの起動
    handler = SocketModeHandler(app_token=os.getenv("SLACK_APP_TOKEN"))
    handler.start()

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 