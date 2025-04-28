

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    height: float
    weight: float
    age: int
    gender: str
    handicap: Optional[float] = None
    average_score: Optional[int] = None
    head_speed: Optional[float] = None
    ball_speed: Optional[float] = None
    launch_angle: Optional[float] = None
    swing_issue: Optional[str] = None

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class ClubBase(BaseModel):
    type: str
    brand: str
    model: str
    loft: Optional[float] = None
    shaft: Optional[str] = None
    shaft_flex: Optional[str] = None
    price: int
    features: str

class ClubCreate(ClubBase):
    pass

class Club(ClubBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class RecommendationBase(BaseModel):
    user_id: int
    total_price: int

class RecommendationCreate(RecommendationBase):
    pass

class Recommendation(RecommendationBase):
    id: int
    created_at: datetime
    clubs: List[Club] = []

    class Config:
        orm_mode = True 