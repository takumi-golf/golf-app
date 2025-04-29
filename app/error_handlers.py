from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from jose.exceptions import JWTError
import logging
from typing import Callable, Any, Dict, Optional
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

class ErrorResponse:
    def __init__(self, error_code: int, message: str, details: Optional[Any] = None):
        self.error_code = error_code
        self.message = message
        self.details = details

    def to_dict(self) -> Dict[str, Any]:
        return {
            "error_code": self.error_code,
            "message": self.message,
            "details": self.details
        }

    async def __call__(self, scope, receive, send):
        response = JSONResponse(
            status_code=self.error_code,
            content=self.to_dict()
        )
        await response(scope, receive, send)

def handle_database_errors(func: Callable) -> Callable:
    """データベースエラーのハンドリングデコレータ"""
    @functools.wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        try:
            return await func(*args, **kwargs)
        except SQLAlchemyError as e:
            logging.error(f"Database error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="データベースエラーが発生しました"
            )
    return wrapper

def handle_validation_errors(func: Callable) -> Callable:
    """バリデーションエラーのハンドリングデコレータ"""
    @functools.wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        try:
            return await func(*args, **kwargs)
        except ValueError as e:
            logging.error(f"Validation error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
    return wrapper

def handle_authentication_errors(func: Callable) -> Callable:
    """認証エラーのハンドリングデコレータ"""
    @functools.wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        try:
            return await func(*args, **kwargs)
        except (HTTPException, JWTError) as e:
            if isinstance(e, HTTPException):
                raise e
            logging.error(f"Authentication error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="認証に失敗しました"
            )
    return wrapper

async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """グローバル例外ハンドラ"""
    logging.error(f"Global error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "予期せぬエラーが発生しました"}
    ) 