import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.main import app
from app.database import Base, get_db
from app import models
import uuid
import os

# テスト用のデータベースURL
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# テスト用のエンジンとセッションを作成
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    # テスト用のデータベースを作成
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            db.rollback()
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        Base.metadata.create_all(bind=engine)
        yield test_client
        Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def test_user(client, db):
    # テスト用のユーザーを作成
    unique_id = str(uuid.uuid4())[:8]
    user_data = {
        "email": f"test_{unique_id}@example.com",
        "password": "testpassword123"  # 8文字以上のパスワード
    }
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 201
    db.commit()  # 明示的にコミット
    return response.json()

@pytest.fixture(scope="function")
def test_recommendation(client, test_user, db):
    # テスト用のレコメンデーションを作成
    recommendation_data = {
        "user_id": test_user["id"],
        "club_name": "テストドライバー",
        "brand": "テストブランド",
        "loft": "10.5",
        "shaft": "テストシャフト",
        "flex": "S"
    }
    response = client.post("/api/v1/recommendations/", json=recommendation_data)
    assert response.status_code == 201
    db.commit()  # 明示的にコミット
    return response.json() 