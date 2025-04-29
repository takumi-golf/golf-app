import pytest
from fastapi.testclient import TestClient
from app import app
import json

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_user_registration():
    user_data = {
        "username": "testuser",
        "password": "testpassword123",
        "email": "test@example.com",
        "full_name": "Test User"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == user_data["username"]
    assert data["email"] == user_data["email"]
    assert "id" in data

def test_user_login():
    login_data = {
        "username": "testuser",
        "password": "testpassword123"
    }
    response = client.post("/token", data=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_club_recommendation():
    # まずログインしてトークンを取得
    login_data = {
        "username": "testuser",
        "password": "testpassword123"
    }
    login_response = client.post("/token", data=login_data)
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # ユーザープレファレンスを送信
    preferences = {
        "gender": "male",
        "age": 30,
        "height": 175,
        "handicap": 20,
        "swing_speed": 35,
        "ball_speed": 130,
        "launch_angle": 12,
        "spin_rate": 3000,
        "preferred_brands": ["XXIO", "Callaway"],
        "budget": 300000
    }
    response = client.post("/recommendations/", json=preferences, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "recommendations" in data
    assert len(data["recommendations"]) > 0
    assert "match_score" in data["recommendations"][0]

def test_club_search():
    search_params = {
        "brand": "XXIO",
        "min_price": 50000,
        "max_price": 100000,
        "shaft_flex": "R"
    }
    response = client.get("/clubs/search", params=search_params)
    assert response.status_code == 200
    data = response.json()
    assert "clubs" in data
    assert len(data["clubs"]) > 0
    assert all(club["brand"] == "XXIO" for club in data["clubs"])
    assert all(50000 <= club["price"] <= 100000 for club in data["clubs"])

def test_error_handling():
    # 無効なユーザー登録データ
    invalid_user_data = {
        "username": "test",
        "password": "123",  # 短すぎるパスワード
        "email": "invalid-email",
        "full_name": "Test User"
    }
    response = client.post("/users/", json=invalid_user_data)
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data

    # 存在しないエンドポイント
    response = client.get("/nonexistent")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data 