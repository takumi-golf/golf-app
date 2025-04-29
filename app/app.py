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
from .database import SessionLocal, Club, Base, engine, GolfCourse, GolfRound, GolfHole, get_db, User
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from .schemas import (
    UserCreate,
    UserUpdate,
    UserPreferences,
    ClubRecommendation,
    ClubSearch,
    ClubSearchResponse,
    Token,
    ErrorResponse,
    GolfCourseCreate,
    GolfRoundCreate,
    GolfHoleCreate
)
from functools import wraps
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

# ルーターのインポート
from .routes import auth, clubs, courses, rounds, holes

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
    title="ゴルフクラブフィッティングAPI",
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
        "name": "ゴルフクラブフィッティングAPI サポートチーム",
        "email": "support@golfclub-fitting.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    }
)

# ルーターの登録
app.include_router(auth.router, prefix="/api", tags=["認証"])
app.include_router(clubs.router, prefix="/api", tags=["クラブ"])
app.include_router(courses.router, prefix="/api", tags=["コース"])
app.include_router(rounds.router, prefix="/api", tags=["ラウンド"])
app.include_router(holes.router, prefix="/api", tags=["ホール"])

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
        "message": "ゴルフフィッティングAPIへようこそ",
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
    current_user: Annotated[User, Depends(get_current_user)]
) -> ClubRecommendation:
    if not models:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "モデル読み込みエラー",
                "message": "必要なAIモデルの一部がロードされていません。システム管理者に連絡してください。"
            }
        )
    
    try:
        profile_data = preprocess_profile(profile)
        recommendations = generate_recommendations(profile_data)
        confidence_score = calculate_overall_confidence(recommendations, profile_data)
        
        return ClubRecommendation(
            **recommendations,
            confidence_score=confidence_score,
            timestamp=datetime.now()
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "入力値エラー",
                "message": str(e)
            }
        )
    except Exception as e:
        print(f"Error details: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "システムエラー",
                "message": "レコメンデーション生成中に予期せぬエラーが発生しました。",
                "debug_info": str(e) if os.getenv("DEBUG_MODE") else None
            }
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

@app.post("/recommendations/", response_model=ClubSearchResponse)
async def get_recommendations(
    preferences: UserPreferences,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[SessionLocal, Depends(get_db)]
) -> ClubSearchResponse:
    clubs = db.query(Club).filter(
        Club.price <= preferences.budget,
        Club.shaft_flex.in_(preferences.preferred_shaft_flex)
    ).all()
    return ClubSearchResponse(clubs=clubs)

@app.get("/clubs/search", response_model=ClubSearchResponse)
async def search_clubs(
    search: ClubSearch,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[SessionLocal, Depends(get_db)]
) -> ClubSearchResponse:
    query = db.query(Club)
    if search.brand:
        query = query.filter(Club.brand == search.brand)
    if search.min_price:
        query = query.filter(Club.price >= search.min_price)
    if search.max_price:
        query = query.filter(Club.price <= search.max_price)
    if search.shaft_flex:
        query = query.filter(Club.shaft_flex == search.shaft_flex)
    clubs = query.all()
    return ClubSearchResponse(clubs=clubs)

