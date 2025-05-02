from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
import os

# データベースURL
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# エンジンの作成
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# セッションファクトリの作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# モデルのベースクラス
Base = declarative_base()

# データベースの初期化
def init_db():
    if not os.path.exists("./sql_app.db"):
        Base.metadata.create_all(bind=engine)

# データベースのクリーンアップ
def cleanup_db():
    if os.path.exists("./sql_app.db"):
        os.remove("./sql_app.db")

# データベースセッションの依存性
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 