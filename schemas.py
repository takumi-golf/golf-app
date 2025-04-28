from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict
from datetime import datetime

class UserBase(BaseModel):
    height: float
    weight: float
    age: int
    gender: str
    handicap: Optional[float] = None
    average_score: Optional[int] = None
    head_speed: Optional[float] = None
    ball_speed: Optional[float] = None
    launch_angle: Optional[float] = None
    swing_issue: Optional[str] = None

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class ClubBase(BaseModel):
    """クラブの基本情報モデル"""
    club_id: int = Field(..., description="クラブのID")
    brand: str = Field(..., description="メーカー名")
    model: str = Field(..., description="モデル名")
    loft: float = Field(..., description="ロフト角（度）")
    shaft: str = Field(..., description="シャフト名")
    shaft_flex: str = Field(..., description="シャフトフレックス（L, A, R, S, X）")
    price: int = Field(..., description="価格（円）")
    features: str = Field(..., description="クラブの特徴")

    class Config:
        schema_extra = {
            "example": {
                "club_id": 1,
                "brand": "XXIO",
                "model": "12",
                "loft": 10.5,
                "shaft": "MP1200",
                "shaft_flex": "R",
                "price": 80000,
                "features": "寛容性が高く、初級者から中級者向けのドライバー"
            }
        }

class ClubCreate(ClubBase):
    pass

class Club(ClubBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class RecommendationBase(BaseModel):
    user_id: int
    total_price: int

class RecommendationCreate(RecommendationBase):
    pass

class Recommendation(RecommendationBase):
    id: int
    created_at: datetime
    clubs: List[Club] = []

    class Config:
        orm_mode = True

class ClubRecommendation(BaseModel):
    """クラブ推奨セットのレスポンスモデル"""
    driver: ClubBase = Field(..., description="推奨ドライバー")
    woods: List[ClubBase] = Field(..., description="推奨フェアウェイウッド", max_items=2)
    utilities: List[ClubBase] = Field(..., description="推奨ユーティリティ", max_items=1)
    irons: List[ClubBase] = Field(..., description="推奨アイアンセット", max_items=7)
    wedges: List[ClubBase] = Field(..., description="推奨ウェッジ", max_items=2)
    putter: ClubBase = Field(..., description="推奨パター")
    total_price: float = Field(..., description="セット合計価格（円）")
    confidence_score: float = Field(..., ge=0, le=1, description="推奨の信頼度スコア（0-1）")
    timestamp: datetime = Field(..., description="推奨生成日時")

    class Config:
        schema_extra = {
            "example": {
                "driver": {
                    "club_id": 1,
                    "brand": "XXIO",
                    "model": "12",
                    "loft": 10.5,
                    "shaft": "MP1200",
                    "shaft_flex": "R",
                    "price": 80000,
                    "features": "寛容性が高く、初級者から中級者向けのドライバー"
                },
                "woods": [
                    {
                        "club_id": 2,
                        "brand": "XXIO",
                        "model": "12",
                        "loft": 15,
                        "shaft": "MP1200",
                        "shaft_flex": "R",
                        "price": 50000,
                        "features": "3番フェアウェイウッド"
                    }
                ],
                "utilities": [
                    {
                        "club_id": 3,
                        "brand": "XXIO",
                        "model": "12U",
                        "loft": 22,
                        "shaft": "MP1200",
                        "shaft_flex": "R",
                        "price": 30000,
                        "features": "4番ユーティリティ"
                    }
                ],
                "irons": [
                    {
                        "club_id": 4,
                        "brand": "XXIO",
                        "model": "12",
                        "loft": 24,
                        "shaft": "MP1200",
                        "shaft_flex": "R",
                        "price": 140000,
                        "features": "5-PW アイアンセット"
                    }
                ],
                "wedges": [
                    {
                        "club_id": 5,
                        "brand": "Cleveland",
                        "model": "RTX-4",
                        "loft": 52,
                        "shaft": "Dynamic Gold",
                        "shaft_flex": "S",
                        "price": 20000,
                        "features": "バンスが適度で扱いやすいウェッジ"
                    }
                ],
                "putter": {
                    "club_id": 6,
                    "brand": "Odyssey",
                    "model": "Stroke Lab",
                    "loft": 3,
                    "shaft": "Stroke Lab",
                    "shaft_flex": "Uniform",
                    "price": 30000,
                    "features": "マレットタイプのパター"
                },
                "total_price": 350000,
                "confidence_score": 0.85,
                "timestamp": "2024-03-20T10:30:00"
            }
        }

class Token(BaseModel):
    """アクセストークンのレスポンスモデル"""
    access_token: str = Field(..., description="JWTアクセストークン")
    token_type: str = Field(..., description="トークンタイプ（bearer）")

    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }

class UserInfo(BaseModel):
    """ユーザー情報のレスポンスモデル"""
    username: str = Field(..., description="ユーザー名")
    email: Optional[str] = Field(None, description="メールアドレス")
    full_name: Optional[str] = Field(None, description="フルネーム")
    is_active: bool = Field(True, description="アクティブ状態")

    class Config:
        schema_extra = {
            "example": {
                "username": "golfer123",
                "email": "golfer@example.com",
                "full_name": "山田 太郎",
                "is_active": True
            }
        }

class ErrorResponse(BaseModel):
    """エラーレスポンスモデル"""
    error: str = Field(..., description="エラーコード")
    message: str = Field(..., description="エラーメッセージ")
    debug_info: Optional[str] = Field(None, description="デバッグ情報（開発環境のみ）")

    class Config:
        schema_extra = {
            "example": {
                "error": "validation_error",
                "message": "入力値が不正です",
                "debug_info": None
            }
        } 