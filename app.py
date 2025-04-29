import os
from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Annotated
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib
from dotenv import load_dotenv
from database import SessionLocal, Club, Base, engine, get_db, User
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from schemas import (
    UserCreate,
    UserUpdate,
    UserPreferences,
    ClubRecommendation,
    ClubSearch,
    ClubSearchResponse,
    Token,
    ErrorResponse
)
from functools import wraps
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

# ルーターのインポート
from app.routes import auth

# テスト環境の判定
if os.getenv("TESTING") == "1":
    from tests.config import (
        DATABASE_URL,
        SQL_ECHO,
        REDIS_URL,
        JWT_SECRET_KEY as SECRET_KEY,
        JWT_ALGORITHM as ALGORITHM,
        ACCESS_TOKEN_EXPIRE_MINUTES
    )
    from tests.security import (
        verify_password,
        get_password_hash,
        create_access_token,
        get_current_user
    )
else:
    from config import (
        DATABASE_URL,
        SQL_ECHO,
        REDIS_URL,
        SECRET_KEY,
        ALGORITHM,
        ACCESS_TOKEN_EXPIRE_MINUTES
    )
    from security import (
        verify_password,
        get_password_hash,
        create_access_token,
        get_current_user
    )

app = FastAPI(
    title="ピッタリゴルフ",
    description="""
    ゴルフクラブのパーソナライズドフィッティングを提供するAPI。
    
    ## 主な機能
    * 👤 ユーザープロファイルに基づくクラブ推奨
    * 🏌️ スイングデータの分析
    * 💰 予算に応じたクラブセットの最適化
    * 📊 フィッティング結果の詳細な分析
    
    ## 認証
    * Bearer token認証を使用
    * `/token`エンドポイントでアクセストークンを取得
    
    ## エラーコード
    * 400: 入力値が不正
    * 401: 認証エラー
    * 403: 権限エラー
    * 404: リソースが見つからない
    * 500: サーバーエラー
    """,
    version="1.0.0",
    contact={
        "name": "ピッタリゴルフ サポートチーム",
        "email": "support@pittari-golf.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    }
)

# ルーターの登録
app.include_router(auth.router, prefix="/api", tags=["認証"])

# エラーハンドラーの定義
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()}
    )

@app.exception_handler(SQLAlchemyError)
async def database_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Database error occurred"}
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Unexpected error occurred"}
    )

# 認証エラーハンドラーデコレータ
def handle_authentication_errors(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except HTTPException as e:
            if e.status_code == status.HTTP_401_UNAUTHORIZED:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect username or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            raise e
    return wrapper

# データベースエラーハンドラーデコレータ
def handle_database_errors(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error occurred"
            )
    return wrapper

# データモデル定義
class UserProfile(BaseModel):
    height: float = Field(..., gt=0, le=250, description="身長（cm）")
    weight: float = Field(..., gt=0, le=200, description="体重（kg）")
    age: int = Field(..., gt=0, le=120, description="年齢")
    gender: str = Field(..., description="性別")
    handicap: Optional[float] = Field(None, ge=0, le=54, description="ハンディキャップ")
    head_speed: Optional[float] = Field(None, ge=0, le=200, description="ヘッドスピード（m/s）")
    ball_speed: Optional[float] = Field(None, ge=0, le=300, description="ボールスピード（m/s）")
    launch_angle: Optional[float] = Field(None, ge=0, le=90, description="打ち出し角（度）")
    swing_issue: Optional[str] = Field(None, description="スイングの課題")
    budget: Optional[float] = Field(None, ge=0, description="予算（円）")

    @validator('gender')
    def validate_gender(cls, v):
        if v.lower() not in ['male', 'female']:
            raise ValueError('性別は "male" または "female" を指定してください')
        return v.lower()

    @validator('handicap')
    def validate_handicap(cls, v):
        if v is not None and (v < 0 or v > 54):
            raise ValueError('ハンディキャップは0から54の間で指定してください')
        return v

    @validator('head_speed')
    def validate_head_speed(cls, v):
        if v is not None and (v < 0 or v > 200):
            raise ValueError('ヘッドスピードは0から200の間で指定してください')
        return v

    @validator('ball_speed')
    def validate_ball_speed(cls, v):
        if v is not None and (v < 0 or v > 300):
            raise ValueError('ボールスピードは0から300の間で指定してください')
        return v

    @validator('launch_angle')
    def validate_launch_angle(cls, v):
        if v is not None and (v < 0 or v > 90):
            raise ValueError('打ち出し角は0から90の間で指定してください')
        return v

    @validator('budget')
    def validate_budget(cls, v):
        if v is not None and v < 0:
            raise ValueError('予算は0以上の値を指定してください')
        return v

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

@app.get("/",
    response_model=Dict[str, str],
    summary="APIの基本情報を取得",
    description="APIの現在のバージョンとステータスを返します。",
    response_description="APIの基本情報",
    tags=["システム情報"]
)
async def root():
    """
    APIの基本情報を返します。
    
    Returns:
        Dict[str, str]: APIの基本情報（メッセージ、バージョン、ステータス）
    """
    return {
        "message": "ピッタリゴルフへようこそ",
        "version": "1.0.0",
        "status": "active"
    }

@app.post("/token", response_model=Token)
@handle_authentication_errors
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: SessionLocal = Depends(get_db)
) -> Token:
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@app.get("/users/me", response_model=Dict[str, Any])
@handle_authentication_errors
async def get_current_user(
    current_user: Annotated[User, Depends(get_current_user)]
) -> Dict[str, Any]:
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "height": current_user.height,
        "weight": current_user.weight,
        "age": current_user.age,
        "gender": current_user.gender,
        "handicap": current_user.handicap
    }

