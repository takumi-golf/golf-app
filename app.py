from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib
import os
from dotenv import load_dotenv
from database import SessionLocal, Club
from datetime import datetime

# 環境変数の読み込み
load_dotenv()

app = FastAPI(
    title="Golf Fitting API",
    description="ゴルフクラブのフィッティングをサポートするAPI",
    version="1.0.0"
)

# データモデル定義
class UserProfile(BaseModel):
    height: float
    weight: float
    age: int
    gender: str
    handicap: Optional[float] = None
    head_speed: Optional[float] = None
    ball_speed: Optional[float] = None
    launch_angle: Optional[float] = None
    swing_issue: Optional[str] = None
    
class ClubRecommendation(BaseModel):
    driver: dict
    woods: List[dict]
    utilities: List[dict]
    irons: List[dict]
    wedges: List[dict]
    putter: dict
    total_price: float
    confidence_score: float
    timestamp: datetime

# AIモデルのロード
def load_models():
    models = {}
    model_paths = {
        'loft': "models/loft_model.pkl",
        'flex': "models/flex_model.pkl",
        'flex_encoder': "models/flex_label_encoder.pkl"
    }
    
    try:
        for name, path in model_paths.items():
            if os.path.exists(path):
                models[name] = joblib.load(path)
            else:
                print(f"Warning: {name} model file not found")
        return models
    except Exception as e:
        print(f"Error loading models: {str(e)}")
        return None

models = load_models()

@app.get("/")
async def root():
    return {
        "message": "ゴルフフィッティングAPIへようこそ",
        "version": "1.0.0",
        "status": "active"
    }

@app.post("/recommend", response_model=ClubRecommendation)
async def recommend_clubs(profile: UserProfile):
    if not models:
        raise HTTPException(status_code=500, detail="必要なAIモデルの一部がロードされていません")
    
    try:
        # プロファイルデータの前処理
        profile_data = preprocess_profile(profile)
        
        # クラブの推奨
        recommendations = generate_recommendations(profile_data)
        
        # 信頼度スコアの計算
        confidence_score = calculate_overall_confidence(recommendations, profile_data)
        
        return {
            **recommendations,
            "confidence_score": confidence_score,
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        print(f"Error details: {str(e)}")
        raise HTTPException(status_code=500, detail=f"レコメンデーション生成中にエラーが発生しました: {str(e)}")

def preprocess_profile(profile: UserProfile) -> Dict[str, Any]:
    return {
        'height': profile.height,
        'weight': profile.weight,
        'age': profile.age,
        'gender_encoded': 1 if profile.gender == "male" else 0,
        'handicap': profile.handicap or 20,
        'head_speed': profile.head_speed or 40,
        'ball_speed': profile.ball_speed or 60,
        'launch_angle': profile.launch_angle or 12,
        'swing_issue': profile.swing_issue
    }

def generate_recommendations(profile_data: Dict[str, Any]) -> Dict[str, Any]:
    # ロフト角を予測
    recommended_loft = float(models['loft'].predict(pd.DataFrame([profile_data]))[0])
    
    # シャフトフレックスを決定
    recommended_flex = determine_shaft_flex(profile_data['head_speed'])
    
    # データベースからクラブを取得
    clubs = get_clubs_from_database(recommended_loft, recommended_flex)
    
    # クラブセットを最適化
    optimized_set = optimize_club_set(clubs, profile_data)
    
    return optimized_set

def determine_shaft_flex(head_speed: float) -> str:
    if head_speed >= 50:
        return "X"
    elif head_speed >= 45:
        return "S"
    elif head_speed >= 40:
        return "R"
    else:
        return "A"

def get_clubs_from_database(loft: float, shaft_flex: str) -> List[Club]:
    db = SessionLocal()
    try:
        clubs = db.query(Club).filter(
            Club.is_available == True,
            Club.loft == loft,
            Club.shaft_flex == shaft_flex
        ).order_by(Club.popularity_score.desc()).all()
        return clubs
    finally:
        db.close()

def optimize_club_set(clubs: List[Club], profile_data: Dict[str, Any]) -> Dict[str, Any]:
    # クラブセットの最適化ロジック
    optimized_set = {
        "driver": select_best_club(clubs, "driver", profile_data),
        "woods": select_clubs(clubs, "wood", profile_data, limit=2),
        "utilities": select_clubs(clubs, "utility", profile_data, limit=1),
        "irons": select_clubs(clubs, "iron", profile_data, limit=7),
        "wedges": select_clubs(clubs, "wedge", profile_data, limit=2),
        "putter": select_best_club(clubs, "putter", profile_data),
        "total_price": 0
    }
    
    # 合計価格の計算
    optimized_set["total_price"] = sum(
        club["price"] for club in [
            optimized_set["driver"],
            *optimized_set["woods"],
            *optimized_set["utilities"],
            *optimized_set["irons"],
            *optimized_set["wedges"],
            optimized_set["putter"]
        ]
    )
    
    return optimized_set

def select_best_club(clubs: List[Club], club_type: str, profile_data: Dict[str, Any]) -> Dict[str, Any]:
    matching_clubs = [c for c in clubs if c.type == club_type]
    if not matching_clubs:
        return None
    
    best_club = max(matching_clubs, key=lambda c: calculate_confidence_score(profile_data, c))
    return format_club_data(best_club)

def select_clubs(clubs: List[Club], club_type: str, profile_data: Dict[str, Any], limit: int) -> List[Dict[str, Any]]:
    matching_clubs = [c for c in clubs if c.type == club_type]
    if not matching_clubs:
        return []
    
    sorted_clubs = sorted(matching_clubs, key=lambda c: calculate_confidence_score(profile_data, c), reverse=True)
    return [format_club_data(c) for c in sorted_clubs[:limit]]

def format_club_data(club: Club) -> Dict[str, Any]:
    return {
        "club_id": club.id,
        "brand": club.brand,
        "model": club.model,
        "loft": club.loft,
        "shaft": club.shaft,
        "shaft_flex": club.shaft_flex,
        "price": club.price,
        "features": club.features
    }

def calculate_confidence_score(profile_data: Dict[str, Any], club: Club) -> float:
    base_score = 0.5
    
    # ヘッドスピードとシャフトの硬さの一致度
    if profile_data['head_speed'] >= 40 and club.shaft_flex == "S":
        base_score += 0.2
    elif profile_data['head_speed'] < 40 and club.shaft_flex == "R":
        base_score += 0.2
        
    # 人気度スコアの考慮
    base_score += (club.popularity_score / 100) * 0.3
    
    return min(base_score, 1.0)

def calculate_overall_confidence(recommendations: Dict[str, Any], profile_data: Dict[str, Any]) -> float:
    # 全推奨クラブの信頼度スコアの平均を計算
    confidence_scores = []
    
    for club_type in ["driver", "woods", "utilities", "irons", "wedges", "putter"]:
        clubs = recommendations[club_type]
        if isinstance(clubs, list):
            confidence_scores.extend([c.get("confidence_score", 0) for c in clubs])
        else:
            confidence_scores.append(clubs.get("confidence_score", 0))
    
    return sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0 