from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any

app = FastAPI()

# CORSの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.post("/recommend")
async def recommend_clubs(user_data: UserData) -> Dict[str, Any]:
    # ダミーデータを返す
    return {
        "total_price": 300000,
        "driver": {
            "recommended_models": [{
                "brand": "Titleist",
                "model": "TSi3",
                "price": 50000,
                "shaft": "Diamana",
                "shaft_flex": "S",
                "features": "低スピン設計で安定した飛距離を実現"
            }]
        },
        "woods": [{
            "brand": "Titleist",
            "model": "TSi2",
            "price": 40000,
            "loft": 15,
            "shaft": "Diamana",
            "shaft_flex": "S",
            "features": "高弾道で着地性が良い"
        }],
        "irons": [{
            "brand": "Titleist",
            "model": "T200",
            "price": 120000,
            "club": "アイアン4",
            "shaft": "Dynamic Gold",
            "shaft_flex": "S",
            "features": "フォルジングで打感が良い"
        }],
        "wedges": [{
            "brand": "Titleist",
            "model": "Vokey SM8",
            "price": 20000,
            "club": "ウェッジピッチング",
            "shaft": "Dynamic Gold",
            "shaft_flex": "S",
            "features": "スピン性能が高い"
        }],
        "putter": {
            "brand": "Scotty Cameron",
            "model": "Special Select",
            "price": 50000,
            "features": "安定したストロークが可能"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 