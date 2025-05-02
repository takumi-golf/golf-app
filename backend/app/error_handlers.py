from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError, NoResultFound
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class ErrorMessages:
    # データベースエラー
    DB_ERROR = "データベースエラーが発生しました"
    DUPLICATE_EMAIL = "このメールアドレスは既に登録されています"
    INVALID_DATA = "無効なデータが入力されました"
    DB_CONNECTION_ERROR = "データベースへの接続に失敗しました"
    DB_QUERY_ERROR = "データベースクエリの実行に失敗しました"
    
    # 認証エラー
    AUTHENTICATION_ERROR = "認証に失敗しました"
    INVALID_CREDENTIALS = "メールアドレスまたはパスワードが正しくありません"
    TOKEN_EXPIRED = "認証トークンの有効期限が切れています"
    INVALID_TOKEN = "無効な認証トークンです"
    
    # リソースエラー
    USER_NOT_FOUND = "ユーザーが見つかりません"
    RECOMMENDATION_NOT_FOUND = "レコメンデーションが見つかりません"
    CLUB_NOT_FOUND = "ゴルフクラブが見つかりません"
    RESOURCE_NOT_FOUND = "リソースが見つかりません"
    
    # バリデーションエラー
    VALIDATION_ERROR = "入力データが不正です"
    REQUIRED_FIELD = "必須項目が入力されていません"
    INVALID_EMAIL_FORMAT = "メールアドレスの形式が正しくありません"
    INVALID_PASSWORD_FORMAT = "パスワードは8文字以上必要です"
    INVALID_CLUB_DATA = "ゴルフクラブのデータが不正です"

def handle_http_exception(request: Request, exc: HTTPException) -> JSONResponse:
    """HTTP例外のハンドラー"""
    logger.error(f"HTTP Exception: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

def handle_integrity_error(request: Request, exc: IntegrityError) -> JSONResponse:
    """データベースの整合性エラーのハンドラー"""
    error_message = ErrorMessages.DB_ERROR
    error_detail = str(exc)
    
    if "unique constraint" in error_detail.lower():
        if "email" in error_detail.lower():
            error_message = ErrorMessages.DUPLICATE_EMAIL
        else:
            error_message = ErrorMessages.INVALID_DATA
    
    logger.error(f"Integrity Error: {error_detail}")
    return JSONResponse(
        status_code=400,
        content={"detail": error_message}
    )

def handle_sqlalchemy_error(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    """SQLAlchemyエラーのハンドラー"""
    error_message = ErrorMessages.DB_ERROR
    
    if isinstance(exc, NoResultFound):
        error_message = ErrorMessages.RESOURCE_NOT_FOUND
        status_code = 404
    else:
        status_code = 500
        logger.error(f"SQLAlchemy Error: {str(exc)}")
    
    return JSONResponse(
        status_code=status_code,
        content={"detail": error_message}
    )

def handle_validation_error(request: Request, exc: RequestValidationError) -> JSONResponse:
    """バリデーションエラーのハンドラー"""
    errors = exc.errors()
    error_messages = []
    
    for error in errors:
        field = error.get("loc", ["unknown"])[-1]
        msg = error.get("msg", "")
        
        if field == "email":
            error_messages.append(ErrorMessages.INVALID_EMAIL_FORMAT)
        elif field == "password":
            error_messages.append(ErrorMessages.INVALID_PASSWORD_FORMAT)
        elif "club" in str(field).lower():
            error_messages.append(ErrorMessages.INVALID_CLUB_DATA)
        else:
            error_messages.append(f"{field}: {msg}")
    
    logger.warning(f"Validation Error: {error_messages}")
    return JSONResponse(
        status_code=422,
        content={
            "detail": ErrorMessages.VALIDATION_ERROR,
            "errors": error_messages
        }
    ) 