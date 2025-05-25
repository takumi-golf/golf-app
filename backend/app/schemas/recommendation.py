from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Any
from datetime import datetime

class PlayerProfile(BaseModel):
    """プレイヤープロファイルのスキーマ"""
    id: int
    head_speed: float
    handicap: float
    age: int
    gender: str
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }

class PlayerProfileCreate(BaseModel):
    """プレイヤープロファイル作成のスキーマ"""
    head_speed: float
    handicap: float
    age: int
    gender: str

class PlayerClubSetup(BaseModel):
    """プレイヤーのクラブセットアップのスキーマ"""
    id: Optional[int] = None
    player_profile_id: int
    club_type: str = Field(..., description="クラブタイプ", example="driver")
    brand: str = Field(..., description="ブランド名", example="XXIO")
    model: str = Field(..., description="モデル名", example="12")
    loft: float = Field(..., description="ロフト角", example=10.5)
    shaft: str = Field(..., description="シャフト", example="MP1200")
    flex: str = Field(..., description="フレックス", example="S")

    class Config:
        from_attributes = True

class PlayerClubSetupCreate(PlayerClubSetup):
    """プレイヤーのクラブセットアップ作成用スキーマ"""
    pass

class RecommendationRequest(BaseModel):
    """レコメンデーションリクエストのスキーマ"""
    head_speed: float = Field(..., description="ヘッドスピード", example=40.5)
    handicap: float = Field(..., description="ハンディキャップ", example=15.0)
    age: int = Field(..., description="年齢", example=35)
    gender: str = Field(..., description="性別", example="male")

    @field_validator('gender')
    def validate_gender(cls, v):
        if v not in ['male', 'female']:
            raise ValueError('性別は"male"または"female"である必要があります')
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "head_speed": 40.5,
                "handicap": 15.0,
                "age": 35,
                "gender": "male"
            }
        }
    }

class RecommendationResponse(BaseModel):
    """レコメンデーションレスポンスのスキーマ"""
    id: int
    player_profile_id: int
    segment: str = Field(..., description="プレイヤーセグメント")
    shaft_recommendation: str = Field(..., description="推奨シャフト")
    created_at: datetime
    feedback: Optional[str] = None
    rating: Optional[int] = None

    model_config = {
        "from_attributes": True
    }

class RecommendationCreate(BaseModel):
    """レコメンデーション作成のスキーマ"""
    player_profile_id: int
    segment: str
    shaft_recommendation: str

class ClubSpecificationResponse(BaseModel):
    """クラブ仕様のレスポンススキーマ"""
    brand: str
    model: str
    club_type: str
    loft: float
    lie_angle: Optional[float] = None
    length: Optional[float] = None
    shaft: Optional[str] = None
    flex: Optional[str] = None

class RecommendedClub(BaseModel):
    """推奨クラブのスキーマ"""
    club_type: str
    specifications: ClubSpecificationResponse

class RecommendationList(BaseModel):
    """レコメンデーション一覧のスキーマ"""
    recommendations: List[RecommendationResponse]
    total: int

class Feedback(BaseModel):
    """フィードバックのスキーマ"""
    feedback: str = Field(..., description="フィードバック内容")
    rating: int = Field(..., description="評価（1-5）", ge=1, le=5)

class FeedbackCreate(BaseModel):
    """フィードバック作成のスキーマ"""
    feedback: str
    rating: int = Field(..., ge=1, le=5) 