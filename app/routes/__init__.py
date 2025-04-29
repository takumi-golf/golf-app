from .users import router as users_router
from .auth import router as auth_router
from .clubs import router as clubs_router
from .recommendations import router as recommendations_router

__all__ = [
    "users_router",
    "auth_router",
    "clubs_router",
    "recommendations_router"
]