@app.post("/clubs/", response_model=Dict[str, Any])
@handle_authentication_errors
@handle_database_errors
async def create_club(
    club: Dict[str, Any],
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[SessionLocal, Depends(get_db)]
) -> Dict[str, Any]:
    try:
        db_club = Club(**club)
        db.add(db_club)
        db.commit()
        db.refresh(db_club)
        return {
            "id": db_club.id,
            "club_id": db_club.club_id,
            "brand": db_club.brand,
            "model": db_club.model,
            "type": db_club.type,
            "loft": db_club.loft,
            "shaft": db_club.shaft,
            "shaft_flex": db_club.shaft_flex,
            "price": db_club.price,
            "features": db_club.features,
            "specifications": db_club.specifications,
            "popularity_score": db_club.popularity_score,
            "is_available": db_club.is_available,
            "created_at": db_club.created_at.isoformat(),
            "updated_at": db_club.updated_at.isoformat()
        }
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@app.post("/courses/", response_model=Dict[str, Any])
@handle_authentication_errors
@handle_database_errors
async def create_golf_course(
    course: GolfCourseCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[SessionLocal, Depends(get_db)]
) -> Dict[str, Any]:
    if course.par <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Par must be greater than 0"
        )
    try:
        created_at = datetime.fromisoformat(course.created_at)
        updated_at = datetime.fromisoformat(course.updated_at)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid date format. Please use ISO format (YYYY-MM-DDTHH:MM:SS)"
        )
    db_course = GolfCourse(
        name=course.name,
        location=course.location,
        par=course.par,
        rating=course.rating,
        slope=course.slope,
        created_at=created_at,
        updated_at=updated_at
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return {
        "id": db_course.id,
        "name": db_course.name,
        "location": db_course.location,
        "par": db_course.par,
        "rating": db_course.rating,
        "slope": db_course.slope,
        "created_at": db_course.created_at.isoformat(),
        "updated_at": db_course.updated_at.isoformat()
    }

@app.post("/rounds/", response_model=Dict[str, Any])
@handle_authentication_errors
@handle_database_errors
async def create_golf_round(
    round: GolfRoundCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[SessionLocal, Depends(get_db)]
) -> Dict[str, Any]:
    try:
        date = datetime.fromisoformat(round.date)
        created_at = datetime.fromisoformat(round.created_at)
        updated_at = datetime.fromisoformat(round.updated_at)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid date format. Please use ISO format (YYYY-MM-DDTHH:MM:SS)"
        )
    db_round = GolfRound(
        user_id=round.user_id,
        course_id=round.course_id,
        date=date,
        total_score=round.total_score,
        weather=round.weather,
        temperature=round.temperature,
        created_at=created_at,
        updated_at=updated_at
    )
    db.add(db_round)
    db.commit()
    db.refresh(db_round)
    return {
        "id": db_round.id,
        "user_id": db_round.user_id,
        "course_id": db_round.course_id,
        "date": db_round.date.isoformat(),
        "total_score": db_round.total_score,
        "weather": db_round.weather,
        "temperature": db_round.temperature,
        "created_at": db_round.created_at.isoformat(),
        "updated_at": db_round.updated_at.isoformat()
    }

@app.post("/holes/", response_model=Dict[str, Any])
@handle_authentication_errors
@handle_database_errors
async def create_golf_hole(
    hole: GolfHoleCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[SessionLocal, Depends(get_db)]
) -> Dict[str, Any]:
    if hole.hole_number <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Hole number must be greater than 0"
        )
    try:
        created_at = datetime.fromisoformat(hole.created_at)
        updated_at = datetime.fromisoformat(hole.updated_at)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid date format. Please use ISO format (YYYY-MM-DDTHH:MM:SS)"
        )
    db_hole = GolfHole(
        round_id=hole.round_id,
        course_id=hole.course_id,
        hole_number=hole.hole_number,
        par=hole.par,
        score=hole.score,
        fairway_hit=hole.fairway_hit,
        green_in_regulation=hole.green_in_regulation,
        putts=hole.putts,
        created_at=created_at,
        updated_at=updated_at
    )
    db.add(db_hole)
    db.commit()
    db.refresh(db_hole)
    return {
        "id": db_hole.id,
        "round_id": db_hole.round_id,
        "course_id": db_hole.course_id,
        "hole_number": db_hole.hole_number,
        "par": db_hole.par,
        "score": db_hole.score,
        "fairway_hit": db_hole.fairway_hit,
        "green_in_regulation": db_hole.green_in_regulation,
        "putts": db_hole.putts,
        "created_at": db_hole.created_at.isoformat(),
        "updated_at": db_hole.updated_at.isoformat()
    }

@app.post("/users/", response_model=Dict[str, Any])
@handle_database_errors
async def create_user(user: UserCreate, db: SessionLocal = Depends(get_db)):
    # ユーザー名の重複チェック
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # メールアドレスの重複チェック
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # ユーザーオブジェクトの作成
    db_user = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=get_password_hash(user.password),
        height=user.height,
        weight=user.weight,
        age=user.age,
        gender=user.gender,
        handicap=user.handicap
    )
    
    # データベースに保存
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return {
        "id": db_user.id,
        "username": db_user.username,
        "email": db_user.email,
        "full_name": db_user.full_name,
        "height": db_user.height,
        "weight": db_user.weight,
        "age": db_user.age,
        "gender": db_user.gender,
        "handicap": db_user.handicap
    } 