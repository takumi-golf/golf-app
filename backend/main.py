from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import uvicorn

from app.database.database import get_db, engine, SessionLocal
from app.models import club, recommendation
from app.schemas import club as schemas
from app.api.api import api_router
from app.core.config import settings
from app.database.init_data import init_db
from app.core.error_handlers import (
    DatabaseError,
    ValidationError,
    database_exception_handler,
    validation_exception_handler,
    sqlalchemy_exception_handler
)
from sqlalchemy.exc import SQLAlchemyError

# データベーステーブルの作成（メタデータを一度に作成）
Base = club.Base
Base.metadata.create_all(bind=engine)

# FastAPIアプリケーションの初期化
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# グローバルエラーハンドラの登録
app.add_exception_handler(DatabaseError, database_exception_handler)
app.add_exception_handler(ValidationError, validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)

# CORSの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# APIルーターを登録（プレフィックスを/apiに変更）
app.include_router(api_router, prefix="/api")

# アプリケーション起動時にテストデータを初期化
@app.on_event("startup")
async def startup_event():
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Golf Club Recommendation API"}

@app.get("/api/clubs", response_model=List[schemas.Club])
def get_clubs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    clubs = db.query(club.Club).offset(skip).limit(limit).all()
    return clubs

@app.get("/api/clubs/{club_type}", response_model=List[schemas.Club])
def get_clubs_by_type(club_type: str, db: Session = Depends(get_db)):
    clubs = db.query(club.Club).filter(club.Club.club_type == club_type).all()
    if not clubs:
        raise HTTPException(status_code=404, detail=f"No clubs found of type {club_type}")
    return clubs

@app.post("/api/clubs/", response_model=schemas.Club)
def create_club(club: schemas.ClubCreate, db: Session = Depends(get_db)):
    db_club = club.Club(**club.dict())
    db.add(db_club)
    db.commit()
    db.refresh(db_club)
    return db_club

@app.get("/api/clubs/brand/{brand}", response_model=List[schemas.Club])
def get_clubs_by_brand(brand: str, db: Session = Depends(get_db)):
    clubs = db.query(club.Club).filter(club.Club.brand == brand).all()
    if not clubs:
        raise HTTPException(status_code=404, detail=f"No clubs found for brand {brand}")
    return clubs

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True) 
