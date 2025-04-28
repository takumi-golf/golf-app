from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib
import os
from dotenv import load_dotenv
from database import SessionLocal, Club
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from config import ACCESS_TOKEN_EXPIRE_MINUTES
from security import create_access_token, get_current_user, verify_password, get_password_hash
from error_handlers import handle_database_errors, handle_validation_errors, handle_authentication_errors, global_exception_handler

# 環境変数の読み込み
load_dotenv()

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

# グローバル例外ハンドラの登録
app.add_exception_handler(Exception, global_exception_handler)

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

@app.post("/token",
    response_model=Dict[str, str],
    summary="アクセストークンの取得",
    description="""
    ユーザー認証を行い、アクセストークンを発行します。
    
    - username: ユーザー名
    - password: パスワード
    """,
    response_description="アクセストークンとトークンタイプ",
    tags=["認証"]
)
@handle_authentication_errors
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    ユーザー認証を行い、アクセストークンを発行します。
    
    Args:
        form_data (OAuth2PasswordRequestForm): ユーザー名とパスワード
        
    Returns:
        Dict[str, str]: アクセストークンとトークンタイプ
        
    Raises:
        HTTPException: 認証失敗時
    """
    if form_data.username != "test" or form_data.password != "test":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ユーザー名またはパスワードが正しくありません",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me",
    response_model=Dict[str, str],
    summary="現在のユーザー情報を取得",
    description="認証されたユーザーの情報を返します。",
    response_description="ユーザー情報",
    tags=["ユーザー"]
)
async def read_users_me(current_user = Depends(get_current_user)):
    """
    現在認証されているユーザーの情報を返します。
    
    Args:
        current_user: 現在のユーザー（認証必須）
        
    Returns:
        Dict[str, str]: ユーザー情報
    """
    return current_user

@app.post("/recommend",
    response_model=ClubRecommendation,
    summary="クラブの推奨セットを取得",
    description="""
    ユーザープロファイルに基づいて、最適なクラブセットを推奨します。
    
    推奨内容:
    - ドライバー
    - フェアウェイウッド
    - ユーティリティ
    - アイアンセット
    - ウェッジ
    - パター
    
    また、セット全体の価格と推奨の信頼度スコアも提供します。
    """,
    response_description="推奨クラブセットの詳細情報",
    tags=["フィッティング"]
)
async def recommend_clubs(
    profile: UserProfile,
    current_user: Dict = Depends(get_current_user)
):
    """
    ユーザープロファイルに基づいて、最適なクラブセットを推奨します。
    
    Args:
        profile (UserProfile): ユーザーのプロファイル情報
        current_user (Dict): 現在のユーザー（認証必須）
        
    Returns:
        ClubRecommendation: 推奨クラブセットの詳細
        
    Raises:
        HTTPException: モデル読み込みエラーまたは推奨生成エラー時
    """
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
        
        return {
            **recommendations,
            "confidence_score": confidence_score,
            "timestamp": datetime.now()
        }
        
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