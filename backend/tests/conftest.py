import pytest
import uuid
from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.main import app
from app.database import Base, get_db
from app import models
from app.models import User
from app.error_handlers import (
    http_exception_handler,
    validation_exception_handler,
    sqlalchemy_exception_handler
)

# テスト用のデータベースURL
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# テスト用のエンジンとセッションを作成
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    """テスト用のデータベースセッションを提供するフィクスチャ"""
    # テスト用のデータベースを作成
    Base.metadata.create_all(bind=engine)
    
    # テストセッションを作成
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # テストデータベースをクリーンアップ
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db):
    """テストクライアントを提供するフィクスチャ"""
    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    
    # エラーハンドラーを登録
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    
    with TestClient(app) as client:
        yield client

@pytest.fixture(scope="function")
def test_user(client):
    """テスト用のユーザーを作成するフィクスチャ"""
    user_data = {
        "email": f"test_{uuid.uuid4().hex[:8]}@example.com",
        "password": "testpassword123"
    }
    response = client.post("/api/v1/users/", json=user_data)
    return response.json()

@pytest.fixture(scope="function")
def test_brand(client, db):
    # テスト用のブランドを作成
    brand_data = {
        "name": "Test Brand",
        "logo_path": "/images/brands/test.png"
    }
    response = client.post("/api/clubs/brands/", json=brand_data)
    assert response.status_code == 200
    db.commit()
    return response.json()

@pytest.fixture(scope="function")
def test_club_model(client, test_brand, db):
    # テスト用のクラブモデルを作成
    model_data = {
        "name": "Test Model",
        "brand_id": test_brand["id"],
        "release_year": 2024,
        "type": "driver",
        "category": "player"
    }
    response = client.post("/api/clubs/models/", json=model_data)
    assert response.status_code == 200
    db.commit()
    return response.json()

@pytest.fixture(scope="function")
def test_shaft(client, db):
    # テスト用のシャフトを作成
    shaft_data = {
        "brand": "Test Shaft",
        "model": "Test Model",
        "flex": "S",
        "weight": 65.0,
        "torque": 4.2,
        "kick_point": "mid",
        "description": "Test shaft"
    }
    response = client.post("/api/clubs/shafts/", json=shaft_data)
    assert response.status_code == 200
    db.commit()
    return response.json()

@pytest.fixture(scope="function")
def test_club_specification(client, test_club_model, test_shaft, db):
    # テスト用のクラブスペックを作成
    spec_data = {
        "club_model_id": test_club_model["id"],
        "club_type": "driver",
        "loft": 10.5,
        "lie_angle": 58.0,
        "length": 45.5,
        "head_weight": 198.0,
        "swing_weight": "D2",
        "flex": "S"
    }
    response = client.post("/api/clubs/specifications/", json=spec_data)
    assert response.status_code == 200
    db.commit()
    return response.json()

@pytest.fixture(scope="function")
def test_player_profile(client, db):
    # テスト用のプレイヤープロファイルを作成
    profile_data = {
        "head_speed": 40.0,
        "handicap": 15.0,
        "age": 35,
        "gender": "male"
    }
    response = client.post("/api/v1/recommendations/", json=profile_data)
    assert response.status_code == 201
    db.commit()
    return response.json() 