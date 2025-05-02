from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from app.main import app
from app.database import Base, get_db
from app import models, schemas

# テスト用のデータベースURL
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/golf_recommendation_test"

# テスト用のエンジンとセッションを作成
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# テスト用のデータベースセッションを提供する関数
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# テスト用のデータベースセッションを設定
app.dependency_overrides[get_db] = override_get_db

# テストクライアントの作成
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    # テスト用のデータベースを作成
    Base.metadata.create_all(bind=engine)
    yield
    # テスト後にデータベースを削除
    Base.metadata.drop_all(bind=engine)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "ゴルフクラブレコメンデーションAPIへようこそ"}

def test_create_user():
    response = client.post(
        "/api/v1/users/",
        json={"email": "test@example.com", "password": "testpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_read_users():
    # ユーザーを作成
    client.post(
        "/api/v1/users/",
        json={"email": "test@example.com", "password": "testpassword"}
    )
    
    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["email"] == "test@example.com"

def test_read_user():
    # ユーザーを作成
    response = client.post(
        "/api/v1/users/",
        json={"email": "test@example.com", "password": "testpassword"}
    )
    user_id = response.json()["id"]
    
    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["id"] == user_id

def test_create_recommendation():
    # ユーザーを作成
    response = client.post(
        "/api/v1/users/",
        json={"email": "test@example.com", "password": "testpassword"}
    )
    user_id = response.json()["id"]
    
    # レコメンデーションを作成
    recommendation_data = {
        "user_id": user_id,
        "club_type": "ドライバー",
        "club_name": "テストドライバー",
        "club_brand": "テストブランド",
        "club_model": "テストモデル",
        "club_loft": "10.5",
        "club_flex": "S",
        "club_length": "45.5",
        "club_lie": "58",
        "club_swing_weight": "D2",
        "club_shaft": "テストシャフト",
        "club_grip": "テストグリップ",
        "club_price": "50000",
        "club_image_url": "http://example.com/image.jpg",
        "club_description": "テスト用ドライバー",
        "club_features": {"feature1": "value1"},
        "club_specs": {"spec1": "value1"}
    }
    
    response = client.post("/api/v1/recommendations/", json=recommendation_data)
    assert response.status_code == 200
    data = response.json()
    assert data["club_type"] == "ドライバー"
    assert data["user_id"] == user_id

def test_read_recommendations():
    # ユーザーを作成
    response = client.post(
        "/api/v1/users/",
        json={"email": "test@example.com", "password": "testpassword"}
    )
    user_id = response.json()["id"]
    
    # レコメンデーションを作成
    recommendation_data = {
        "user_id": user_id,
        "club_type": "ドライバー",
        "club_name": "テストドライバー",
        "club_brand": "テストブランド",
        "club_model": "テストモデル",
        "club_loft": "10.5",
        "club_flex": "S",
        "club_length": "45.5",
        "club_lie": "58",
        "club_swing_weight": "D2",
        "club_shaft": "テストシャフト",
        "club_grip": "テストグリップ",
        "club_price": "50000",
        "club_image_url": "http://example.com/image.jpg",
        "club_description": "テスト用ドライバー",
        "club_features": {"feature1": "value1"},
        "club_specs": {"spec1": "value1"}
    }
    
    client.post("/api/v1/recommendations/", json=recommendation_data)
    
    response = client.get("/api/v1/recommendations/")
    assert response.status_code == 200
    data = response.json()
    assert "recommendations" in data
    assert "total" in data
    assert len(data["recommendations"]) > 0
    assert data["recommendations"][0]["club_type"] == "ドライバー"

def test_read_recommendation():
    # ユーザーを作成
    response = client.post(
        "/api/v1/users/",
        json={"email": "test@example.com", "password": "testpassword"}
    )
    user_id = response.json()["id"]
    
    # レコメンデーションを作成
    recommendation_data = {
        "user_id": user_id,
        "club_type": "ドライバー",
        "club_name": "テストドライバー",
        "club_brand": "テストブランド",
        "club_model": "テストモデル",
        "club_loft": "10.5",
        "club_flex": "S",
        "club_length": "45.5",
        "club_lie": "58",
        "club_swing_weight": "D2",
        "club_shaft": "テストシャフト",
        "club_grip": "テストグリップ",
        "club_price": "50000",
        "club_image_url": "http://example.com/image.jpg",
        "club_description": "テスト用ドライバー",
        "club_features": {"feature1": "value1"},
        "club_specs": {"spec1": "value1"}
    }
    
    response = client.post("/api/v1/recommendations/", json=recommendation_data)
    recommendation_id = response.json()["id"]
    
    response = client.get(f"/api/v1/recommendations/{recommendation_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["club_type"] == "ドライバー"
    assert data["id"] == recommendation_id 