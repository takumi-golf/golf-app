from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.core.config import settings
import os

# データベースファイルのパスを絶対パスに変換
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../golf_clubs.db"))
db_url = f"sqlite:///{db_path}"

engine = create_engine(
    db_url,
    connect_args={"check_same_thread": False}  # SQLite用の設定
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 