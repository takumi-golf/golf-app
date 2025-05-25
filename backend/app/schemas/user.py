from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """ユーザーの基本スキーマ"""
    email: EmailStr = Field(..., description="メールアドレス")

class UserCreate(UserBase):
    """ユーザー作成用スキーマ"""
    password: str = Field(..., min_length=8, description="パスワード（8文字以上）")

class User(UserBase):
    """ユーザーのレスポンススキーマ"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    """認証トークンのスキーマ"""
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """トークンデータのスキーマ"""
    email: Optional[str] = None
    expires: Optional[datetime] = None 