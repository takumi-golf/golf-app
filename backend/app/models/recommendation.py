from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..database.database import Base

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    total_price = Column(Integer)
    match_score = Column(Float)
    reason = Column(String)
    purchase_url = Column(String, nullable=True)

    # クラブとの関連付け
    clubs = relationship("Club", secondary="recommendation_clubs")

class RecommendationClub(Base):
    __tablename__ = "recommendation_clubs"

    recommendation_id = Column(Integer, ForeignKey("recommendations.id"), primary_key=True)
    club_id = Column(Integer, ForeignKey("clubs.id"), primary_key=True) 