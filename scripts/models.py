from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Boolean
from datetime import datetime
from .init_db import Base

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