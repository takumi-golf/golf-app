import pytest
from fastapi.testclient import TestClient
from app import app
from schemas import UserCreate, UserPreferences, ClubSearch
from tests.security import create_access_token

@pytest.fixture
def client():
    return TestClient(app)

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_create_user(client):
    user_data = {
        "username": "testuser",
        "password": "password123",
        "email": "test@example.com",
        "full_name": "Test User",
        "height": 175.0,
        "weight": 70.0,
        "age": 30,
        "gender": "male"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == user_data["username"]
    assert data["email"] == user_data["email"]
    assert "password" not in data

def test_login(client):
    # テスト用のアクセストークンを作成
    access_token = create_access_token(data={"sub": "testuser"})
    response = client.post(
        "/token",
        data={"username": "testuser", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_get_recommendations(client):
    # テスト用のアクセストークンを作成
    access_token = create_access_token(data={"sub": "testuser"})
    headers = {"Authorization": f"Bearer {access_token}"}
    
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
    
    response = client.post(
        "/recommendations/",
        json=preferences,
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "clubs" in data

def test_search_clubs(client):
    # テスト用のアクセストークンを作成
    access_token = create_access_token(data={"sub": "testuser"})
    headers = {"Authorization": f"Bearer {access_token}"}
    
    search_params = {
        "brand": "XXIO",
        "min_price": 50000,
        "max_price": 100000,
        "shaft_flex": "R"
    }
    
    response = client.get(
        "/clubs/search",
        params=search_params,
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "clubs" in data

def test_unauthorized_access(client):
    response = client.get("/clubs/search")
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data

def test_invalid_token(client):
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/clubs/search", headers=headers)
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data 