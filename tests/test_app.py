import pytest
from fastapi.testclient import TestClient
import sys
import os
from datetime import datetime
from sqlalchemy.orm import Session

# プロジェクトのルートディレクトリをPythonパスに追加
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from app import app
from app.database import (
    Base,
    User,
    Club,
    GolfCourse,
    GolfRound,
    GolfHole,
    engine,
    SessionLocal
)
from app.schemas import UserCreate, GolfCourseCreate, GolfRoundCreate, GolfHoleCreate

# テスト環境の設定
os.environ["TESTING"] = "1"
os.environ["JWT_SECRET_KEY"] = "test_secret_key"
os.environ["JWT_ALGORITHM"] = "HS256"
os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "30"

# テストクライアントの作成
client = TestClient(app)

@pytest.fixture
def db():
    """テスト用データベースセッション"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(autouse=True)
def setup_database():
    """テストデータベースのセットアップ"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def get_auth_headers(db: Session):
    """認証ヘッダーを取得する"""
    # ユーザーを作成
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword",
        "full_name": "Test User",
        "height": 170.0,
        "weight": 70.0,
        "age": 30,
        "gender": "male",
        "handicap": 10.5
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200

    # ログインしてトークンを取得
    login_data = {
        "username": "testuser",
        "password": "testpassword"
    }
    login_response = client.post("/token", data=login_data)
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_create_user():
    """ユーザー作成のテスト"""
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword",
        "full_name": "Test User",
        "height": 170.0,
        "weight": 70.0,
        "age": 30,
        "gender": "male",
        "handicap": 10.5
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == user_data["username"]
    assert data["email"] == user_data["email"]
    assert "id" in data

def test_create_club(client):
    club_data = {
        "brand": "テストブランド",
        "model": "テストモデル",
        "type": "driver",
        "loft": 10.5,
        "shaft": "テストシャフト",
        "shaft_flex": "R",
        "price": 50000,
        "features": "テスト機能",
        "specifications": {"length": "45.5", "weight": "300"},
        "popularity_score": 80.0,
        "is_available": True
    }
    response = client.post("/clubs/", json=club_data)
    print(f"Response status code: {response.status_code}")
    print(f"Response body: {response.json()}")
    assert response.status_code == 200
    data = response.json()
    assert data["brand"] == club_data["brand"]
    assert data["model"] == club_data["model"]
    assert data["type"] == club_data["type"]
    assert data["loft"] == club_data["loft"]
    assert data["shaft"] == club_data["shaft"]
    assert data["shaft_flex"] == club_data["shaft_flex"]
    assert data["price"] == club_data["price"]
    assert data["features"] == club_data["features"]
    assert data["specifications"] == club_data["specifications"]
    assert data["popularity_score"] == club_data["popularity_score"]
    assert data["is_available"] == club_data["is_available"]
    return data["id"]

