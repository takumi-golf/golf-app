from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from .database import Base

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    recommendation_id = Column(Integer, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    feedback = Column(Text, nullable=True)
    rating = Column(Integer, nullable=True) 