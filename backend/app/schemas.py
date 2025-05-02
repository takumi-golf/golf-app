from pydantic import BaseModel, ConfigDict, constr
from typing import List, Optional
from datetime import datetime

class MatchDetails(BaseModel):
    flex_match: float
    physique_match: float
    budget_match: float

class RecommendationResponse(BaseModel):
    brand: str
    model: str
    confidence_score: float
    match_details: MatchDetails
    features: str
    price: int

    model_config = ConfigDict(from_attributes=True)

class RecommendationList(BaseModel):
    recommendations: List[RecommendationResponse]
    total: int

class RecommendationHistory(BaseModel):
    id: int
    recommendation_id: int
    created_at: datetime
    feedback: Optional[str] = None
    rating: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

class Feedback(BaseModel):
    recommendation_id: int
    feedback: str
    rating: int

    model_config = ConfigDict(from_attributes=True)

class RecommendationRequest(BaseModel):
    height: float
    weight: float
    age: int
    gender: str
    handicap: int

    model_config = ConfigDict(from_attributes=True) 