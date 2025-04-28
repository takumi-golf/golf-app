from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
import logging
from typing import Callable, Any
import functools

# ログ設定
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('error.log'),
        logging.StreamHandler()
    ]
)

class DatabaseError(Exception):
    """データベース関連のエラー"""
    pass

class ValidationError(Exception):
    """バリデーションエラー"""
    pass

class AuthenticationError(Exception):
    """認証エラー"""
    pass

def handle_database_errors(func: Callable) -> Callable:
    """データベースエラーのハンドリングデコレータ"""
    @functools.wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        try:
            return await func(*args, **kwargs)
        except SQLAlchemyError as e:
            logging.error(f"Database error: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="データベースエラーが発生しました。しばらくしてから再度お試しください。"
            )
    return wrapper

def handle_validation_errors(func: Callable) -> Callable:
    """バリデーションエラーのハンドリングデコレータ"""
    @functools.wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        try:
            return await func(*args, **kwargs)
        except ValidationError as e:
            logging.warning(f"Validation error: {str(e)}")
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )
    return wrapper

def handle_authentication_errors(func: Callable) -> Callable:
    """認証エラーのハンドリングデコレータ"""
    @functools.wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        try:
            return await func(*args, **kwargs)
        except AuthenticationError as e:
            logging.warning(f"Authentication error: {str(e)}")
            raise HTTPException(
                status_code=401,
                detail=str(e)
            )
    return wrapper

async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """グローバル例外ハンドラ"""
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )
    
    logging.error(f"Unexpected error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "予期せぬエラーが発生しました。しばらくしてから再度お試しください。"}
    ) 