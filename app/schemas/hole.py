from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class GolfHoleBase(BaseModel):
    hole_number: int
    par: int
    score: Optional[int] = None
    fairway_hit: Optional[bool] = None
    green_in_regulation: Optional[bool] = None
    putts: Optional[int] = None

class GolfHoleCreate(GolfHoleBase):
    round_id: int
    course_id: int

class GolfHole(GolfHoleBase):
    id: int
    round_id: int
    course_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 