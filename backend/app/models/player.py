from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..db.database import Base
from .club import Brand, ClubModel, ClubSpecification, Shaft

class User(Base):
    """ユーザーモデル"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # リレーションシップ
    recommendations = relationship("Recommendation", back_populates="user", foreign_keys="[Recommendation.user_id]")

class PlayerProfile(Base):
    """プレイヤープロファイルモデル"""
    __tablename__ = "player_profiles"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=True)  # プロ、アマチュア
    name = Column(String, nullable=True)  # プロの場合は名前
    head_speed = Column(Float, nullable=False)
    handicap = Column(Float, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # リレーションシップ
    recommendations = relationship("Recommendation", back_populates="player_profile", cascade="all, delete-orphan")
    club_setups = relationship("PlayerClubSetup", back_populates="player", cascade="all, delete-orphan")

class PlayerClubSetup(Base):
    """プレイヤーのクラブセットアップモデル"""
    __tablename__ = "player_club_setups"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("player_profiles.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # リレーションシップ
    player = relationship("PlayerProfile", back_populates="club_setups")
    clubs = relationship("PlayerClub", back_populates="setup", cascade="all, delete-orphan")

class PlayerClub(Base):
    """プレイヤーのクラブモデル"""
    __tablename__ = "player_clubs"

    id = Column(Integer, primary_key=True, index=True)
    setup_id = Column(Integer, ForeignKey("player_club_setups.id"))
    specification_id = Column(Integer, ForeignKey("club_specifications.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # リレーションシップ
    setup = relationship("PlayerClubSetup", back_populates="clubs")
    specification = relationship("ClubSpecification")

class Recommendation(Base):
    """レコメンデーションモデル"""
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    player_profile_id = Column(Integer, ForeignKey("player_profiles.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    segment = Column(String, nullable=False)
    shaft_recommendation = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    feedback = Column(Text, nullable=True)
    rating = Column(Integer, nullable=True)

    # リレーションシップ
    player_profile = relationship("PlayerProfile", back_populates="recommendations")
    user = relationship("User", back_populates="recommendations", foreign_keys=[user_id]) 