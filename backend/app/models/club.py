from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..db.database import Base

class Brand(Base):
    """ブランドモデル"""
    __tablename__ = "brands"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    logo_path = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    
    club_models = relationship("ClubModel", back_populates="brand", cascade="all, delete-orphan")

class ClubModel(Base):
    """クラブモデルモデル"""
    __tablename__ = "club_models"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False)
    release_year = Column(Integer, nullable=True)
    type = Column(String, nullable=False)  # driver, iron, etc.
    category = Column(String, nullable=False)  # player, game_improvement, etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    
    brand = relationship("Brand", back_populates="club_models")
    specifications = relationship("ClubSpecification", back_populates="club_model", cascade="all, delete-orphan")

class ClubSpecification(Base):
    """クラブスペックモデル"""
    __tablename__ = "club_specifications"
    
    id = Column(Integer, primary_key=True, index=True)
    club_model_id = Column(Integer, ForeignKey("club_models.id"), nullable=False)
    club_type = Column(String, nullable=False)  # driver, iron, etc.
    club_number = Column(String, nullable=False)  # 1W, 7i, etc.
    loft = Column(Float, nullable=False)
    lie_angle = Column(Float, nullable=True)
    length = Column(Float, nullable=True)
    head_weight = Column(Float, nullable=True)
    swing_weight = Column(String, nullable=True)
    shaft_id = Column(Integer, ForeignKey("shafts.id"), nullable=False)
    face_angle = Column(Float, nullable=True)
    offset = Column(Float, nullable=True)
    bounce_angle = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    
    club_model = relationship("ClubModel", back_populates="specifications")
    shaft = relationship("Shaft", back_populates="specifications")

class Shaft(Base):
    """シャフトモデル"""
    __tablename__ = "shafts"
    
    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    flex = Column(String, nullable=False)
    weight = Column(Float, nullable=False)
    torque = Column(Float, nullable=True)
    kick_point = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    
    specifications = relationship("ClubSpecification", back_populates="shaft") 