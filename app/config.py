import os
from dotenv import load_dotenv

# .envファイルを読み込む
load_dotenv()

# データベース設定
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./golf.db")
SQL_ECHO = os.getenv("SQL_ECHO", "False").lower() == "true"

# キャッシュ設定
CACHE_TTL = int(os.getenv("CACHE_TTL", "3600"))  # 1時間
MAX_CACHE_SIZE = int(os.getenv("MAX_CACHE_SIZE", "1000"))
CACHE_CLEANUP_INTERVAL = int(os.getenv("CACHE_CLEANUP_INTERVAL", "300"))  # 5分

# Slack設定
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

# アプリケーション設定
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

# ログ設定
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "app.log") 