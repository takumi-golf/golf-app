from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, JSON, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
import os
from datetime import datetime

# データベース接続設定
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
engine = create_engine(DATABASE_URL)
Base = declarative_base()

class Club(Base):
    __tablename__ = "clubs"

    id = Column(Integer, primary_key=True, index=True)
    club_id = Column(String, unique=True, index=True)
    brand = Column(String)
    model = Column(String)
    loft = Column(Float)
    shaft = Column(String)
    shaft_flex = Column(String)
    price = Column(Integer)
    features = Column(JSON)
    type = Column(String, index=True)
    specifications = Column(JSON)
    popularity_score = Column(Float, default=0.0, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)
    is_available = Column(Boolean, default=True, index=True)

class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, index=True)
    club_id = Column(Integer, ForeignKey("clubs.id"))
    old_price = Column(Integer)  # 変更前価格
    new_price = Column(Integer)  # 変更後価格
    changed_at = Column(DateTime)  # 価格変更日時

def create_tables():
    Base.metadata.create_all(bind=engine)
    print("テーブルの作成が完了しました。")

if __name__ == "__main__":
    create_tables() 