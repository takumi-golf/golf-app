from fastapi import APIRouter
from .endpoints import recommendations

api_router = APIRouter()
api_router.include_router(recommendations.router, prefix="/recommendations", tags=["recommendations"]) 