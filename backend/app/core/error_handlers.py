from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from typing import Any, Callable, TypeVar, Optional
from functools import wraps
import logging

# ロガーの設定
logger = logging.getLogger(__name__)

# 型変数の定義
T = TypeVar('T')

class DatabaseError(Exception):
    """データベース関連のエラー"""
    def __init__(self, message: str, original_error: Optional[Exception] = None):
        self.message = message
        self.original_error = original_error
        super().__init__(self.message)

class ValidationError(Exception):
    """バリデーションエラー"""
    def __init__(self, message: str, field: Optional[str] = None):
        self.message = message
        self.field = field
        super().__init__(self.message)

def error_handler(func: Callable[..., T]) -> Callable[..., T]:
    """エラーハンドリング用のデコレータ"""
    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> T:
        try:
            return await func(*args, **kwargs)
        except DatabaseError as e:
            logger.error(f"Database error in {func.__name__}: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail={"message": "データベースエラーが発生しました", "error": str(e)}
            )
        except ValidationError as e:
            logger.error(f"Validation error in {func.__name__}: {str(e)}")
            raise HTTPException(
                status_code=400,
                detail={"message": e.message, "field": e.field}
            )
        except SQLAlchemyError as e:
            logger.error(f"SQLAlchemy error in {func.__name__}: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail={"message": "データベースエラーが発生しました", "error": str(e)}
            )
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail={"message": "予期せぬエラーが発生しました", "error": str(e)}
            )
    return wrapper

async def database_exception_handler(request: Request, exc: DatabaseError) -> JSONResponse:
    """データベースエラーのグローバルハンドラ"""
    return JSONResponse(
        status_code=500,
        content={
            "message": "データベースエラーが発生しました",
            "error": str(exc),
            "original_error": str(exc.original_error) if exc.original_error else None
        }
    )

async def validation_exception_handler(request: Request, exc: ValidationError) -> JSONResponse:
    """バリデーションエラーのグローバルハンドラ"""
    return JSONResponse(
        status_code=400,
        content={
            "message": exc.message,
            "field": exc.field
        }
    )

async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    """SQLAlchemyエラーのグローバルハンドラ"""
    return JSONResponse(
        status_code=500,
        content={
            "message": "データベースエラーが発生しました",
            "error": str(exc)
        }
    ) 