from fastapi import FastAPI, HTTPException, status, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from typing import List, Optional, Dict
from pydantic import BaseModel
import random
from datetime import datetime
from . import schemas
from .core.config import settings
from .core.error_handlers import (
    http_exception_handler,
    validation_exception_handler,
    sqlalchemy_exception_handler
)
import logging
from .api.endpoints import recommendations, clubs, users
from .db.init_db import init_db
from sqlalchemy.orm import Session
from .db.database import get_db, engine, Base
from .recommendation_engine import GolfClubRecommender
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

# ロギングの設定
logger = logging.getLogger(__name__)

# データベーステーブルの作成
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """アプリケーションのライフスパンイベントを管理"""
    # 起動時の処理
    init_db()
    yield
    # シャットダウン時の処理
    pass

app = FastAPI(
    title="SwingFit Pro API",
    description="ゴルフクラブレコメンデーションシステムのAPI",
    version="1.0.0",
    lifespan=lifespan
)

# CORSミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# エラーハンドラーの登録
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)

@app.get("/")
def read_root():
    return {"message": "ゴルフクラブレコメンデーションAPIへようこそ"}

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
        "cors_origins": settings.BACKEND_CORS_ORIGINS,
        "log_level": settings.LOG_LEVEL
    }

# ルーターの登録
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(recommendations.router, prefix="/api/v1/recommendations", tags=["recommendations"])
app.include_router(clubs.router, prefix="/api/clubs", tags=["clubs"]) 