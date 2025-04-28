from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib
import os
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

app = FastAPI(title="Golf Fitting API")

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
    
class ClubRecommendation(BaseModel):
    driver: dict
    woods: List[dict]
    utilities: List[dict]
    irons: List[dict]
    wedges: List[dict]
    putter: dict
    total_price: float

# AIモデルのロード
loft_model_path = "models/loft_model.pkl"
flex_model_path = "models/flex_model.pkl"
flex_encoder_path = "models/flex_label_encoder.pkl"

loft_model = None
flex_model = None
flex_encoder = None

if os.path.exists(loft_model_path) and os.path.exists(flex_model_path) and os.path.exists(flex_encoder_path):
    loft_model = joblib.load(loft_model_path)
    flex_model = joblib.load(flex_model_path)
    flex_encoder = joblib.load(flex_encoder_path)
else:
    print("Warning: One or more model files not found")

@app.get("/")
async def root():
    return {"message": "ゴルフフィッティングAPIへようこそ"}

@app.post("/recommend", response_model=ClubRecommendation)
async def recommend_clubs(profile: UserProfile):
    if loft_model is None or flex_model is None or flex_encoder is None:
        raise HTTPException(status_code=500, detail="必要なAIモデルの一部がロードされていません")
    
    try:
        # プロファイルデータを前処理
        profile_data = pd.DataFrame([{
            'height': profile.height,
            'weight': profile.weight,
            'age': profile.age,
            'gender_encoded': 1 if profile.gender == "male" else 0,
            'handicap': profile.handicap or 20,  # デフォルト値
            'head_speed': profile.head_speed or 40,
            'ball_speed': profile.ball_speed or 60,
            'launch_angle': profile.launch_angle or 12
        }])
        
        # ロフト角を予測
        recommended_loft = float(loft_model.predict(profile_data)[0])
        
        # ヘッドスピードに基づいてシャフトフレックスを決定
        head_speed = profile.head_speed or 40
        if head_speed >= 50:
            recommended_flex = "X"
        elif head_speed >= 45:
            recommended_flex = "S"
        elif head_speed >= 40:
            recommended_flex = "R"
        else:
            recommended_flex = "A"
        
        # レスポンス形式を修正
        response = {
            "driver": {
                "club": "ドライバー",
                "loft": recommended_loft,
                "shaft_flex": recommended_flex,
                "recommended_models": [
                    {
                        "brand": "タイトリスト",
                        "model": "TSR3",
                        "loft": recommended_loft,
                        "shaft": "Ventus Blue",
                        "shaft_flex": recommended_flex,
                        "price": 55000,
                        "features": "低スピン設計、高弾道"
                    },
                    {
                        "brand": "キャロウェイ",
                        "model": "Paradym",
                        "loft": recommended_loft,
                        "shaft": "HZRDUS Black",
                        "shaft_flex": recommended_flex,
                        "price": 50000,
                        "features": "高反発設計、安定性重視"
                    }
                ]
            },
            "woods": [
                {
                    "club": "フェアウェイウッド",
                    "brand": "タイトリスト",
                    "model": "TSR2",
                    "loft": recommended_loft + 5,
                    "shaft": "Ventus Blue",
                    "shaft_flex": recommended_flex,
                    "price": 35000,
                    "features": "高弾道、安定性重視"
                }
            ],
            "utilities": [
                {
                    "club": "ユーティリティ",
                    "brand": "タイトリスト",
                    "model": "T200",
                    "loft": recommended_loft + 10,
                    "shaft": "Dynamic Gold",
                    "shaft_flex": recommended_flex,
                    "price": 25000,
                    "features": "打ちやすさ重視"
                }
            ],
            "irons": [
                {
                    "club": f"アイアン{i+4}",
                    "brand": "タイトリスト",
                    "model": "T200",
                    "loft": recommended_loft + (i * 4),
                    "shaft": "Dynamic Gold",
                    "shaft_flex": recommended_flex,
                    "price": 15000,
                    "features": "フォージド設計、高弾道"
                } for i in range(7)
            ],
            "wedges": [
                {
                    "club": "サンドウェッジ",
                    "brand": "タイトリスト",
                    "model": "Vokey SM9",
                    "loft": 56,
                    "shaft": "Dynamic Gold",
                    "shaft_flex": recommended_flex,
                    "price": 20000,
                    "features": "スピン性能重視"
                },
                {
                    "club": "ロブウェッジ",
                    "brand": "タイトリスト",
                    "model": "Vokey SM9",
                    "loft": 60,
                    "shaft": "Dynamic Gold",
                    "shaft_flex": recommended_flex,
                    "price": 20000,
                    "features": "高弾道、スピン性能重視"
                }
            ],
            "putter": {
                "club": "パター",
                "brand": "タイトリスト",
                "model": "Scotty Cameron",
                "length": 34,
                "price": 40000,
                "features": "安定性重視"
            },
            "total_price": 55000 + 35000 + 25000 + (15000 * 7) + (20000 * 2) + 40000  # 全クラブの合計
        }
        
        return response
        
    except Exception as e:
        print(f"Error details: {str(e)}")  # デバッグ用
        raise HTTPException(status_code=500, detail=f"レコメンデーション生成中にエラーが発生しました: {str(e)}")

