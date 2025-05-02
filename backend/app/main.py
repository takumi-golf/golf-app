from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from typing import List, Optional, Dict
from pydantic import BaseModel
import random
from datetime import datetime
from . import schemas
from .config import settings
from .error_handlers import (
    handle_http_exception,
    handle_validation_error,
    ErrorMessages
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORSミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# エラーハンドラーの登録
app.add_exception_handler(RequestValidationError, handle_validation_error)
app.add_exception_handler(HTTPException, handle_http_exception)

# クラブデータベース
CLUB_DATABASE = {
    "ドライバー": [
        {
            "brand": "タイトリスト",
            "model": "TSR3",
            "flex": "S",
            "loft": "9.0°",
            "shaft": "Mitsubishi Tensei AV Blue",
            "swing_speed_range": (35, 45),
            "skill_level": "中級者",
            "price": 80000,
            "features": "低スピン設計で安定した弾道を実現"
        },
        {
            "brand": "テーラーメイド",
            "model": "Stealth 2",
            "flex": "X",
            "loft": "10.5°",
            "shaft": "Fujikura Ventus Red",
            "swing_speed_range": (40, 50),
            "skill_level": "上級者",
            "price": 90000,
            "features": "高反発設計で飛距離アップ"
        },
        {
            "brand": "キャロウェイ",
            "model": "Paradym",
            "flex": "R",
            "loft": "12°",
            "shaft": "Project X HZRDUS Smoke Red",
            "swing_speed_range": (30, 40),
            "skill_level": "初級者",
            "price": 70000,
            "features": "フォルジブネス設計で打ちやすさを追求"
        },
        {
            "brand": "ミズノ",
            "model": "ST-Z 230",
            "flex": "S",
            "loft": "9°",
            "shaft": "Fujikura Ventus Black",
            "swing_speed_range": (35, 45),
            "skill_level": "中級者",
            "price": 75000,
            "features": "安定した弾道と操作性を両立"
        },
        {
            "brand": "コブラ",
            "model": "Aerojet",
            "flex": "R",
            "loft": "10.5°",
            "shaft": "Mitsubishi Kai'li White",
            "swing_speed_range": (30, 40),
            "skill_level": "初級者",
            "price": 65000,
            "features": "高反発設計で打ちやすさを実現"
        }
    ],
    "ウッド": [
        {
            "brand": "キャロウェイ",
            "model": "Paradym",
            "flex": "R",
            "loft": "15°",
            "shaft": "Project X HZRDUS Smoke Red",
            "swing_speed_range": (30, 40),
            "skill_level": "初級者",
            "price": 50000,
            "features": "フォルジブネス設計で打ちやすさを追求"
        },
        {
            "brand": "ミズノ",
            "model": "ST-Z 230",
            "flex": "S",
            "loft": "16.5°",
            "shaft": "Fujikura Ventus Black",
            "swing_speed_range": (35, 45),
            "skill_level": "中級者",
            "price": 55000,
            "features": "安定した弾道と操作性を両立"
        }
    ],
    "アイアン": [
        {
            "brand": "タイトリスト",
            "model": "T200",
            "flex": "S",
            "loft": "5番",
            "shaft": "True Temper AMT Red",
            "swing_speed_range": (35, 45),
            "skill_level": "中級者",
            "price": 120000,
            "features": "フォージド設計で打感と操作性を両立"
        },
        {
            "brand": "キャロウェイ",
            "model": "Apex Pro",
            "flex": "R",
            "loft": "7番",
            "shaft": "True Temper Elevate MPH",
            "swing_speed_range": (30, 40),
            "skill_level": "初級者",
            "price": 100000,
            "features": "キャビティバック設計で打ちやすさを追求"
        },
        {
            "brand": "ミズノ",
            "model": "JPX923 Forged",
            "flex": "S",
            "loft": "6番",
            "shaft": "Nippon NS Pro Modus3 Tour 120",
            "swing_speed_range": (35, 45),
            "skill_level": "中級者",
            "price": 110000,
            "features": "フォージド設計で優れた打感を実現"
        },
        {
            "brand": "テーラーメイド",
            "model": "P790",
            "flex": "X",
            "loft": "4番",
            "shaft": "KBS Tour 120",
            "swing_speed_range": (40, 50),
            "skill_level": "上級者",
            "price": 130000,
            "features": "スピードフォアード設計で飛距離を追求"
        },
        {
            "brand": "ピン",
            "model": "i525",
            "flex": "R",
            "loft": "8番",
            "shaft": "True Temper Dynamic Gold 105",
            "swing_speed_range": (30, 40),
            "skill_level": "初級者",
            "price": 95000,
            "features": "キャビティバック設計で打ちやすさを実現"
        }
    ],
    "ウェッジ": [
        {
            "brand": "クリーブランド",
            "model": "RTX 6",
            "flex": "S",
            "loft": "56°",
            "shaft": "True Temper Dynamic Gold",
            "swing_speed_range": (30, 45),
            "skill_level": "中級者",
            "price": 25000,
            "features": "優れたスピン性能とコントロール性"
        },
        {
            "brand": "ボブ・ボッシュ",
            "model": "Vokey SM9",
            "flex": "S",
            "loft": "60°",
            "shaft": "True Temper Dynamic Gold",
            "swing_speed_range": (30, 45),
            "skill_level": "中級者",
            "price": 28000,
            "features": "プロ仕様の高精度なショットコントロール"
        }
    ],
    "パター": [
        {
            "brand": "タイトリスト",
            "model": "Scotty Cameron",
            "flex": "無し",
            "loft": "3°",
            "shaft": "Steel",
            "swing_speed_range": (0, 0),
            "skill_level": "中級者",
            "price": 45000,
            "features": "優れた安定性と打感"
        },
        {
            "brand": "テーラーメイド",
            "model": "Spider X",
            "flex": "無し",
            "loft": "3°",
            "shaft": "Steel",
            "swing_speed_range": (0, 0),
            "skill_level": "初級者",
            "price": 40000,
            "features": "高安定性と視認性の高いデザイン"
        }
    ]
}

# シャフトデータベース
SHAFT_DATABASE = {
    "ドライバー": [
        {
            "brand": "Mitsubishi",
            "model": "Tensei AV Blue",
            "flex": "S",
            "weight": "65g",
            "torque": "3.5",
            "price": 35000,
            "features": "中弾道で安定した飛距離を実現",
            "swing_speed_range": (35, 45),
            "skill_level": "中級者"
        },
        {
            "brand": "Fujikura",
            "model": "Ventus Red",
            "flex": "X",
            "weight": "60g",
            "torque": "3.2",
            "price": 40000,
            "features": "低スピンで最大飛距離を追求",
            "swing_speed_range": (40, 50),
            "skill_level": "上級者"
        },
        {
            "brand": "Project X",
            "model": "HZRDUS Smoke Red",
            "flex": "R",
            "weight": "55g",
            "torque": "3.8",
            "price": 30000,
            "features": "高弾道で打ちやすさを実現",
            "swing_speed_range": (30, 40),
            "skill_level": "初級者"
        }
    ],
    "アイアン": [
        {
            "brand": "True Temper",
            "model": "AMT Red",
            "flex": "S",
            "weight": "95g",
            "price": 25000,
            "features": "軽量で操作性を追求",
            "swing_speed_range": (35, 45),
            "skill_level": "中級者"
        },
        {
            "brand": "KBS",
            "model": "Tour 120",
            "flex": "X",
            "weight": "120g",
            "price": 30000,
            "features": "安定した打感と操作性",
            "swing_speed_range": (40, 50),
            "skill_level": "上級者"
        },
        {
            "brand": "Nippon",
            "model": "NS Pro Modus3 Tour 120",
            "flex": "R",
            "weight": "110g",
            "price": 28000,
            "features": "しなやかな打感で打ちやすさを実現",
            "swing_speed_range": (30, 40),
            "skill_level": "初級者"
        }
    ]
}

def calculate_skill_level(handicap: float) -> str:
    if handicap <= 10:
        return "上級者"
    elif handicap <= 20:
        return "中級者"
    else:
        return "初級者"

def calculate_swing_speed_match(club_speed_range: tuple, user_speed: float) -> float:
    min_speed, max_speed = club_speed_range
    # パターの場合は常に1.0を返す
    if min_speed == 0 and max_speed == 0:
        return 1.0
    if min_speed <= user_speed <= max_speed:
        return 1.0
    elif user_speed < min_speed:
        return 1.0 - (min_speed - user_speed) / min_speed
    else:
        return 1.0 - (user_speed - max_speed) / max_speed

def calculate_skill_level_match(club_skill: str, user_skill: str) -> float:
    skill_levels = {"初級者": 0, "中級者": 1, "上級者": 2}
    diff = abs(skill_levels[club_skill] - skill_levels[user_skill])
    return 1.0 - (diff * 0.3)

def calculate_preference_match(club_brand: str, preferred_brands: List[str]) -> float:
    if not preferred_brands:
        return 0.7  # 好みが指定されていない場合は中程度のスコア
    return 1.0 if club_brand in preferred_brands else 0.5

def calculate_budget_match(club_price: float, user_budget: float) -> float:
    if club_price <= user_budget:
        return 1.0
    return max(0.3, 1.0 - (club_price - user_budget) / user_budget)

def calculate_shaft_match_score(shaft: dict, user_data: dict) -> float:
    """シャフトのマッチングスコアを計算"""
    # スイングスピードのマッチング
    swing_speed_match = calculate_swing_speed_match(
        shaft["swing_speed_range"],
        float(user_data["headSpeed"])
    )

    # スキルレベルのマッチング
    user_skill = calculate_skill_level(float(user_data["handicap"]))
    skill_level_match = calculate_skill_level_match(shaft["skill_level"], user_skill)

    # 予算のマッチング
    budget_match = calculate_budget_match(shaft["price"], float(user_data["budget"]))

    # 総合スコアの計算（重み付け）
    weights = {
        "swing_speed": 0.5,
        "skill_level": 0.3,
        "budget": 0.2
    }

    match_score = (
        swing_speed_match * weights["swing_speed"] +
        skill_level_match * weights["skill_level"] +
        budget_match * weights["budget"]
    )

    return match_score

def find_best_shaft(club_type: str, user_data: dict) -> dict:
    """最適なシャフトを選択"""
    shafts = SHAFT_DATABASE.get(club_type, [])
    if not shafts:
        return None
        
    # マッチングスコアを計算
    shaft_scores = []
    for shaft in shafts:
        match_score = calculate_shaft_match_score(shaft, user_data)
        shaft_scores.append((shaft, match_score))
    
    # 最適なシャフトを選択
    best_shaft, _ = max(shaft_scores, key=lambda x: x[1])
    return best_shaft

def calculate_match_score(club: dict, user_data: dict) -> float:
    # スイングスピードのマッチング
    swing_speed_match = calculate_swing_speed_match(
        club["swing_speed_range"],
        float(user_data["headSpeed"])
    )

    # スキルレベルのマッチング
    user_skill = calculate_skill_level(float(user_data["handicap"]))
    skill_level_match = calculate_skill_level_match(club["skill_level"], user_skill)

    # 好みのマッチング
    preferred_brands = user_data.get("preferred_brands", [])
    preference_match = calculate_preference_match(club["brand"], preferred_brands)

    # 予算のマッチング
    budget_match = calculate_budget_match(club["price"], float(user_data["budget"]))

    # パターの場合は重み付けを調整
    if club["swing_speed_range"] == (0, 0):  # パターの場合
        weights = {
            "swing_speed": 0.0,  # スイングスピードは考慮しない
            "skill_level": 0.4,  # スキルレベルを重視
            "preference": 0.3,   # 好みを重視
            "budget": 0.3        # 予算を重視
        }
    else:
        weights = {
            "swing_speed": 0.3,
            "skill_level": 0.3,
            "preference": 0.2,
            "budget": 0.2
        }

    match_score = (
        swing_speed_match * weights["swing_speed"] +
        skill_level_match * weights["skill_level"] +
        preference_match * weights["preference"] +
        budget_match * weights["budget"]
    )

    return match_score

class RecommendationRequest(BaseModel):
    height: float
    weight: float
    age: int
    gender: str
    handicap: float
    headSpeed: float
    ballSpeed: float
    launchAngle: float
    swingIssue: str
    budget: float

    model_config = {
        "json_schema_extra": {
            "example": {
                "height": 170,
                "weight": 65,
                "age": 40,
                "gender": "male",
                "handicap": 20,
                "headSpeed": 40,
                "ballSpeed": 50,
                "launchAngle": 15,
                "swingIssue": "none",
                "budget": 100000
            }
        }
    }

class ClubSetRecommendation(BaseModel):
    brand: str
    clubs: Dict[str, dict]
    match_score: float
    total_price: float
    features: str
    match_details: Dict[str, float]

class RecommendationResponse(BaseModel):
    id: int
    timestamp: str
    recommendations: List[ClubSetRecommendation]

class RecommendationList(BaseModel):
    recommendations: List[RecommendationResponse]

@app.get("/")
def read_root():
    return {"message": "ゴルフクラブレコメンデーションAPIへようこそ"}

def is_custom_build_viable(user_budget: float, club_type: str) -> bool:
    """予算に応じてカスタムビルドが可能かどうかを判断"""
    base_price = {
        "ドライバー": 80000,
        "アイアン": 120000
    }.get(club_type, 100000)
    
    # 予算が基本価格の1.5倍以上あればカスタムビルドを推奨
    return user_budget >= base_price * 1.5

@app.post("/api/recommendations/", response_model=RecommendationResponse)
async def get_recommendations(request: RecommendationRequest):
    user_data = request.dict()
    recommendations = []
    
    # 各クラブタイプの最適な組み合わせを生成
    for _ in range(3):  # 3つの異なるセットを生成
        set_clubs = {}
        total_price = 0
        features = []
        
        # ドライバーを選択
        driver_scores = [(club, calculate_match_score(club, user_data)) for club in CLUB_DATABASE["ドライバー"]]
        best_driver, driver_score = max(driver_scores, key=lambda x: x[1])
        set_clubs["ドライバー"] = {
            "brand": best_driver["brand"],
            "model": best_driver["model"],
            "flex": best_driver["flex"],
            "loft": best_driver["loft"],
            "shaft": best_driver["shaft"]
        }
        total_price += best_driver["price"]
        features.append(f"ドライバー: {best_driver['features']}")
        
        # ウッドを選択
        wood_scores = [(club, calculate_match_score(club, user_data)) for club in CLUB_DATABASE["ウッド"]]
        best_wood, wood_score = max(wood_scores, key=lambda x: x[1])
        set_clubs["ウッド"] = {
            "brand": best_wood["brand"],
            "model": best_wood["model"],
            "flex": best_wood["flex"],
            "loft": best_wood["loft"],
            "shaft": best_wood["shaft"]
        }
        total_price += best_wood["price"]
        features.append(f"ウッド: {best_wood['features']}")
        
        # アイアンセットを選択
        iron_scores = [(club, calculate_match_score(club, user_data)) for club in CLUB_DATABASE["アイアン"]]
        best_iron, iron_score = max(iron_scores, key=lambda x: x[1])
        set_clubs["アイアン"] = {
            "brand": best_iron["brand"],
            "model": best_iron["model"],
            "flex": best_iron["flex"],
            "loft": "5番-9番",
            "shaft": best_iron["shaft"]
        }
        total_price += best_iron["price"] * 5  # 5本セット
        features.append(f"アイアン: {best_iron['features']}")
        
        # ウェッジを選択
        wedge_scores = [(club, calculate_match_score(club, user_data)) for club in CLUB_DATABASE["ウェッジ"]]
        best_wedge, wedge_score = max(wedge_scores, key=lambda x: x[1])
        set_clubs["ウェッジ"] = {
            "brand": best_wedge["brand"],
            "model": best_wedge["model"],
            "flex": best_wedge["flex"],
            "loft": "56°, 60°",
            "shaft": best_wedge["shaft"]
        }
        total_price += best_wedge["price"] * 2  # 2本セット
        features.append(f"ウェッジ: {best_wedge['features']}")
        
        # パターを選択
        putter_scores = [(club, calculate_match_score(club, user_data)) for club in CLUB_DATABASE["パター"]]
        best_putter, putter_score = max(putter_scores, key=lambda x: x[1])
        set_clubs["パター"] = {
            "brand": best_putter["brand"],
            "model": best_putter["model"],
            "flex": best_putter["flex"],
            "loft": best_putter["loft"],
            "shaft": best_putter["shaft"]
        }
        total_price += best_putter["price"]
        features.append(f"パター: {best_putter['features']}")
        
        # セットの特徴をまとめる
        set_features = "、".join(features)
        
        # マッチングスコアを計算
        match_details = {
            "swing_speed_match": (driver_score + wood_score + iron_score) / 3,
            "skill_level_match": (driver_score + wood_score + iron_score + wedge_score + putter_score) / 5,
            "preference_match": calculate_preference_match(best_driver["brand"], user_data.get("preferred_brands", [])),
            "budget_match": calculate_budget_match(total_price, float(user_data["budget"]))
        }
        
        # 総合マッチングスコアを計算
        weights = {
            "swing_speed": 0.3,
            "skill_level": 0.3,
            "preference": 0.2,
            "budget": 0.2
        }
        
        match_score = (
            match_details["swing_speed_match"] * weights["swing_speed"] +
            match_details["skill_level_match"] * weights["skill_level"] +
            match_details["preference_match"] * weights["preference"] +
            match_details["budget_match"] * weights["budget"]
        )
        
        recommendation = {
            "brand": f"カスタムセット #{len(recommendations) + 1}",
            "clubs": set_clubs,
            "total_price": total_price,
            "features": set_features,
            "match_details": match_details,
            "match_score": match_score
        }
        
        recommendations.append(recommendation)
    
    # マッチングスコアでソート
    recommendations.sort(key=lambda x: x["match_score"], reverse=True)
    
    # レスポンスを生成
    response = {
        "id": random.randint(1, 1000),
        "timestamp": datetime.now().isoformat(),
        "recommendations": recommendations
    }
    
    return response

@app.get("/api/recommendations/history/", response_model=RecommendationList)
async def get_recommendation_history():
    return {"recommendations": []}

@app.post("/api/recommendations/{recommendation_id}/feedback/")
async def submit_feedback(recommendation_id: int, feedback: str):
    return {"message": "フィードバックを受け付けました", "recommendation_id": recommendation_id} 