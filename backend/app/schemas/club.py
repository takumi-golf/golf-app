from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class BrandSchema(BaseModel):
    """ブランドのスキーマ"""
    id: Optional[int] = None
    name: str = Field(..., description="ブランド名")
    logo_path: Optional[str] = Field(None, description="ブランドロゴのパス")

    class Config:
        from_attributes = True

class BrandCreate(BrandSchema):
    """ブランド作成用スキーマ"""
    pass

class Brand(BrandSchema):
    """ブランドのレスポンススキーマ"""
    id: int

class ClubModelSchema(BaseModel):
    """クラブモデルのスキーマ"""
    id: Optional[int] = None
    name: str = Field(..., description="モデル名")
    brand_id: int = Field(..., description="ブランドID")
    release_year: int = Field(..., description="発売年")
    type: str = Field(..., description="クラブタイプ")
    category: str = Field(..., description="カテゴリ")

    class Config:
        from_attributes = True

class ClubModelCreate(ClubModelSchema):
    """クラブモデル作成用スキーマ"""
    pass

class ClubModel(ClubModelSchema):
    """クラブモデルのレスポンススキーマ"""
    id: int
    brand: Brand

class ClubSpecificationSchema(BaseModel):
    """クラブスペックのスキーマ"""
    id: Optional[int] = None
    club_type: str = Field(..., description="クラブタイプ")
    loft: float = Field(..., description="ロフト角")
    lie_angle: Optional[float] = Field(None, description="ライ角")
    length: Optional[float] = Field(None, description="長さ")
    head_weight: Optional[float] = Field(None, description="ヘッド重量")
    swing_weight: Optional[str] = Field(None, description="スイングウェイト")
    flex: Optional[str] = Field(None, description="シャフトフレックス")

    class Config:
        from_attributes = True

class ClubSpecificationCreate(ClubSpecificationSchema):
    """クラブスペック作成用スキーマ"""
    club_model_id: int = Field(..., description="クラブモデルID")

class ClubSpecification(ClubSpecificationSchema):
    """クラブスペックのレスポンススキーマ"""
    id: int
    club_model: ClubModel

class ShaftBase(BaseModel):
    brand: str = Field(..., description="シャフトのブランド名")
    model: str = Field(..., description="シャフトのモデル名")
    flex: str = Field(..., description="シャフトのフレックス")
    weight: float = Field(..., description="シャフトの重量（g）")
    torque: float = Field(..., description="シャフトのトルク")
    kick_point: str = Field(..., description="シャフトのキックポイント")
    description: Optional[str] = Field(None, description="シャフトの説明")

class ShaftCreate(ShaftBase):
    pass

class ShaftResponse(ShaftBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 