def search_clubs_database(recommended_loft, recommended_flex):
    # TODO: 実際のデータベース検索を実装
    return {
        "driver": {"loft": recommended_loft, "shaft_flex": recommended_flex},
        "woods": [{"loft": recommended_loft + 5, "shaft_flex": recommended_flex}],
        "utilities": [],
        "irons": [{"loft": 30, "shaft_flex": recommended_flex}],
        "wedges": [{"loft": 56}],
        "putter": {"length": 34}
    }

def optimize_club_set(clubs):
    # TODO: 実際の最適化ロジックを実装
    return {
        "driver": clubs["driver"],
        "woods": clubs["woods"],
        "utilities": clubs["utilities"],
        "irons": clubs["irons"],
        "wedges": clubs["wedges"],
        "putter": clubs["putter"],
        "total_price": 150000  # 仮の価格
    }

def get_club_recommendations(user_data: Dict[str, Any]) -> Dict[str, Any]:
    try:
        # ユーザーデータの前処理
        features = {
            'height': user_data['height'],
            'weight': user_data['weight'],
            'age': user_data['age'],
            'gender': 1 if user_data['gender'] == 'male' else 0,
            'head_speed': user_data.get('head_speed', 45.0),
            'ball_speed': user_data.get('ball_speed', 60.0),
            'launch_angle': user_data.get('launch_angle', 12.0)
        }
        
        # 予測用のDataFrame作成
        X = pd.DataFrame([features])
        
        # ドライバーの推奨
        driver_loft = driver_model.predict(X)[0]
        shaft_flex = shaft_model.predict(X)[0]
        
        # アイアンセットの推奨
        iron_lofts = iron_model.predict(X)
        
        # クラブセットの構成を決定
        club_set = {
            "driver": {
                "club": "ドライバー",
                "loft": float(driver_loft),
                "shaft_flex": str(shaft_flex),
                "recommended_models": [
                    {
                        "brand": "タイトリスト",
                        "model": "TSR3",
                        "loft": float(driver_loft),
                        "shaft": "Ventus Blue",
                        "shaft_flex": str(shaft_flex),
                        "price": 55000,
                        "features": "低スピン設計、高弾道"
                    },
                    {
                        "brand": "キャロウェイ",
                        "model": "Paradym",
                        "loft": float(driver_loft),
                        "shaft": "HZRDUS Black",
                        "shaft_flex": str(shaft_flex),
                        "price": 50000,
                        "features": "高反発設計、安定性重視"
                    }
                ]
            },
            "irons": [
                {
                    "club": f"アイアン{i+4}",
                    "brand": "タイトリスト",
                    "model": "T200",
                    "loft": float(loft),
                    "shaft": "Dynamic Gold",
                    "shaft_flex": str(shaft_flex),
                    "price": 15000,
                    "features": "フォージド設計、高弾道"
                } for i, loft in enumerate(iron_lofts)
            ],
            "total_price": 55000 + (15000 * 7)  # ドライバー + 7本のアイアン
        }
        
        # スイングの悩みに基づいて鉛テープの位置を提案
        swing_issue = user_data.get('swing_issue')
        if swing_issue:
            weight_position = {
                "スライス": "トゥ側",
                "フック": "ヒール側",
                "低い弾道": "クラウン側",
                "高い弾道": "ソール側"
            }
            club_set["weight_position"] = weight_position.get(swing_issue, "未指定")
        
        return club_set
        
    except Exception as e:
        print(f"エラー詳細: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 