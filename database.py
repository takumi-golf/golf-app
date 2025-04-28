from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

# 環境変数からデータベース接続情報を取得
DATABASE_URL = os.getenv('DATABASE_URL', 'mysql://user:password@localhost:3306/golfclub')

# エンジンの作成（MySQL用の設定を追加）
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # 接続の死活監視
    pool_recycle=3600,   # 1時間で接続を再確立
    echo=True           # SQLクエリのログ出力（開発時のみ）
)

# セッションの作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ベースクラスの作成
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    height = Column(Float)
    weight = Column(Float)
    age = Column(Integer)
    gender = Column(String)
    handicap = Column(Float, nullable=True)
    average_score = Column(Integer, nullable=True)
    head_speed = Column(Float, nullable=True)
    ball_speed = Column(Float, nullable=True)
    launch_angle = Column(Float, nullable=True)
    swing_issue = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    preferences = Column(JSON, nullable=True)  # ユーザーの好みを保存

    recommendations = relationship("Recommendation", back_populates="user")
    feedback = relationship("UserFeedback", back_populates="user")

class Club(Base):
    __tablename__ = "clubs"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)  # driver, wood, iron, wedge, putter
    brand = Column(String)
    model = Column(String)
    loft = Column(Float, nullable=True)
    shaft = Column(String, nullable=True)
    shaft_flex = Column(String, nullable=True)
    price = Column(Integer)
    features = Column(Text)
    specifications = Column(JSON)  # 詳細な仕様をJSONで保存
    popularity_score = Column(Float, default=0.0)  # 人気度スコア
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_available = Column(Boolean, default=True)

    recommendations = relationship("Recommendation", back_populates="club")
    performance_data = relationship("ClubPerformance", back_populates="club")

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    club_id = Column(Integer, ForeignKey("clubs.id"))
    confidence_score = Column(Float)  # レコメンデーションの信頼度
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="recommendations")
    club = relationship("Club", back_populates="recommendations")

class UserFeedback(Base):
    __tablename__ = "user_feedback"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    club_id = Column(Integer, ForeignKey("clubs.id"))
    rating = Column(Integer)  # 1-5の評価
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="feedback")
    club = relationship("Club")

class ClubPerformance(Base):
    __tablename__ = "club_performance"

    id = Column(Integer, primary_key=True, index=True)
    club_id = Column(Integer, ForeignKey("clubs.id"))
    head_speed_range = Column(String)  # 適正ヘッドスピード範囲
    ball_speed_range = Column(String)  # 適正ボールスピード範囲
    launch_angle_range = Column(String)  # 適正打ち出し角度範囲
    spin_rate_range = Column(String)  # 適正スピン率範囲
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    club = relationship("Club", back_populates="performance_data")

# データベースの初期化
def init_db():
    Base.metadata.create_all(bind=engine)

# データベースセッションの依存性
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 