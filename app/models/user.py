from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    height = Column(Float)
    weight = Column(Float)
    age = Column(Integer)
    gender = Column(String)
    handicap = Column(Float, nullable=True, index=True)
    average_score = Column(Integer, nullable=True, index=True)
    head_speed = Column(Float, nullable=True, index=True)
    ball_speed = Column(Float, nullable=True, index=True)
    launch_angle = Column(Float, nullable=True, index=True)
    swing_issue = Column(String, nullable=True, index=True)
    preferences = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), index=True)
    is_active = Column(Boolean, default=True, index=True) 