from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class ClubBase(BaseModel):
    club_id: str
    brand: str
    model: str
    type: str
    loft: float
    shaft: str
    shaft_flex: str
    price: int
    features: Dict[str, Any]
    specifications: Dict[str, Any]

class ClubCreate(ClubBase):
    pass

class ClubUpdate(ClubBase):
    club_id: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    type: Optional[str] = None
    loft: Optional[float] = None
    shaft: Optional[str] = None
    shaft_flex: Optional[str] = None
    price: Optional[int] = None
    features: Optional[Dict[str, Any]] = None
    specifications: Optional[Dict[str, Any]] = None

class ClubResponse(ClubBase):
    id: int
    popularity_score: float
    created_at: datetime
    updated_at: datetime
    is_available: bool

    class Config:
        from_attributes = True

class ClubSearch(BaseModel):
    type: Optional[str] = None
    brand: Optional[str] = None
    min_price: Optional[int] = None
    max_price: Optional[int] = None
    features: Optional[List[str]] = None
    swing_speed: Optional[float] = None
    spin_preference: Optional[str] = None
    forgiveness_preference: Optional[str] = None

class ClubSearchResponse(BaseModel):
    clubs: List[ClubResponse]
    total_count: int
    page: int
    per_page: int

class ClubRecommendation(BaseModel):
    club: ClubResponse
    score: float
    match_reasons: List[str] 