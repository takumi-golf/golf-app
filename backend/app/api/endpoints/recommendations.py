from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.core.error_handlers import error_handler, ValidationError, DatabaseError
from app.models import recommendation as models
from app.schemas import recommendation as schemas

router = APIRouter()

@router.post("/", response_model=schemas.Recommendation)
@error_handler
async def create_recommendation(
    recommendation: schemas.RecommendationCreate,
    db: Session = Depends(get_db)
):
    """ゴルフクラブのレコメンデーションを作成"""
    try:
        db_recommendation = models.Recommendation(**recommendation.dict())
        db.add(db_recommendation)
        db.commit()
        db.refresh(db_recommendation)
        return db_recommendation
    except Exception as e:
        db.rollback()
        raise DatabaseError("レコメンデーションの作成に失敗しました", original_error=e)

@router.get("/", response_model=List[schemas.Recommendation])
@error_handler
async def get_recommendations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """レコメンデーション一覧を取得"""
    try:
        recommendations = db.query(models.Recommendation).offset(skip).limit(limit).all()
        return recommendations
    except Exception as e:
        raise DatabaseError("レコメンデーションの取得に失敗しました", original_error=e)

@router.get("/{recommendation_id}", response_model=schemas.Recommendation)
@error_handler
async def get_recommendation(
    recommendation_id: int,
    db: Session = Depends(get_db)
):
    """特定のレコメンデーションを取得"""
    try:
        recommendation = db.query(models.Recommendation).filter(
            models.Recommendation.id == recommendation_id
        ).first()
        if not recommendation:
            raise ValidationError(
                message=f"ID {recommendation_id} のレコメンデーションが見つかりません",
                field="recommendation_id"
            )
        return recommendation
    except ValidationError:
        raise
    except Exception as e:
        raise DatabaseError("レコメンデーションの取得に失敗しました", original_error=e)

@router.put("/{recommendation_id}", response_model=schemas.Recommendation)
@error_handler
async def update_recommendation(
    recommendation_id: int,
    recommendation: schemas.RecommendationUpdate,
    db: Session = Depends(get_db)
):
    """レコメンデーションを更新"""
    try:
        db_recommendation = db.query(models.Recommendation).filter(
            models.Recommendation.id == recommendation_id
        ).first()
        if not db_recommendation:
            raise ValidationError(
                message=f"ID {recommendation_id} のレコメンデーションが見つかりません",
                field="recommendation_id"
            )
        
        for key, value in recommendation.dict(exclude_unset=True).items():
            setattr(db_recommendation, key, value)
        
        db.commit()
        db.refresh(db_recommendation)
        return db_recommendation
    except ValidationError:
        raise
    except Exception as e:
        db.rollback()
        raise DatabaseError("レコメンデーションの更新に失敗しました", original_error=e)

@router.delete("/{recommendation_id}")
@error_handler
async def delete_recommendation(
    recommendation_id: int,
    db: Session = Depends(get_db)
):
    """レコメンデーションを削除"""
    try:
        db_recommendation = db.query(models.Recommendation).filter(
            models.Recommendation.id == recommendation_id
        ).first()
        if not db_recommendation:
            raise ValidationError(
                message=f"ID {recommendation_id} のレコメンデーションが見つかりません",
                field="recommendation_id"
            )
        
        db.delete(db_recommendation)
        db.commit()
        return {"message": "レコメンデーションを削除しました"}
    except ValidationError:
        raise
    except Exception as e:
        db.rollback()
        raise DatabaseError("レコメンデーションの削除に失敗しました", original_error=e) 