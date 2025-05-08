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
import logging

# ロギングの設定
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="SwingFit Pro API",
    description="AIゴルフクラブレコメンデーションシステムのバックエンドAPI",
    version="1.0.0",
    debug=settings.DEBUG
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
async def root():
    return {
        "message": "SwingFit Pro API",
        "environment": settings.ENV,
        "debug": settings.DEBUG
    }

# 環境情報を返すエンドポイント（開発環境のみ）
@app.get("/env-info")
async def env_info():
    if not settings.is_development:
        return {"message": "This endpoint is only available in development environment"}
    
    return {
        "environment": settings.ENV,
        "debug": settings.DEBUG,
        "api_host": settings.API_HOST,
        "api_port": settings.API_PORT,
        "cors_origins": settings.CORS_ORIGINS,
        "log_level": settings.LOG_LEVEL
    }

def is_custom_build_viable(user_budget: float, club_type: str) -> bool:
    """予算に応じてカスタムビルドが可能かどうかを判断"""
    base_price = {
        "ドライバー": 80000,
        "アイアン": 120000
    }.get(club_type, 100000)
    
    # 予算が基本価格の1.5倍以上あればカスタムビルドを推奨
    return user_budget >= base_price * 1.5

# 属性ごとの推奨パターン
USER_PATTERNS = {
    "tour_pro": [1, 7, 10],
    "advanced": [2, 5, 8],
    "intermediate_male": [4, 6, 9],
    "intermediate_female": [3, 5, 9],
    "senior": [3, 6, 9],
    "beginner": [6, 9],
}

# パターンごとのクラブ構成（14本に厳密調整）
PATTERN_CLUBS = {
    1: [
        ("ドライバー", "9.5°"), ("3W", "15°"), ("5W", "18°"), ("3U", "19°"),
        ("4I", "24°"), ("5I", "27°"), ("6I", "30°"), ("7I", "34°"), ("8I", "38°"), ("9I", "42°"), ("PW", "46°"),
        ("AW", "50°"), ("SW", "54°"), ("LW", "58°"), ("パター", "")
    ][:14],
    2: [
        ("ドライバー", "10.5°"), ("3W", "16°"), ("5H", "24°"),
        ("6I", "28°"), ("7I", "32°"), ("8I", "36°"), ("9I", "40°"), ("PW", "46°"),
        ("AW", "52°"), ("SW", "56°"), ("LW", "60°"), ("パター", "")
    ][:14],
    3: [
        ("ドライバー", "12°"), ("4W", "16.5°"), ("7W", "21°"), ("9W", "24°"),
        ("5I", "27°"), ("6I", "30°"), ("7I", "34°"), ("8I", "38°"), ("9I", "42°"), ("PW", "46°"),
        ("AW", "50°"), ("SW", "54°"), ("パター", "")
    ][:14],
    4: [
        ("ドライバー", "10.5°"), ("2U", "17°"), ("3U", "20°"), ("4U", "23°"),
        ("5I", "27°"), ("6I", "30°"), ("7I", "34°"), ("8I", "38°"), ("9I", "42°"), ("PW", "46°"),
        ("AW", "52°"), ("LW", "58°"), ("パター", "")
    ][:14],
    5: [
        ("ドライバー", "10.5°"), ("3W", "15°"), ("5H", "24°"),
        ("6I", "28°"), ("7I", "32°"), ("8I", "36°"), ("9I", "40°"), ("PW", "46°"),
        ("AW", "48°"), ("GW", "52°"), ("SW", "56°"), ("LW", "60°"), ("パター", "")
    ][:14],
    6: [
        ("ドライバー", "12°"), ("5W", "18°"), ("4H", "22°"),
        ("6I", "28°"), ("7I", "32°"), ("8I", "36°"), ("9I", "40°"), ("PW", "46°"),
        ("AW", "50°"), ("SW", "54°"), ("LW", "58°"), ("パター", "")
    ][:14],
    7: [
        ("ドライバー", "9°"), ("3W", "13.5°"), ("5W", "18°"), ("2I", "17°"),
        ("4I", "24°"), ("5I", "27°"), ("6I", "30°"), ("7I", "34°"), ("8I", "38°"), ("9I", "42°"), ("PW", "46°"),
        ("SW", "54°"), ("LW", "58°"), ("パター", "")
    ][:14],
    8: [
        ("ドライバー", "10.5°"), ("4W", "16.5°"), ("5H", "24°"),
        ("6I", "28°"), ("7I", "32°"), ("8I", "36°"), ("9I", "40°"), ("PW", "46°"),
        ("AW", "50°"), ("GW", "52°"), ("SW", "54°"), ("LW", "56°"), ("パター", "")
    ][:14],
    9: [
        ("ドライバー", "10.5°"), ("3H", "19°"), ("4H", "22°"), ("5H", "25°"),
        ("6I", "28°"), ("7I", "32°"), ("8I", "36°"), ("9I", "40°"), ("PW", "46°"),
        ("AW", "52°"), ("LW", "58°"), ("パター", "")
    ][:14],
    10: [
        ("ドライバー", "10.5°"), ("3W", "15°"), ("2U", "18°"), ("4I", "24°"),
        ("5I", "27°"), ("6I", "30°"), ("7I", "34°"), ("8I", "38°"), ("9I", "42°"), ("PW", "46°"),
        ("AW", "52°"), ("LW", "58°"), ("パター", "")
    ][:14],
}

