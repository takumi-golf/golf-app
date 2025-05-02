from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Golf Club Recommendation"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # データベース設定
    SQLITE_DATABASE_URL: str = "sqlite:///./golf_clubs.db"
    POSTGRES_DATABASE_URL: Optional[str] = None
    
    # セキュリティ設定
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # CORS設定
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000"]
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 