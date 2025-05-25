import pytest
from fastapi import status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.error_handlers import ErrorMessages
from app import models

def test_duplicate_email_error(client, db):
    """重複メールアドレスでのユーザー登録エラーをテスト"""
    # データベースをクリーンな状態にする
    db.query(models.User).delete()
    db.commit()

    # 最初のユーザー登録
    user_data = {
        "email": "duplicate@example.com",
        "password": "testpassword123"
    }
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == status.HTTP_201_CREATED
    db.commit()

    # 同じメールアドレスでの登録
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == ErrorMessages.DUPLICATE_EMAIL

def test_invalid_email_format(client):
    """無効なメールアドレス形式のエラーをテスト"""
    invalid_user_data = {
        "email": "invalid-email",
        "password": "testpassword123"
    }
    response = client.post("/api/v1/users/", json=invalid_user_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    data = response.json()
    assert "detail" in data
    assert "errors" in data
    assert any(error["field"] == "body.email" for error in data["errors"])

def test_invalid_password_format(client):
    """無効なパスワード形式のエラーをテスト"""
    invalid_user_data = {
        "email": "test@example.com",
        "password": "short"  # 8文字未満
    }
    response = client.post("/api/v1/users/", json=invalid_user_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    data = response.json()
    assert "detail" in data
    assert "errors" in data
    assert any(error["field"] == "body.password" for error in data["errors"])

def test_user_not_found_error(client):
    """存在しないユーザーIDでのエラーをテスト"""
    response = client.get("/api/v1/users/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == ErrorMessages.USER_NOT_FOUND

def test_recommendation_not_found_error(client, test_user, db):
    """存在しないレコメンデーションIDでのエラーをテスト"""
    db.query(models.Recommendation).delete()
    db.commit()

    response = client.get("/api/v1/recommendations/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == ErrorMessages.RECOMMENDATION_NOT_FOUND

def test_invalid_recommendation_data_error(client, test_user):
    """無効なレコメンデーションデータでのエラーをテスト"""
    invalid_data = {
        "head_speed": -1.0,  # 無効な値
        "handicap": 100.0,  # 無効な値
        "age": 0,  # 無効な値
        "gender": "invalid"  # 無効な値
    }
    response = client.post("/api/v1/recommendations/", json=invalid_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    data = response.json()
    assert "detail" in data
    assert "errors" in data
    assert len(data["errors"]) > 0

def test_database_error_handling(client, test_user, monkeypatch):
    """データベースエラーのハンドリングをテスト"""
    def mock_db_error(*args, **kwargs):
        raise SQLAlchemyError("テスト用のデータベースエラー")

    monkeypatch.setattr("sqlalchemy.orm.Session.query", mock_db_error)

    response = client.get(f"/api/v1/users/{test_user['id']}")
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json()["detail"] == ErrorMessages.DATABASE_ERROR

def test_validation_error_details(client):
    """バリデーションエラーの詳細情報をテスト"""
    invalid_data = {
        "email": "invalid-email",
        "password": "short",
        "club_name": ""
    }
    response = client.post("/api/v1/users/", json=invalid_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    data = response.json()
    assert "detail" in data
    assert "errors" in data
    assert all("field" in error and "message" in error for error in data["errors"]) 