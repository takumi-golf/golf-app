from pydantic import BaseModel, ConfigDict, constr, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class MatchDetails(BaseModel):
    flex_match: float
    physique_match: float
    budget_match: float

class RecommendationRequest(BaseModel):
    head_speed: float = Field(..., description="ヘッドスピード（m/s）")
    handicap: float = Field(..., description="ハンディキャップ")
    age: int = Field(..., description="年齢")
    gender: str = Field(..., description="性別（male/female）")
    user_id: Optional[int] = Field(None, description="ユーザーID（協調フィルタリング用）")
    use_collaborative_filtering: bool = Field(False, description="協調フィルタリングを使用するか")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "head_speed": 40.0,
                    "handicap": 12.0,
                    "age": 45,
                    "gender": "male",
                    "user_id": None,
                    "use_collaborative_filtering": False
                }
            ]
        }
    }

class RecommendationResponse(BaseModel):
    segment: str
    shaft_recommendation: Dict[str, Any]
    recommended_clubs: List[RecommendedClub]

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

class ClubSpecificationResponse(BaseModel):
    brand: str
    model: str
    club_type: str
    club_number: str
    loft: float
    lie_angle: Optional[float] = None
    length: float
    shaft_brand: str
    shaft_model: str
    shaft_flex: str
    shaft_weight: float
    
    class Config:
        orm_mode = True

class RecommendedClub(BaseModel):
    type: str
    specifications: List[ClubSpecificationResponse]

class BrandBase(BaseModel):
    name: str
    logo_path: str

class BrandCreate(BrandBase):
    pass

class Brand(BrandBase):
    id: int
    
    class Config:
        orm_mode = True

class ClubModelBase(BaseModel):
    name: str
    brand_id: int
    release_year: int
    type: str
    category: str

class ClubModelCreate(ClubModelBase):
    pass

class ClubModel(ClubModelBase):
    id: int
    
    class Config:
        orm_mode = True

class ShaftBase(BaseModel):
    brand: str
    model: str
    flex: str
    weight: float
    material: str
    launch_characteristics: str
    spin_characteristics: str

class ShaftCreate(ShaftBase):
    pass

class Shaft(ShaftBase):
    id: int
    
    class Config:
        orm_mode = True 