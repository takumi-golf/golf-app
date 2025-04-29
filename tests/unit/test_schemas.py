import pytest
from schemas import (
    UserCreate,
    UserUpdate,
    UserPreferences,
    ClubRecommendation,
    ClubSearch,
    ClubSearchResponse,
    ErrorResponse
)

def test_user_create_validation():
    # 正常なケース
    user = UserCreate(
        username="testuser",
        password="password123",
        email="test@example.com",
        full_name="Test User",
        height=175.0,
        weight=70.0,
        age=30,
        gender="male"
    )
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.height == 175.0
    assert user.weight == 70.0
    assert user.age == 30
    assert user.gender == "male"

    # 異常なケース（パスワードが短すぎる）
    with pytest.raises(ValueError):
        UserCreate(
            username="testuser",
            password="123",
            email="test@example.com",
            full_name="Test User",
            height=175.0,
            weight=70.0,
            age=30,
            gender="male"
        )

def test_user_preferences_validation():
    # 正常なケース
    prefs = UserPreferences(
        gender="male",
        age=30,
        height=175,
        handicap=20,
        swing_speed=35,
        ball_speed=130,
        launch_angle=12,
        spin_rate=3000,
        preferred_brands=["XXIO", "Callaway"],
        budget=300000
    )
    assert prefs.gender == "male"
    assert prefs.age == 30

    # 異常なケース（年齢が範囲外）
    with pytest.raises(ValueError):
        UserPreferences(
            gender="male",
            age=150,  # 無効な年齢
            height=175,
            handicap=20,
            swing_speed=35,
            ball_speed=130,
            launch_angle=12,
            spin_rate=3000,
            preferred_brands=["XXIO"],
            budget=300000
        )

def test_club_recommendation_validation():
    # 正常なケース
    club = ClubRecommendation(
        club_id=1,
        brand="XXIO",
        model="12",
        loft=10.5,
        shaft="MP1200",
        shaft_flex="R",
        price=80000,
        features="寛容性が高く、初級者から中級者向けのドライバー",
        match_score=0.85,
        confidence_score=0.9
    )
    assert club.brand == "XXIO"
    assert club.match_score == 0.85

    # 異常なケース（価格が負の値）
    with pytest.raises(ValueError):
        ClubRecommendation(
            club_id=1,
            brand="XXIO",
            model="12",
            loft=10.5,
            shaft="MP1200",
            shaft_flex="R",
            price=-80000,  # 無効な価格
            features="寛容性が高く、初級者から中級者向けのドライバー",
            match_score=0.85,
            confidence_score=0.9
        )

def test_error_response():
    error = ErrorResponse(
        error_code="INVALID_INPUT",
        message="入力値が無効です",
        details={"field": "age", "reason": "範囲外の値です"}
    )
    assert error.error_code == "INVALID_INPUT"
    assert error.message == "入力値が無効です"
    assert "field" in error.details 