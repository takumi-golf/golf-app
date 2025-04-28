from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean, JSON, Index, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, joinedload, selectinload
from datetime import datetime
import os
import ssl
import logging
import time
from sqlalchemy.engine import Engine
from cache_manager import cached, cache
# from dotenv import load_dotenv

# load_dotenv()

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('database_access.log'),
        logging.StreamHandler()
    ]
)

# クエリパフォーマンス監視
@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    context._query_start_time = time.time()
    logging.info(f"SQL Query: {statement}")
    if parameters:
        logging.info(f"Parameters: {parameters}")

@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total_time = time.time() - context._query_start_time
    if total_time > 1.0:  # 1秒以上かかるクエリを警告
        logging.warning(f"Slow query detected: {statement}")
        logging.warning(f"Query time: {total_time:.2f} seconds")
    logging.info(f"Query completed in {total_time:.2f} seconds")

# 環境変数からデータベース接続情報を取得
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:your_password@localhost:5432/golfclub')

# PostgreSQL用の設定
engine_params = {
    'pool_pre_ping': True,  # 接続の死活監視
    'pool_recycle': 3600,   # 1時間で接続を再確立
    'pool_size': 5,         # 接続プールのサイズ
    'max_overflow': 10,     # 最大オーバーフロー接続数
    'pool_timeout': 30      # 接続タイムアウト（秒）
}

# エンジンの作成
engine = create_engine(
    DATABASE_URL,
    **engine_params,
    echo=os.getenv('SQL_ECHO', 'False').lower() == 'true'  # 環境変数でログ出力を制御
)

# セッションの作成
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False  # コミット後もオブジェクトを保持
)

# ベースクラスの作成
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    height = Column(Float, index=True)
    weight = Column(Float, index=True)
    age = Column(Integer, index=True)
    gender = Column(String, index=True)
    handicap = Column(Float, nullable=True, index=True)
    average_score = Column(Integer, nullable=True, index=True)
    head_speed = Column(Float, nullable=True, index=True)
    ball_speed = Column(Float, nullable=True, index=True)
    launch_angle = Column(Float, nullable=True, index=True)
    swing_issue = Column(String, nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)
    is_active = Column(Boolean, default=True, index=True)
    preferences = Column(JSON, nullable=True)

    recommendations = relationship("Recommendation", back_populates="user", lazy="selectin")
    feedback = relationship("UserFeedback", back_populates="user", lazy="selectin")

    __table_args__ = (
        Index('idx_user_handicap_swing', handicap, head_speed),
        Index('idx_user_active_handicap', is_active, handicap),
        Index('idx_user_swing_metrics', head_speed, ball_speed, launch_angle),
    )

class Club(Base):
    __tablename__ = "clubs"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, index=True)
    brand = Column(String, index=True)
    model = Column(String, index=True)
    loft = Column(Float, nullable=True, index=True)
    shaft = Column(String, nullable=True, index=True)
    shaft_flex = Column(String, nullable=True, index=True)
    price = Column(Integer, index=True)
    features = Column(Text)
    specifications = Column(JSON)
    popularity_score = Column(Float, default=0.0, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)
    is_available = Column(Boolean, default=True, index=True)

    recommendations = relationship("Recommendation", back_populates="club", lazy="selectin")
    performance_data = relationship("ClubPerformance", back_populates="club", lazy="selectin")

    __table_args__ = (
        Index('idx_club_type_brand', type, brand),
        Index('idx_club_loft_flex', loft, shaft_flex),
        Index('idx_club_availability', is_available, popularity_score),
    )

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    club_id = Column(Integer, ForeignKey("clubs.id"), index=True)
    confidence_score = Column(Float, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)

    user = relationship("User", back_populates="recommendations", lazy="joined")
    club = relationship("Club", back_populates="recommendations", lazy="joined")

    __table_args__ = (
        Index('idx_recommendation_user_club', user_id, club_id),
        Index('idx_recommendation_score', confidence_score),
        Index('idx_recommendation_user_score', user_id, confidence_score),
    )

class UserFeedback(Base):
    __tablename__ = "user_feedback"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    club_id = Column(Integer, ForeignKey("clubs.id"), index=True)
    rating = Column(Integer, index=True)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    user = relationship("User", back_populates="feedback", lazy="joined")
    club = relationship("Club", lazy="joined")

    __table_args__ = (
        Index('idx_feedback_user_club', user_id, club_id),
        Index('idx_feedback_rating', rating),
        Index('idx_feedback_user_rating', user_id, rating),
    )

class ClubPerformance(Base):
    __tablename__ = "club_performance"

    id = Column(Integer, primary_key=True, index=True)
    club_id = Column(Integer, ForeignKey("clubs.id"), index=True)
    head_speed_range = Column(String, index=True)
    ball_speed_range = Column(String, index=True)
    launch_angle_range = Column(String, index=True)
    spin_rate_range = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)

    club = relationship("Club", back_populates="performance_data", lazy="joined")

    __table_args__ = (
        Index('idx_performance_club_metrics', club_id, head_speed_range, ball_speed_range, launch_angle_range, spin_rate_range),
        Index('idx_performance_club_updated', club_id, updated_at),
    )

# データベースの初期化
def init_db():
    try:
        Base.metadata.create_all(bind=engine)
        logging.info("Database initialized successfully")
    except Exception as e:
        logging.error(f"Database initialization failed: {str(e)}")
        raise

# データベースセッションの依存性
def get_db():
    db = SessionLocal()
    try:
        logging.info("Database session started")
        yield db
    except Exception as e:
        logging.error(f"Database error: {str(e)}")
        raise
    finally:
        # セッションの統計情報を記録
        logging.info(f"Session statistics: {db.get_bind().pool.status()}")
        logging.info("Database session closed")
        db.close()

# キャッシュ付きのデータベース操作関数
@cached(ttl=300)  # 5分間キャッシュ
def get_user_by_id(db, user_id: int):
    return db.query(User).options(
        selectinload(User.recommendations),
        selectinload(User.feedback)
    ).filter(User.id == user_id).first()

@cached(ttl=300)
def get_club_by_id(db, club_id: int):
    return db.query(Club).options(
        selectinload(Club.recommendations),
        selectinload(Club.performance_data)
    ).filter(Club.id == club_id).first()

@cached(ttl=300)
def get_recommendations_by_user(db, user_id: int):
    return db.query(Recommendation).options(
        joinedload(Recommendation.club)
    ).filter(Recommendation.user_id == user_id).all()

@cached(ttl=300)
def get_feedback_by_user(db, user_id: int):
    return db.query(UserFeedback).options(
        joinedload(UserFeedback.club)
    ).filter(UserFeedback.user_id == user_id).all()

@cached(ttl=300)
def get_club_performance(db, club_id: int):
    return db.query(ClubPerformance).options(
        joinedload(ClubPerformance.club)
    ).filter(ClubPerformance.club_id == club_id).first()

# キャッシュを無効化する必要がある操作
def invalidate_user_cache(user_id: int):
    cache.delete(f"get_user_by_id:({user_id},)")
    cache.delete(f"get_recommendations_by_user:({user_id},)")
    cache.delete(f"get_feedback_by_user:({user_id},)")

def invalidate_club_cache(club_id: int):
    cache.delete(f"get_club_by_id:({club_id},)")
    cache.delete(f"get_club_performance:({club_id},)") 