from pydantic import BaseModel
from typing import List, Optional
from .club import Club

class RecommendationBase(BaseModel):
    name: str
    description: str
    total_price: int
    match_score: float
    reason: str
    purchase_url: Optional[str] = None

class RecommendationCreate(RecommendationBase):
    clubs: List[Club]

class RecommendationUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    total_price: Optional[int] = None
    match_score: Optional[float] = None
    reason: Optional[str] = None
    purchase_url: Optional[str] = None
    clubs: Optional[List[Club]] = None

class Recommendation(RecommendationBase):
    id: int
    clubs: List[Club]

    class Config:
        from_attributes = True 