@app.post("/recommend", response_model=ClubRecommendation)
async def recommend_clubs(
    profile: UserProfile,
    db: Session = Depends(get_db)
) -> ClubRecommendation:
    # ユーザープロファイルに基づいてクラブを選択
    def select_clubs_by_profile(clubs, profile):
        # スイングスピードに基づくシャフトフレックスの選択
        if profile.head_speed:
            if profile.head_speed >= 45:
                preferred_flex = "X"
            elif profile.head_speed >= 40:
                preferred_flex = "S"
            else:
                preferred_flex = "R"
        else:
            preferred_flex = "S"  # デフォルト値

        # 予算に基づく価格帯の選択
        if profile.budget:
            if profile.budget >= 300000:
                price_categories = ["プレミアム", "ミドル"]
            elif profile.budget >= 200000:
                price_categories = ["ミドル"]
            else:
                price_categories = ["エントリー"]
        else:
            price_categories = ["プレミアム", "ミドル", "エントリー"]

        # ハンディキャップに基づく容錯性の選択
        if profile.handicap:
            if profile.handicap <= 10:
                forgiveness = "低"
            elif profile.handicap <= 20:
                forgiveness = "中"
            else:
                forgiveness = "高"
        else:
            forgiveness = "中"  # デフォルト値

        # クラブのフィルタリングとソート
        filtered_clubs = [
            club for club in clubs
            if (club.shaft_flex == preferred_flex or club.type == "putter")
            and club.price_category in price_categories
            and (club.forgiveness == forgiveness or club.type == "putter")
        ]

        # 評価とレビュー数に基づくスコアリング
        for club in filtered_clubs:
            club.score = (club.average_rating * 0.7 + (club.review_count / 100) * 0.3)

        # スコアでソート
        return sorted(filtered_clubs, key=lambda x: x.score, reverse=True)

    # 各タイプのクラブを取得
    drivers = select_clubs_by_profile(
        db.query(Club).filter(Club.type == "driver").all(),
        profile
    )
    woods = select_clubs_by_profile(
        db.query(Club).filter(Club.type == "wood").all(),
        profile
    )
    utilities = select_clubs_by_profile(
        db.query(Club).filter(Club.type == "utility").all(),
        profile
    )
    irons = select_clubs_by_profile(
        db.query(Club).filter(Club.type == "iron").all(),
        profile
    )
    wedges = select_clubs_by_profile(
        db.query(Club).filter(Club.type == "wedge").all(),
        profile
    )
    putters = select_clubs_by_profile(
        db.query(Club).filter(Club.type == "putter").all(),
        profile
    )

    # クラブ情報を整形
    def format_club(club):
        return {
            "brand": club.brand,
            "model": club.model,
            "loft": club.loft,
            "shaft": club.shaft,
            "shaft_flex": club.shaft_flex,
            "price": club.price,
            "features": club.features,
            "trajectory": club.trajectory,
            "spin": club.spin,
            "forgiveness": club.forgiveness,
            "shaft_details": club.shaft_details,
            "price_category": club.price_category,
            "average_rating": club.average_rating,
            "review_count": club.review_count,
            "reviews": club.reviews
        }

    # 推奨クラブセットを返す
    return ClubRecommendation(
        driver=format_club(drivers[0]) if drivers else None,
        woods=[format_club(wood) for wood in woods[:2]],
        utilities=[format_club(utility) for utility in utilities[:1]],
        irons=[format_club(iron) for iron in irons[:7]],
        wedges=[format_club(wedge) for wedge in wedges[:2]],
        putter=format_club(putters[0]) if putters else None,
        total_price=sum([
            drivers[0].price if drivers else 0,
            sum(wood.price for wood in woods[:2]),
            sum(utility.price for utility in utilities[:1]),
            sum(iron.price for iron in irons[:7]),
            sum(wedge.price for wedge in wedges[:2]),
            putters[0].price if putters else 0
        ]),
        confidence_score=0.85,
        timestamp=datetime.now()
    )

def preprocess_profile(profile: UserProfile) -> Dict[str, Any]:
    """プロファイルデータの前処理"""
    # 数値データの変換
    data = {
        "height": profile.height,
        "weight": profile.weight,
        "age": profile.age,
        "gender_encoded": 1 if profile.gender == "male" else 0,
        "handicap": profile.handicap or 20,
        "head_speed": profile.head_speed or 40,
        "ball_speed": profile.ball_speed or 60,
        "launch_angle": profile.launch_angle or 12
    }
    
    return data

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

# 認証関連の関数
def authenticate_user(username: str, password: str, db: SessionLocal = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# セキュリティ設定
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") 