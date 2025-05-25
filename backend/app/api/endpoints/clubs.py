from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from ...db.database import get_db
from ...models.player import Brand, ClubModel, ClubSpecification, Shaft
from ...schemas.club import (
    BrandSchema,
    BrandCreate,
    ClubModelSchema,
    ClubModelCreate,
    ClubSpecificationSchema,
    ClubSpecificationCreate,
    ShaftCreate,
    ShaftResponse
)

router = APIRouter()

@router.get("/brands/", response_model=List[BrandSchema])
def get_brands(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """利用可能なブランドの一覧を取得"""
    brands = db.query(Brand).offset(skip).limit(limit).all()
    return brands

@router.post("/brands/", response_model=BrandSchema)
def create_brand(
    brand: BrandCreate,
    db: Session = Depends(get_db)
):
    """新しいブランドを作成"""
    db_brand = Brand(**brand.model_dump())
    db.add(db_brand)
    db.commit()
    db.refresh(db_brand)
    return db_brand

@router.get("/models/", response_model=List[ClubModelSchema])
def get_club_models(
    brand_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """クラブモデルの一覧を取得（オプションでブランドでフィルタリング）"""
    query = db.query(ClubModel)
    if brand_id:
        query = query.filter(ClubModel.brand_id == brand_id)
    models = query.offset(skip).limit(limit).all()
    return models

@router.post("/models/", response_model=ClubModelSchema)
def create_club_model(
    model: ClubModelCreate,
    db: Session = Depends(get_db)
):
    """新しいクラブモデルを作成"""
    db_model = ClubModel(**model.model_dump())
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model

@router.get("/specifications/{club_model_id}", response_model=List[ClubSpecificationSchema])
def get_club_specifications(
    club_model_id: int,
    db: Session = Depends(get_db)
):
    """特定のクラブモデルのスペックを取得"""
    specifications = db.query(ClubSpecification).filter(
        ClubSpecification.club_model_id == club_model_id
    ).all()
    
    if not specifications:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Club specifications not found"
        )
    
    return specifications

@router.post("/specifications/", response_model=ClubSpecificationSchema)
def create_club_specification(
    specification: ClubSpecificationCreate,
    db: Session = Depends(get_db)
):
    """新しいクラブスペックを作成"""
    db_spec = ClubSpecification(**specification.model_dump())
    db.add(db_spec)
    db.commit()
    db.refresh(db_spec)
    return db_spec

@router.post("/shafts/", response_model=ShaftResponse, status_code=status.HTTP_201_CREATED)
def create_shaft(shaft: ShaftCreate, db: Session = Depends(get_db)):
    """新しいシャフトを作成"""
    db_shaft = Shaft(**shaft.dict())
    db.add(db_shaft)
    db.commit()
    db.refresh(db_shaft)
    return db_shaft

@router.get("/shafts/", response_model=List[ShaftResponse])
def get_shafts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """シャフトの一覧を取得"""
    shafts = db.query(Shaft).offset(skip).limit(limit).all()
    return shafts

@router.get("/shafts/{shaft_id}", response_model=ShaftResponse)
def get_shaft(shaft_id: int, db: Session = Depends(get_db)):
    """特定のシャフトを取得"""
    shaft = db.query(Shaft).filter(Shaft.id == shaft_id).first()
    if shaft is None:
        raise HTTPException(status_code=404, detail="シャフトが見つかりません")
    return shaft 