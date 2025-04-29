from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean, JSON, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import logging

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('partitioning.log'),
        logging.StreamHandler()
    ]
)

Base = declarative_base()

class PartitionedUser(Base):
    __tablename__ = "partitioned_users"
    __table_args__ = (
        # パーティショニングのためのチェック制約
        CheckConstraint('height >= 0', name='height_positive'),
        CheckConstraint('weight >= 0', name='weight_positive'),
        CheckConstraint('age >= 0', name='age_positive'),
    )

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

    # パーティショニングキー
    partition_key = Column(Integer, index=True)

    recommendations = relationship("PartitionedRecommendation", back_populates="user")
    feedback = relationship("PartitionedUserFeedback", back_populates="user")

class PartitionedClub(Base):
    __tablename__ = "partitioned_clubs"
    __table_args__ = (
        # パーティショニングのためのチェック制約
        CheckConstraint('price >= 0', name='price_positive'),
        CheckConstraint('popularity_score >= 0', name='popularity_positive'),
    )

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

    # パーティショニングキー
    partition_key = Column(Integer, index=True)

    recommendations = relationship("PartitionedRecommendation", back_populates="club")
    performance_data = relationship("PartitionedClubPerformance", back_populates="club")

class PartitionedRecommendation(Base):
    __tablename__ = "partitioned_recommendations"
    __table_args__ = (
        # パーティショニングのためのチェック制約
        CheckConstraint('confidence_score >= 0 AND confidence_score <= 1', name='confidence_range'),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("partitioned_users.id"), index=True)
    club_id = Column(Integer, ForeignKey("partitioned_clubs.id"), index=True)
    confidence_score = Column(Float, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)

    # パーティショニングキー
    partition_key = Column(Integer, index=True)

    user = relationship("PartitionedUser", back_populates="recommendations")
    club = relationship("PartitionedClub", back_populates="recommendations")

class PartitionedUserFeedback(Base):
    __tablename__ = "partitioned_user_feedback"
    __table_args__ = (
        # パーティショニングのためのチェック制約
        CheckConstraint('rating >= 1 AND rating <= 5', name='rating_range'),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("partitioned_users.id"), index=True)
    club_id = Column(Integer, ForeignKey("partitioned_clubs.id"), index=True)
    rating = Column(Integer, index=True)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # パーティショニングキー
    partition_key = Column(Integer, index=True)

    user = relationship("PartitionedUser", back_populates="feedback")
    club = relationship("PartitionedClub")

class PartitionedClubPerformance(Base):
    __tablename__ = "partitioned_club_performance"

    id = Column(Integer, primary_key=True, index=True)
    club_id = Column(Integer, ForeignKey("partitioned_clubs.id"), index=True)
    head_speed_range = Column(String, index=True)
    ball_speed_range = Column(String, index=True)
    launch_angle_range = Column(String, index=True)
    spin_rate_range = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)

    # パーティショニングキー
    partition_key = Column(Integer, index=True)

    club = relationship("PartitionedClub", back_populates="performance_data")

def create_partition_tables(engine):
    """
    パーティションテーブルを作成
    :param engine: SQLAlchemyエンジン
    """
    try:
        # パーティションテーブルの作成
        Base.metadata.create_all(bind=engine)
        logging.info("Partitioned tables created successfully")
    except Exception as e:
        logging.error(f"Failed to create partitioned tables: {str(e)}")
        raise

def migrate_data_to_partitions(db_session, source_model, target_model, partition_size: int = 1000):
    """
    既存のデータをパーティションテーブルに移行
    :param db_session: データベースセッション
    :param source_model: 移行元のモデル
    :param target_model: 移行先のモデル
    :param partition_size: パーティションサイズ
    """
    try:
        # 既存のデータを取得
        source_data = db_session.query(source_model).all()
        
        # パーティションごとにデータを移行
        for i, item in enumerate(source_data):
            partition_key = i // partition_size
            target_item = target_model(**item.__dict__)
            target_item.partition_key = partition_key
            db_session.add(target_item)
        
        db_session.commit()
        logging.info(f"Data migrated successfully from {source_model.__name__} to {target_model.__name__}")
    except Exception as e:
        db_session.rollback()
        logging.error(f"Failed to migrate data: {str(e)}")
        raise 