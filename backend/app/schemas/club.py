from pydantic import BaseModel
from typing import Optional

class ClubBase(BaseModel):
    name: str
    type: str
    loft: float
    length: float
    flex: str
    weight: float
    brand: str
    price: int
    description: str
    image_url: Optional[str] = None

class ClubCreate(ClubBase):
    pass

class Club(ClubBase):
    id: int

    class Config:
        from_attributes = True 