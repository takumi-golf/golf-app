from fastapi import APIRouter, Depends, HTTPException, status, Request, Body
from sqlalchemy.orm import Session
from typing import List, Optional
from ...db.database import get_db
from ...models.player import PlayerProfile, Recommendation
from ...schemas.recommendation import (
    RecommendationRequest,
    RecommendationResponse,
    RecommendationCreate,
    PlayerProfileCreate,
    FeedbackCreate
)
from ...recommendation_engine import GolfClubRecommender
from ...core.error_handlers import ErrorMessages
from pydantic import ValidationError, Field, validator

router = APIRouter()

class RecommendationRequestValidator(RecommendationRequest):
    head_speed: float = Field(gt=0, description="ヘッドスピード（m/s）")
    handicap: float = Field(ge=0, description="ハンディキャップ")
    age: int = Field(gt=0, description="年齢")
    gender: str = Field(description="性別")

    @validator('gender')
    def validate_gender(cls, v):
        if v.lower() not in ["male", "female"]:
            raise ValueError("性別は'male'または'female'である必要があります")
        return v.lower()

@router.post("/", response_model=RecommendationResponse)
def create_recommendation(request: RecommendationRequest, db: Session = Depends(get_db)):
    """新しいレコメンデーションを作成"""
    # レコメンダーの初期化
    recommender = GolfClubRecommender(db)
    
    # プレイヤープロファイルの作成
    player_profile = PlayerProfile(
        head_speed=request.head_speed,
        handicap=request.handicap,
        age=request.age,
        gender=request.gender
    )
    db.add(player_profile)
    db.commit()
    db.refresh(player_profile)

    # レコメンデーションの生成
    segment, shaft_recommendation = recommender.analyze_player(player_profile)

    # レコメンデーションの保存
    recommendation = Recommendation(
        player_profile_id=player_profile.id,
        user_id=1,  # TODO: 認証実装後に修正
        segment=segment,
        shaft_recommendation=shaft_recommendation
    )
    db.add(recommendation)
    db.commit()
    db.refresh(recommendation)

    return recommendation

@router.get("/", response_model=List[RecommendationResponse])
def read_recommendations(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """レコメンデーション一覧を取得"""
    recommendations = db.query(Recommendation).offset(skip).limit(limit).all()
    return recommendations

@router.get("/{recommendation_id}", response_model=RecommendationResponse)
def get_recommendation(recommendation_id: int, db: Session = Depends(get_db)):
    """指定されたIDのレコメンデーションを取得"""
    recommendation = db.query(Recommendation).filter(Recommendation.id == recommendation_id).first()
    if not recommendation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="指定されたレコメンデーションが見つかりません"
        )
    return recommendation

@router.post("/{recommendation_id}/feedback")
def add_feedback(recommendation_id: int, feedback: FeedbackCreate, db: Session = Depends(get_db)):
    """レコメンデーションにフィードバックを追加"""
    recommendation = db.query(Recommendation).filter(Recommendation.id == recommendation_id).first()
    if not recommendation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="指定されたレコメンデーションが見つかりません"
        )

    recommendation.feedback = feedback.feedback
    recommendation.rating = feedback.rating
    db.commit()
    db.refresh(recommendation)
    return {"message": "フィードバックが正常に追加されました"} 

@router.post("/sets")
def recommend_sets(
    payload: dict = Body(...)
):
    """
    複数の14本クラブセット（マッチ度付き）を返す（ダミーデータ）
    """
    # ダミーデータ例
    sets = [
        {
            "match": 95,
            "set_name": "バランス重視セット",
            "description": "初心者～中級者向けのバランス型セットです。",
            "clubs": [
                {"type": "ドライバー", "brand": "XXIO", "model": "XXIO 12", "flex": "R"},
                {"type": "3W", "brand": "テーラーメイド", "model": "SIM2", "flex": "SR"},
                {"type": "5W", "brand": "キャロウェイ", "model": "MAVRIK", "flex": "S"},
                {"type": "4U", "brand": "PING", "model": "G425", "flex": "SR"},
                {"type": "5I", "brand": "ミズノ", "model": "JPX921", "flex": "R"},
                {"type": "6I", "brand": "ミズノ", "model": "JPX921", "flex": "R"},
                {"type": "7I", "brand": "ミズノ", "model": "JPX921", "flex": "R"},
                {"type": "8I", "brand": "ミズノ", "model": "JPX921", "flex": "R"},
                {"type": "9I", "brand": "ミズノ", "model": "JPX921", "flex": "R"},
                {"type": "PW", "brand": "ミズノ", "model": "JPX921", "flex": "R"},
                {"type": "AW", "brand": "タイトリスト", "model": "VOKEY", "flex": "S"},
                {"type": "SW", "brand": "タイトリスト", "model": "VOKEY", "flex": "S"},
                {"type": "LW", "brand": "タイトリスト", "model": "VOKEY", "flex": "S"},
                {"type": "パター", "brand": "オデッセイ", "model": "WHITE HOT", "flex": ""}
            ]
        },
        {
            "match": 90,
            "set_name": "飛距離重視セット",
            "description": "飛距離を伸ばしたい方におすすめのセットです。",
            "clubs": [
                {"type": "ドライバー", "brand": "キャロウェイ", "model": "ROGUE ST", "flex": "S"},
                {"type": "3W", "brand": "キャロウェイ", "model": "ROGUE ST", "flex": "S"},
                {"type": "5W", "brand": "テーラーメイド", "model": "SIM2", "flex": "S"},
                {"type": "4U", "brand": "PING", "model": "G425", "flex": "S"},
                {"type": "5I", "brand": "ブリヂストン", "model": "TOUR B", "flex": "S"},
                {"type": "6I", "brand": "ブリヂストン", "model": "TOUR B", "flex": "S"},
                {"type": "7I", "brand": "ブリヂストン", "model": "TOUR B", "flex": "S"},
                {"type": "8I", "brand": "ブリヂストン", "model": "TOUR B", "flex": "S"},
                {"type": "9I", "brand": "ブリヂストン", "model": "TOUR B", "flex": "S"},
                {"type": "PW", "brand": "ブリヂストン", "model": "TOUR B", "flex": "S"},
                {"type": "AW", "brand": "クリーブランド", "model": "RTX ZIPCORE", "flex": "S"},
                {"type": "SW", "brand": "クリーブランド", "model": "RTX ZIPCORE", "flex": "S"},
                {"type": "LW", "brand": "クリーブランド", "model": "RTX ZIPCORE", "flex": "S"},
                {"type": "パター", "brand": "スコッティキャメロン", "model": "SELECT", "flex": ""}
            ]
        }
    ]
    return sets 