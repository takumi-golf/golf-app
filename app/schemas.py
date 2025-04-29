from pydantic import BaseModel, Field, validator, confloat, conint
from typing import List, Optional, Dict, Any
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: str
    full_name: str
    height: float
    weight: float
    age: int
    gender: str
    handicap: Optional[float] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    handicap: Optional[float] = None

class UserPreferences(BaseModel):
    budget: float
    preferred_shaft_flex: List[str]
    preferred_brand: Optional[str] = None
    preferred_type: Optional[str] = None

class ClubSearch(BaseModel):
    brand: Optional[str] = None
    model: Optional[str] = None
    type: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    shaft_flex: Optional[str] = None

class ClubDetails(BaseModel):
    brand: str
    model: str
    loft: float
    shaft: str
    shaft_flex: str
    price: int
    features: str
    trajectory: str
    spin: str
    forgiveness: str
    shaft_details: Dict[str, str]
    price_category: str
    average_rating: float
    review_count: int
    reviews: List[Dict[str, Any]]

class ClubRecommendation(BaseModel):
    driver: Optional[ClubDetails]
    woods: List[ClubDetails]
    utilities: List[ClubDetails]
    irons: List[ClubDetails]
    wedges: List[ClubDetails]
    putter: Optional[ClubDetails]
    total_price: float
    confidence_score: float
    timestamp: datetime

class ClubSearchResponse(BaseModel):
    clubs: List[ClubRecommendation]

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class ErrorResponse(BaseModel):
    error: str
    message: str
    debug_info: Optional[str] = None

class ProductBase(BaseModel):
    brand: str
    model: str
    category: str
    type: str
    description: Optional[str] = None
    specifications: Dict[str, str] = {}
    features: List[str] = []
    url: str
    release_date: Optional[datetime] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    description: Optional[str] = None
    specifications: Optional[Dict[str, str]] = None
    features: Optional[List[str]] = None
    url: Optional[str] = None
    release_date: Optional[datetime] = None

class Product(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class PriceHistoryBase(BaseModel):
    product_id: int
    price: int
    currency: str = "JPY"
    source: str
    is_tax_included: bool = True

class PriceHistoryCreate(PriceHistoryBase):
    pass

class PriceHistory(PriceHistoryBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class ProductWithPrice(Product):
    current_price: Optional[PriceHistory] = None
    price_history: List[PriceHistory] = []

    class Config:
        orm_mode = True 