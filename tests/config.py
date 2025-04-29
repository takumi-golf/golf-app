import os

# データベース設定
DATABASE_URL = "sqlite:///./test.db"
SQL_ECHO = False

# Redis設定
REDIS_URL = "redis://localhost:6379/0"

# JWT設定
JWT_SECRET_KEY = "test_secret_key"
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# テスト環境フラグ
os.environ["TESTING"] = "1" 