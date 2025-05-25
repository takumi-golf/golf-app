from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import pytest
from app.main import app
from app.database import Base, get_db
from app import models, schemas
from app.models import Brand, ClubModel, ClubSpecification, Shaft
from fastapi import status
from app.error_handlers import ErrorMessages
import requests
import json
import time

# テスト用のデータベース設定
SQLALCHEMY_DATABASE_URL = "sqlite://"

# テスト用のエンジンとセッションを作成
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
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

def test_read_root(client):
    """ルートエンドポイントのテスト"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_create_user(client):
    """ユーザー作成のテスト"""
    user_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == user_data["email"]
    assert "id" in data

def test_read_users(client, test_user):
    """ユーザー一覧取得のテスト"""
    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["email"] == test_user["email"]

def test_read_user(client, test_user):
    """特定のユーザー取得のテスト"""
    response = client.get(f"/api/v1/users/{test_user['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user["email"]

def test_create_recommendation(client):
    """レコメンデーション作成のテスト"""
    profile_data = {
        "head_speed": 40.0,
        "handicap": 15.0,
        "age": 35,
        "gender": "male"
    }
    response = client.post("/api/v1/recommendations/", json=profile_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "id" in data
    assert "segment" in data
    assert "shaft_recommendation" in data

def test_read_recommendations(client):
    """レコメンデーション一覧取得のテスト"""
    # プレイヤープロファイルとレコメンデーションを作成
    profile_data = {
        "head_speed": 40.0,
        "handicap": 15.0,
        "age": 35,
        "gender": "male"
    }
    client.post("/api/v1/recommendations/", json=profile_data)

    response = client.get("/api/v1/recommendations/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

def test_read_recommendation(client):
    """特定のレコメンデーション取得のテスト"""
    # プレイヤープロファイルとレコメンデーションを作成
    profile_data = {
        "head_speed": 40.0,
        "handicap": 15.0,
        "age": 35,
        "gender": "male"
    }
    create_response = client.post("/api/v1/recommendations/", json=profile_data)
    recommendation_id = create_response.json()["id"]

    response = client.get(f"/api/v1/recommendations/{recommendation_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == recommendation_id

def test_get_brands(client):
    """ブランド一覧取得のテスト"""
    response = client.get("/api/clubs/brands/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_brand(client):
    """ブランド作成のテスト"""
    brand_data = {
        "name": "Test Brand",
        "logo_path": "/images/brands/test.png"
    }
    response = client.post("/api/clubs/brands/", json=brand_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == brand_data["name"]
    assert "id" in data

def test_get_club_models(client):
    """クラブモデル一覧取得のテスト"""
    response = client.get("/api/clubs/models/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_club_model(client):
    """クラブモデル作成のテスト"""
    # まずブランドを作成
    brand_data = {
        "name": "Test Brand",
        "logo_path": "/images/brands/test.png"
    }
    brand_response = client.post("/api/clubs/brands/", json=brand_data)
    brand_id = brand_response.json()["id"]

    model_data = {
        "name": "Test Model",
        "brand_id": brand_id,
        "release_year": 2024,
        "type": "driver",
        "category": "player"
    }
    response = client.post("/api/clubs/models/", json=model_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == model_data["name"]
    assert "id" in data

def test_get_club_specifications(client):
    """クラブスペック取得のテスト"""
    # まずブランドを作成
    brand_data = {
        "name": "Test Brand",
        "logo_path": "/images/brands/test.png"
    }
    brand_response = client.post("/api/clubs/brands/", json=brand_data)
    brand_id = brand_response.json()["id"]

    # クラブモデルを作成
    model_data = {
        "name": "Test Model",
        "brand_id": brand_id,
        "release_year": 2024,
        "type": "driver",
        "category": "player"
    }
    model_response = client.post("/api/clubs/models/", json=model_data)
    model_id = model_response.json()["id"]

    # スペックを作成
    spec_data = {
        "model_id": model_id,
        "loft": 10.5,
        "shaft_name": "Test Shaft",
        "flex": "S",
        "length": 45.5,
        "swing_weight": "D2"
    }
    response = client.post("/api/clubs/specifications/", json=spec_data)
    assert response.status_code == 200
    data = response.json()
    assert data["model_id"] == model_id
    assert "id" in data

BASE_URL = "http://localhost:8000"

def wait_for_server():
    """サーバーが起動するまで待機"""
    max_retries = 5
    for i in range(max_retries):
        try:
            requests.get(f"{BASE_URL}/")
            return True
        except requests.exceptions.ConnectionError:
            print(f"サーバー起動待機中... ({i+1}/{max_retries})")
            time.sleep(2)
    return False

def test_root():
    """ルートエンドポイントのテスト"""
    try:
        response = requests.get(f"{BASE_URL}/")
        print("ルートエンドポイントのテスト:")
        print(f"ステータスコード: {response.status_code}")
        print(f"レスポンス: {response.json()}\n")
        return True
    except Exception as e:
        print(f"ルートエンドポイントのテストでエラー: {e}\n")
        return False

def test_create_recommendation():
    """レコメンデーション作成APIのテスト"""
    try:
        data = {
            "head_speed": 40.0,
            "handicap": 15.0,
            "age": 35,
            "gender": "male"
        }
        response = requests.post(
            f"{BASE_URL}/api/v1/recommendations/",
            json=data
        )
        print("レコメンデーション作成APIのテスト:")
        print(f"ステータスコード: {response.status_code}")
        print(f"レスポンス: {response.json()}\n")
        return True
    except Exception as e:
        print(f"レコメンデーション作成APIのテストでエラー: {e}\n")
        return False

def test_get_recommendations():
    """レコメンデーション一覧取得APIのテスト"""
    try:
        response = requests.get(f"{BASE_URL}/api/v1/recommendations/")
        print("レコメンデーション一覧取得APIのテスト:")
        print(f"ステータスコード: {response.status_code}")
        print(f"レスポンス: {response.json()}\n")
        return True
    except Exception as e:
        print(f"レコメンデーション一覧取得APIのテストでエラー: {e}\n")
        return False

if __name__ == "__main__":
    print("APIテストを開始します...\n")
    
    if not wait_for_server():
        print("サーバーに接続できませんでした。")
        exit(1)
    
    success = all([
        test_root(),
        test_create_recommendation(),
        test_get_recommendations()
    ])
    
    if success:
        print("全てのテストが成功しました。")
    else:
        print("一部のテストが失敗しました。")
        exit(1) 