from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    height: float = Field(..., gt=0, le=250, description="身長（cm）")
    weight: float = Field(..., gt=0, le=200, description="体重（kg）")
    age: int = Field(..., gt=0, le=120, description="年齢")
    gender: str = Field(..., description="性別")
    handicap: Optional[float] = Field(None, ge=0, le=54, description="ハンディキャップ")

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    height: Optional[float] = Field(None, gt=0, le=250, description="身長（cm）")
    weight: Optional[float] = Field(None, gt=0, le=200, description="体重（kg）")
    age: Optional[int] = Field(None, gt=0, le=120, description="年齢")
    gender: Optional[str] = Field(None, description="性別")
    handicap: Optional[float] = Field(None, ge=0, le=54, description="ハンディキャップ")

class UserPreferences(BaseModel):
    budget: float = Field(..., ge=0, description="予算（円）")
    preferred_shaft_flex: list[str] = Field(..., description="希望のシャフトフレックス")
    preferred_brands: Optional[list[str]] = Field(None, description="希望のブランド")
    preferred_club_types: Optional[list[str]] = Field(None, description="希望のクラブタイプ") 