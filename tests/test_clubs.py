import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.database import get_db, init_db
from app.models import Club
import json

client = TestClient(app)

@pytest.fixture
def test_db():
    """テスト用のデータベースセッションを作成"""
    db = next(get_db())
    init_db()
    yield db
    db.close()

@pytest.fixture
def sample_clubs(test_db: Session):
    """テスト用のサンプルクラブデータを作成"""
    clubs = [
        Club(
            club_id="driver1",
            brand="TaylorMade",
            model="Stealth",
            type="driver",
            loft=10.5,
            shaft="Fujikura",
            shaft_flex="S",
            price=45000,
            features=json.dumps({
                "trajectory": "中弾道",
                "spin": "中スピン",
                "forgiveness": "高"
            }),
            specifications=json.dumps({
                "length": "45.75",
                "weight": "310g"
            }),
            popularity_score=0.0
        ),
        Club(
            club_id="driver2",
            brand="Callaway",
            model="Paradym",
            type="driver",
            loft=9.0,
            shaft="Mitsubishi",
            shaft_flex="X",
            price=50000,
            features=json.dumps({
                "trajectory": "低弾道",
                "spin": "低スピン",
                "forgiveness": "中"
            }),
            specifications=json.dumps({
                "length": "45.5",
                "weight": "305g"
            }),
            popularity_score=0.5
        ),
        Club(
            club_id="iron1",
            brand="Titleist",
            model="T200",
            type="iron",
            loft=7.0,
            shaft="True Temper",
            shaft_flex="R",
            price=35000,
            features=json.dumps({
                "trajectory": "高弾道",
                "spin": "高スピン",
                "forgiveness": "高"
            }),
            specifications=json.dumps({
                "length": "37.0",
                "weight": "285g"
            }),
            popularity_score=0.3
        )
    ]
    for club in clubs:
        test_db.add(club)
    test_db.commit()
    return clubs

def test_get_clubs(test_db: Session, sample_clubs):
    """クラブ一覧取得のテスト"""
    response = client.get("/clubs/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert data[0]["brand"] == "TaylorMade"
    assert data[1]["brand"] == "Callaway"
    assert data[2]["brand"] == "Titleist"

def test_get_clubs_by_type(test_db: Session, sample_clubs):
    """タイプによるクラブ検索のテスト"""
    response = client.get("/clubs/?type=driver")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(club["type"] == "driver" for club in data)

def test_get_clubs_by_brand(test_db: Session, sample_clubs):
    """ブランドによるクラブ検索のテスト"""
    response = client.get("/clubs/?brand=TaylorMade")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["brand"] == "TaylorMade"

def test_get_club_detail(test_db: Session, sample_clubs):
    """クラブ詳細取得のテスト"""
    response = client.get("/clubs/driver1")
    assert response.status_code == 200
    data = response.json()
    assert data["club_id"] == "driver1"
    assert data["brand"] == "TaylorMade"
    assert data["model"] == "Stealth"

def test_get_popular_clubs(test_db: Session, sample_clubs):
    """人気クラブ取得のテスト"""
    response = client.get("/clubs/popular")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    # 人気度の降順でソートされていることを確認
    assert data[0]["popularity_score"] >= data[1]["popularity_score"]
    assert data[1]["popularity_score"] >= data[2]["popularity_score"]

def test_search_clubs(test_db: Session, sample_clubs):
    """詳細検索のテスト"""
    search_data = {
        "type": "driver",
        "min_price": 40000,
        "max_price": 55000
    }
    response = client.post("/clubs/search", json=search_data)
    assert response.status_code == 200
    data = response.json()
    assert "clubs" in data
    assert "total_count" in data
    assert "page" in data
    assert "per_page" in data
    assert len(data["clubs"]) == 2
    assert all(club["type"] == "driver" for club in data["clubs"])
    assert all(40000 <= club["price"] <= 55000 for club in data["clubs"])

def test_recommend_clubs(test_db: Session, sample_clubs):
    """レコメンデーションのテスト"""
    search_data = {
        "type": "driver",
        "swing_speed": 42,
        "spin_preference": "中スピン",
        "forgiveness_preference": "高"
    }
    response = client.post("/clubs/recommend", json=search_data)
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    # スコアの降順でソートされていることを確認
    assert data[0]["score"] >= data[1]["score"]
    # マッチ理由が含まれていることを確認
    assert "match_reasons" in data[0]
    assert len(data[0]["match_reasons"]) > 0

def test_club_not_found(test_db: Session):
    """存在しないクラブのテスト"""
    response = client.get("/clubs/nonexistent")
    assert response.status_code == 404
    assert response.json()["detail"] == "Club not found" 