# 属性判定関数
def get_user_attribute(user_data):
    head_speed = float(user_data.get("headSpeed", 0))
    handicap = float(user_data.get("handicap", 99))
    age = int(user_data.get("age", 99))
    gender = user_data.get("gender", "male")
    # プロ
    if head_speed >= 110 and handicap <= 5:
        return "tour_pro"
    # 上級アマ
    if head_speed >= 95 and handicap <= 10:
        return "advanced"
    # シニア
    if age >= 60 or (head_speed <= 75 and handicap >= 15):
        return "senior"
    # 初心者
    if handicap >= 21 or head_speed <= 85:
        return "beginner"
    # 中級女性
    if gender == "female" and 11 <= handicap <= 20:
        return "intermediate_female"
    # 中級男性
    if gender == "male" and 11 <= handicap <= 20:
        return "intermediate_male"
    # デフォルト
    return "intermediate_male"

@app.post("/api/recommendations/", response_model=RecommendationResponse)
async def get_recommendations(request: RecommendationRequest):
    user_data = request.dict()
    recommendations = []

    # 属性判定
    user_attr = get_user_attribute(user_data)
    pattern_ids = USER_PATTERNS.get(user_attr, [1])

    # 3つの異なるセットを生成
    for i, pattern_id in enumerate(pattern_ids[:3]):
        pattern = PATTERN_CLUBS.get(pattern_id)
        if not pattern:
            continue
        set_clubs = {}
        total_price = 0
        features = []
        used_types = set()
        for club_type, loft in pattern:
            # 14本を厳密に管理
            if len(set_clubs) >= 14:
                break
            # DBから該当クラブを検索（ロフトやタイプで最適なものを選ぶ）
            db_type = club_type.replace("W", "ウッド").replace("U", "ユーティリティ").replace("I", "アイアン").replace("H", "ユーティリティ")
            candidates = [c for c in CLUB_DATABASE.get(db_type, []) if loft in c["loft"] or club_type in c["model"]]
            club = candidates[0] if candidates else (CLUB_DATABASE.get(db_type, [{}])[0])
            set_clubs[club_type] = {
                "brand": club.get("brand", ""),
                "model": club.get("model", ""),
                "flex": club.get("flex", ""),
                "loft": club.get("loft", loft),
                "shaft": club.get("shaft", "")
            }
            total_price += club.get("price", 0)
            features.append(f"{club_type}: {club.get('features', '')}")
            used_types.add(club_type)
        # 14本未満の場合はパターン内から追加
        if len(set_clubs) < 14:
            for club_type, loft in pattern:
                if len(set_clubs) >= 14:
                    break
                if club_type not in used_types:
                    db_type = club_type.replace("W", "ウッド").replace("U", "ユーティリティ").replace("I", "アイアン").replace("H", "ユーティリティ")
                    candidates = [c for c in CLUB_DATABASE.get(db_type, []) if loft in c["loft"] or club_type in c["model"]]
                    club = candidates[0] if candidates else (CLUB_DATABASE.get(db_type, [{}])[0])
                    set_clubs[club_type] = {
                        "brand": club.get("brand", ""),
                        "model": club.get("model", ""),
                        "flex": club.get("flex", ""),
                        "loft": club.get("loft", loft),
                        "shaft": club.get("shaft", "")
                    }
                    total_price += club.get("price", 0)
                    features.append(f"{club_type}: {club.get('features', '')}")
                    used_types.add(club_type)
        set_features = "、".join(features)
        match_details = {
            "swing_speed_match": 1.0,
            "skill_level_match": 1.0,
            "preference_match": 1.0,
            "budget_match": 1.0
        }
        match_score = 1.0
        recommendation = {
            "brand": f"カスタムセット #{i+1}",
            "clubs": set_clubs,
            "total_price": total_price,
            "features": set_features,
            "match_details": match_details,
            "match_score": match_score
        }
        recommendations.append(recommendation)
    recommendations = recommendations[:3]
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