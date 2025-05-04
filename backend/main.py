from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Union
import uvicorn

# FastAPIアプリケーションの初期化
app = FastAPI(
    title="Golf Club Recommendation API",
    description="ゴルフクラブのレコメンデーションAPI",
    version="1.0.0"
)

# CORSの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # フロントエンドのURL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# モデルの定義
class ClubRecommendation(BaseModel):
    club_type: str
    brand: str
    model: str
    loft: float
    shaft: str
    flex: str
    description: str

class UserProfile(BaseModel):
    height: Union[int, str] = Field(..., description="身長（cm）")
    weight: Union[int, str] = Field(..., description="体重（kg）")
    age: Union[int, str] = Field(..., description="年齢")
    gender: str = Field(..., description="性別")
    handicap: Union[int, str] = Field(..., description="ハンディキャップ")
    swing_speed: Optional[Union[float, str]] = Field(None, description="スイングスピード（mph）")
    ball_speed: Optional[Union[float, str]] = Field(None, description="ボールスピード（mph）")
    launch_angle: Optional[Union[float, str]] = Field(None, description="打ち出し角（度）")
    spin_rate: Optional[Union[float, str]] = Field(None, description="スピン量（rpm）")
    preferred_brands: Optional[List[str]] = Field(None, description="希望ブランド")
    budget: Optional[Union[float, str]] = Field(None, description="予算（円）")

    def __init__(self, **data):
        # 文字列を数値に変換
        for field in ['height', 'weight', 'age', 'handicap']:
            if field in data and isinstance(data[field], str):
                data[field] = int(data[field])
        for field in ['swing_speed', 'ball_speed', 'launch_angle', 'spin_rate', 'budget']:
            if field in data and data[field] is not None and isinstance(data[field], str):
                data[field] = float(data[field])
        super().__init__(**data)

# サンプルデータ
SAMPLE_CLUBS = [
    ClubRecommendation(
        club_type="Driver",
        brand="Titleist",
        model="TSR3",
        loft=9.0,
        shaft="HZRDUS Smoke Red",
        flex="Stiff",
        description="低スピンで高弾道のドライバー"
    ),
    ClubRecommendation(
        club_type="Driver",
        brand="Callaway",
        model="Paradym",
        loft=10.5,
        shaft="Tensei AV Blue",
        flex="Regular",
        description="高容錯性で安定した飛距離を実現"
    )
]

@app.get("/")
async def root():
    return {"message": "Golf Club Recommendation API"}

@app.get("/api/clubs", response_model=List[ClubRecommendation])
async def get_clubs():
    return SAMPLE_CLUBS

@app.get("/api/clubs/{club_type}", response_model=List[ClubRecommendation])
async def get_clubs_by_type(club_type: str):
    filtered_clubs = [club for club in SAMPLE_CLUBS if club.club_type.lower() == club_type.lower()]
    if not filtered_clubs:
        raise HTTPException(status_code=404, detail=f"No clubs found of type {club_type}")
    return filtered_clubs

@app.post("/api/recommendations/", response_model=List[ClubRecommendation])
async def get_recommendations(user_profile: UserProfile):
    # ここで実際のレコメンデーションロジックを実装
    # 現在はサンプルデータを返す
    recommendations = []
    
    # ハンディキャップに基づいてクラブを選択
    if user_profile.handicap > 15:
        # 高ハンディキャップ向けのクラブ
        recommendations.append(ClubRecommendation(
            club_type="Driver",
            brand="Callaway",
            model="Paradym",
            loft=10.5,
            shaft="Tensei AV Blue",
            flex="Regular",
            description="高容錯性で安定した飛距離を実現"
        ))
    else:
        # 低ハンディキャップ向けのクラブ
        recommendations.append(ClubRecommendation(
            club_type="Driver",
            brand="Titleist",
            model="TSR3",
            loft=9.0,
            shaft="HZRDUS Smoke Red",
            flex="Stiff",
            description="低スピンで高弾道のドライバー"
        ))
    
    return recommendations

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True) 
