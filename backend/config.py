import os
from pathlib import Path
from dotenv import load_dotenv

# 環境変数ファイルの読み込み
env = os.getenv("ENV", "development")
env_file = f".env.{env}"
load_dotenv(env_file)

class Settings:
    # 基本設定
    ENV: str = os.getenv("ENV", "development")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # API設定
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    
    # CORS設定
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
    
    # データベース設定
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./dev.db")
    
    # Google Analytics設定
    GA_MEASUREMENT_ID: str = os.getenv("GA_MEASUREMENT_ID", "")
    
    # ログ設定
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # 環境判定
    @property
    def is_development(self) -> bool:
        return self.ENV == "development"
    
    @property
    def is_staging(self) -> bool:
        return self.ENV == "staging"
    
    @property
    def is_production(self) -> bool:
        return self.ENV == "production"

# 設定インスタンスの作成
settings = Settings() 