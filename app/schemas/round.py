from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .hole import GolfHole

class GolfRoundBase(BaseModel):
    course_id: int
    date: datetime
    total_score: int
    weather: str
    temperature: int

class GolfRoundCreate(GolfRoundBase):
    user_id: int

class GolfRound(GolfRoundBase):
    id: int
    user_id: int
    holes: List[GolfHole]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 