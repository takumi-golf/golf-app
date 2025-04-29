from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    height: Optional[float] = None
    weight: Optional[float] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    handicap: Optional[float] = None
    average_score: Optional[int] = None
    head_speed: Optional[float] = None
    ball_speed: Optional[float] = None
    launch_angle: Optional[float] = None
    swing_issue: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    handicap: Optional[float] = None
    average_score: Optional[int] = None
    head_speed: Optional[float] = None
    ball_speed: Optional[float] = None
    launch_angle: Optional[float] = None
    swing_issue: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = None

class UserPreferences(BaseModel):
    budget: Optional[float] = Field(None, ge=0, description="予算（円）")
    preferred_brands: Optional[list[str]] = Field(None, description="好みのブランド")
    preferred_shaft_flex: Optional[str] = Field(None, description="好みのシャフトフレックス")
    preferred_club_types: Optional[list[str]] = Field(None, description="好みのクラブタイプ")
    swing_characteristics: Optional[Dict[str, Any]] = Field(None, description="スイング特性") 