from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError, NoResultFound
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class ValidationError(Exception):
    """バリデーションエラーの基底クラス"""
    pass

class HeadSpeedError(ValidationError):
    """ヘッドスピードに関するエラー"""
    pass

class HandicapError(ValidationError):
    """ハンディキャップに関するエラー"""
    pass

class AgeError(ValidationError):
    """年齢に関するエラー"""
    pass

class GenderError(ValidationError):
    """性別に関するエラー"""
    pass

class ErrorMessages:
    """エラーメッセージの定義"""
    INVALID_EMAIL_FORMAT = "メールアドレスの形式が正しくありません"
    INVALID_PASSWORD_FORMAT = "パスワードは8文字以上である必要があります"
    INVALID_CLUB_DATA = "クラブデータの形式が正しくありません"
    USER_NOT_FOUND = "ユーザーが見つかりません"
    RECOMMENDATION_NOT_FOUND = "レコメンデーションが見つかりません"
    RECOMMENDATION_CREATION_ERROR = "レコメンデーションの生成に失敗しました"
    DATABASE_ERROR = "データベースエラーが発生しました"
    DUPLICATE_EMAIL = "このメールアドレスは既に登録されています"
    INVALID_DATA = "無効なデータが入力されました"
    DB_CONNECTION_ERROR = "データベースへの接続に失敗しました"
    DB_QUERY_ERROR = "データベースクエリの実行に失敗しました"
    AUTHENTICATION_ERROR = "認証に失敗しました"
    INVALID_CREDENTIALS = "メールアドレスまたはパスワードが正しくありません"
    TOKEN_EXPIRED = "認証トークンの有効期限が切れています"
    INVALID_TOKEN = "無効な認証トークンです"
    EMAIL_ALREADY_EXISTS = "このメールアドレスは既に登録されています"
    INVALID_RECOMMENDATION_DATA = "レコメンデーションデータが無効です"
    HEAD_SPEED_INVALID = "ヘッドスピードは0より大きく、80.0以下の値を指定してください"
    HANDICAP_INVALID = "ハンディキャップは0以上、54.0以下の値を指定してください"
    AGE_INVALID = "年齢は0より大きく、120以下の値を指定してください"
    GENDER_INVALID = "性別は'male'または'female'を指定してください"

def create_error_response(status_code: int, message: str, errors: list = None) -> JSONResponse:
    """統一されたエラーレスポンスを作成"""
    content = {"detail": message}
    if errors:
        content["errors"] = errors
    return JSONResponse(status_code=status_code, content=content)

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """バリデーションエラーのハンドラー"""
    logger.warning(f"Validation Error: {exc.errors()}")
    errors = []
    for error in exc.errors():
        error_msg = {
            "field": ".".join(str(loc) for loc in error["loc"]),
            "message": error["msg"]
        }
        errors.append(error_msg)
    return create_error_response(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        message=ErrorMessages.INVALID_DATA,
        errors=errors
    )

async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """データベースエラーのハンドラー"""
    logger.error(f"Database Error: {str(exc)}")
    return create_error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message=ErrorMessages.DATABASE_ERROR
    )

async def http_exception_handler(request: Request, exc: HTTPException):
    """HTTPエラーのハンドラー"""
    logger.error(f"HTTPException: {exc.detail}")
    return create_error_response(
        status_code=exc.status_code,
        message=exc.detail
    )

def handle_integrity_error(request: Request, exc: IntegrityError) -> JSONResponse:
    """データベースの整合性エラーのハンドラー"""
    error_message = ErrorMessages.DATABASE_ERROR
    error_detail = str(exc)
    
    if "unique constraint" in error_detail.lower():
        if "email" in error_detail.lower():
            error_message = ErrorMessages.DUPLICATE_EMAIL
        else:
            error_message = ErrorMessages.INVALID_DATA
    
    logger.error(f"Integrity Error: {error_detail}")
    return create_error_response(
        status_code=status.HTTP_400_BAD_REQUEST,
        message=error_message
    )

def handle_sqlalchemy_error(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    """SQLAlchemyエラーのハンドラー"""
    error_message = ErrorMessages.DATABASE_ERROR
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    
    if isinstance(exc, NoResultFound):
        error_message = ErrorMessages.RESOURCE_NOT_FOUND
        status_code = status.HTTP_404_NOT_FOUND
    
    logger.error(f"SQLAlchemy Error: {str(exc)}")
    return create_error_response(
        status_code=status_code,
        message=error_message
    ) 