def test_create_golf_course(client):
    course_data = {
        "name": "テストゴルフコース",
        "location": "東京都",
        "par": 72,
        "rating": 72.0,
        "slope": 120,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    response = client.post("/courses/", json=course_data)
    print(f"Response status code: {response.status_code}")
    print(f"Response body: {response.json()}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == course_data["name"]
    assert data["location"] == course_data["location"]
    assert data["par"] == course_data["par"]
    assert data["rating"] == course_data["rating"]
    assert data["slope"] == course_data["slope"]
    return data["id"]

def test_create_golf_round(client):
    round_data = {
        "user_id": 1,
        "course_id": 1,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "total_score": 85,
        "weather": "晴れ",
        "temperature": 25,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    response = client.post("/rounds/", json=round_data)
    print(f"Response status code: {response.status_code}")
    print(f"Response body: {response.json()}")
    assert response.status_code == 200
    data = response.json()
    assert data["course_id"] == round_data["course_id"]
    assert data["total_score"] == round_data["total_score"]

def test_create_golf_hole(client):
    hole_data = {
        "round_id": 1,
        "course_id": 1,
        "hole_number": 1,
        "par": 4,
        "score": 5,
        "fairway_hit": True,
        "green_in_regulation": False,
        "putts": 2,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    response = client.post("/holes/", json=hole_data)
    print(f"Response status code: {response.status_code}")
    print(f"Response body: {response.json()}")
    assert response.status_code == 200
    data = response.json()
    assert data["round_id"] == hole_data["round_id"]
    assert data["course_id"] == hole_data["course_id"]
    assert data["hole_number"] == hole_data["hole_number"]
    assert data["par"] == hole_data["par"]
    assert data["score"] == hole_data["score"]
    assert data["fairway_hit"] == hole_data["fairway_hit"]
    assert data["green_in_regulation"] == hole_data["green_in_regulation"]
    assert data["putts"] == hole_data["putts"]

def test_create_golf_course_invalid_par(db: Session):
    """無効なパー値でのゴルフコース作成のテスト"""
    headers = get_auth_headers(db)
    course_data = {
        "name": "Test Course",
        "location": "Tokyo",
        "par": 0,  # 無効なパー値
        "rating": 72.0,
        "slope": 113
    }
    response = client.post("/courses/", json=course_data, headers=headers)
    assert response.status_code == 422
    error_detail = response.json()["detail"]
    assert any("par" in error["loc"] for error in error_detail)

def test_create_golf_round_invalid_date(db: Session):
    """無効な日付でのゴルフラウンド作成のテスト"""
    headers = get_auth_headers(db)
    course_id = test_create_golf_course(client)
    
    # ユーザーIDを取得
    user_response = client.get("/users/me", headers=headers)
    assert user_response.status_code == 200
    user_id = user_response.json()["id"]
    
    round_data = {
        "user_id": user_id,
        "course_id": course_id,
        "date": "invalid-date",
        "total_score": 80,
        "weather": "Sunny",
        "temperature": 25.0,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    response = client.post("/rounds/", json=round_data, headers=headers)
    assert response.status_code == 422
    error_detail = response.json()["detail"]
    assert any("date" in error["loc"] for error in error_detail)

def test_create_golf_hole_invalid_hole_number(client):
    round_id = test_create_golf_round(client)
    course_id = test_create_golf_course(client)
    
    hole_data = {
        "round_id": round_id,
        "course_id": course_id,
        "hole_number": 0,
        "par": 4,
        "score": 4,
        "fairway_hit": True,
        "green_in_regulation": True,
        "putts": 2,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    response = client.post("/holes/", json=hole_data)
    print(f"Response status code: {response.status_code}")
    print(f"Response body: {response.json()}")
    assert response.status_code == 422
    error_detail = response.json()["detail"]
    assert any("hole_number" in error["loc"] for error in error_detail)

def test_get_current_user(client):
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "full_name": "Test User",
        "height": 170.0,
        "weight": 70.0,
        "age": 30,
        "gender": "male",
        "handicap": 10.5
    }
    response = client.post("/users/", json=user_data)
    print(f"Response status code: {response.status_code}")
    print(f"Response body: {response.json()}")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == user_data["username"]
    assert data["email"] == user_data["email"]
    assert data["full_name"] == user_data["full_name"]
    assert data["height"] == user_data["height"]
    assert data["weight"] == user_data["weight"]
    assert data["age"] == user_data["age"]
    assert data["gender"] == user_data["gender"]
    assert data["handicap"] == user_data["handicap"]
    return data["id"]

def test_get_current_user_invalid_token(client):
    response = client.get(
        "/users/me",
        headers={"Authorization": "Bearer invalid_token"}
    )
    print(f"Response status code: {response.status_code}")
    print(f"Response body: {response.json()}")
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"

def test_database_error_handling(client):
    # 無効なデータベース接続をシミュレート
    engine.dispose()
    
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "full_name": "Test User",
        "height": 170.0,
        "weight": 70.0,
        "age": 30,
        "gender": "male",
        "handicap": 10.5
    }
    response = client.post("/users/", json=user_data)
    print(f"Response status code: {response.status_code}")
    print(f"Response body: {response.json()}")
    assert response.status_code == 500
    assert "detail" in response.json() 