import pytest
import sys
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# プロジェクトのルートディレクトリをPythonパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# テスト環境の設定
os.environ["TESTING"] = "1"

from app.database import Base, engine, SessionLocal
from app import app
from app.core.security import create_access_token
import json
from datetime import datetime, timedelta
from jose import jwt

# テスト用のデータベース設定
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def db():
    Base.metadata.create_all(bind=engine)
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(db):
    # 各テスト用のセッションを作成
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="function")
def auth_headers():
    # テスト用のアクセストークンを作成
    access_token = create_access_token(data={"sub": "testuser"})
    return {"Authorization": f"Bearer {access_token}"}

@pytest.fixture
def test_user():
    return {
        "username": "testuser",
        "password": "testpassword",
        "email": "test@example.com",
        "full_name": "Test User"
    }

@pytest.fixture
def test_club_data():
    return {
        "club_id": 1,
        "brand": "XXIO",
        "model": "12",
        "loft": 10.5,
        "shaft": "MP1200",
        "shaft_flex": "R",
        "price": 80000,
        "features": "寛容性が高く、初級者から中級者向けのドライバー"
    }

@pytest.fixture
def test_user_data():
    return {
        "gender": "male",
        "age": 30,
        "height": 175,
        "handicap": 20,
        "swing_speed": 35,
        "ball_speed": 130,
        "launch_angle": 12,
        "spin_rate": 3000,
        "preferred_brands": ["XXIO", "Callaway"],
        "budget": 300000,
        "preferred_shaft_flex": "R",
        "preferred_shaft_weight": "軽量",
        "preferred_club_feel": "柔らかい",
        "preferred_shot_shape": "ストレート",
        "preferred_forgiveness": "高め",
        "preferred_workability": "低め",
        "preferred_distance": "長め",
        "preferred_accuracy": "高め",
        "preferred_consistency": "高め",
        "preferred_launch": "中",
        "preferred_spin": "中",
        "preferred_trajectory": "中",
        "preferred_sound": "静か",
        "preferred_look": "モダン",
        "preferred_material": "チタン",
        "preferred_technology": "最新",
        "preferred_customization": "可能",
        "preferred_durability": "高め",
        "preferred_maintenance": "簡単",
        "preferred_price_range": "中価格帯",
        "preferred_availability": "国内",
        "preferred_warranty": "長期",
        "preferred_service": "充実",
        "preferred_reviews": "高評価",
        "preferred_reputation": "高",
        "preferred_innovation": "高",
        "preferred_tradition": "中",
        "preferred_performance": "高",
        "preferred_value": "高",
        "preferred_style": "モダン",
        "preferred_comfort": "高",
        "preferred_fit": "標準",
        "preferred_support": "高",
        "preferred_breathability": "高",
        "preferred_water_resistance": "中",
        "preferred_insulation": "低",
        "preferred_flexibility": "中",
        "preferred_stability": "高",
        "preferred_cushioning": "中",
        "preferred_traction": "高"
    }

@pytest.fixture
def test_token():
    to_encode = {
        "sub": "testuser",
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }
    return jwt.encode(
        to_encode,
        os.environ["JWT_SECRET_KEY"],
        algorithm=os.environ["JWT_ALGORITHM"]
    ) 