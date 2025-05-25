from pydantic_settings import BaseSettings
from typing import List
import os
import logging

class Settings(BaseSettings):
    # 環境設定
    ENV: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    # APIサーバー設定
    API_HOST: str = "localhost"
    API_PORT: int = 8000
    API_V1_STR: str = "/api/v1"

    # データベース設定
    DATABASE_URL: str = "sqlite:///./golf_recommendation.db"

    # CORS設定
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    # JWT設定
    SECRET_KEY: str = "your-secret-key"  # 本番環境では必ず変更すること
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # その他の設定
    PROJECT_NAME: str = "SwingFit Pro"
    VERSION: str = "1.0.0"

    class Config:
        case_sensitive = True

    @property
    def is_development(self) -> bool:
        return self.ENV.lower() == "development"

settings = Settings()

# ロギングの設定
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
) 