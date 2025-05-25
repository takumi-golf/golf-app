from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import os
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "ゴルフクラブレコメンデーションAPI"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True
    SQL_ECHO: bool = True
    ENVIRONMENT: str = "development"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    LOG_LEVEL: str = "INFO"
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1"]
    LOG_FILE: str = "app.log"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="allow")

    # API設定
    API_V1_STR: str = "/api/v1"
    
    # CORS設定
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000"]
    
    # セキュリティ設定
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # キャッシュ設定
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", "3600"))  # 1時間
    MAX_CACHE_SIZE: int = int(os.getenv("MAX_CACHE_SIZE", "1000"))
    CACHE_CLEANUP_INTERVAL: int = int(os.getenv("CACHE_CLEANUP_INTERVAL", "300"))  # 5分

    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT == "development"

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings() 