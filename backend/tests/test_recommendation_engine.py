import pytest
from fastapi import status
from app.recommendation_engine import GolfClubRecommender
from app.models import PlayerProfile, ClubSpecification, Brand, ClubModel, Shaft
from app.schemas.recommendation import RecommendationRequest
from app.error_handlers import (
    HeadSpeedError, HandicapError, AgeError, GenderError,
    ErrorMessages
)

def test_determine_segment():
    """セグメント判定のテスト"""
    db = None  # テスト用のモックDB
    recommender = GolfClubRecommender(db)
    
    # テストケース
    assert recommender._determine_segment(46.0) == "high"
    assert recommender._determine_segment(42.0) == "intermediate"
    assert recommender._determine_segment(35.0) == "low"

def test_recommend_shaft():
    """シャフト推奨のテスト"""
    db = None  # テスト用のモックDB
    recommender = GolfClubRecommender(db)
    
    # テスト用のプロファイル
    profile = {
        "head_speed": 45.0,
        "handicap": 15.0,
        "age": 35,
        "gender": "male"
    }
    
    # シャフト推奨を取得
    shaft = recommender.recommend_shaft(profile)
    
    # 推奨結果の検証
    assert "フレックス" in shaft
    assert "スチール" in shaft or "カーボン" in shaft

def test_get_player_segment():
    """プレイヤーセグメントのテスト"""
    db = None  # テスト用のモックDB
    recommender = GolfClubRecommender(db)
    
    # テストケース
    segment = recommender._get_player_segment(45.0, 8.0, 35, "male")
    assert "high" in segment
    assert "expert" in segment
    assert "adult" in segment
    assert "male" in segment

def test_get_shaft_recommendation():
    """シャフトフレックス推奨のテスト"""
    db = None  # テスト用のモックDB
    recommender = GolfClubRecommender(db)
    
    # テストケース
    assert recommender._get_shaft_flex(46.0) == "X"
    assert recommender._get_shaft_flex(43.0) == "S"
    assert recommender._get_shaft_flex(40.0) == "R"
    assert recommender._get_shaft_flex(35.0) == "SR"
    assert recommender._get_shaft_flex(30.0) == "L"

def test_recommend_clubs():
    """クラブ推奨のテスト"""
    db = None  # テスト用のモックDB
    recommender = GolfClubRecommender(db)
    
    # テスト用のプロファイル
    profile = {
        "head_speed": 45.0,
        "handicap": 15.0,
        "age": 35,
        "gender": "male"
    }
    
    # 推奨を取得
    recommendation = recommender.recommend_clubs(profile)
    
    # レスポンスの検証
    assert "segment" in recommendation
    assert "shaft_recommendation" in recommendation
    assert "recommended_clubs" in recommendation
    assert isinstance(recommendation["recommended_clubs"], list)

def test_recommendation_with_invalid_data():
    """無効なデータでの推奨生成のテスト"""
    db = None  # テスト用のモックDB
    recommender = GolfClubRecommender(db)
    
    # 無効なヘッドスピード
    with pytest.raises(HeadSpeedError) as exc_info:
        recommender.recommend_clubs({
            "head_speed": -1.0,
            "handicap": 15.0,
            "age": 35,
            "gender": "male"
        })
    assert str(exc_info.value) == ErrorMessages.HEAD_SPEED_INVALID
    
    # 無効なハンディキャップ
    with pytest.raises(HandicapError) as exc_info:
        recommender.recommend_clubs({
            "head_speed": 45.0,
            "handicap": -5.0,
            "age": 35,
            "gender": "male"
        })
    assert str(exc_info.value) == ErrorMessages.HANDICAP_INVALID
    
    # 無効な年齢
    with pytest.raises(AgeError) as exc_info:
        recommender.recommend_clubs({
            "head_speed": 45.0,
            "handicap": 15.0,
            "age": 0,
            "gender": "male"
        })
    assert str(exc_info.value) == ErrorMessages.AGE_INVALID
    
    # 無効な性別
    with pytest.raises(GenderError) as exc_info:
        recommender.recommend_clubs({
            "head_speed": 45.0,
            "handicap": 15.0,
            "age": 35,
            "gender": "invalid"
        })
    assert str(exc_info.value) == ErrorMessages.GENDER_INVALID

def test_recommendation_with_edge_cases():
    """境界値でのレコメンデーション生成のテスト"""
    db = None  # テスト用のモックDB
    recommender = GolfClubRecommender(db)
    
    # 境界値のテストケース
    edge_cases = [
        {
            "head_speed": 0.1,  # 最小値に近い
            "handicap": 0.0,    # 最小値
            "age": 1,          # 最小値
            "gender": "male"
        },
        {
            "head_speed": 79.9,  # 最大値に近い
            "handicap": 53.9,    # 最大値に近い
            "age": 119,         # 最大値に近い
            "gender": "female"
        }
    ]
    
    # 境界値のテストケースは正常に処理されることを確認
    for case in edge_cases:
        recommendation = recommender.recommend_clubs(case)
        assert "segment" in recommendation
        assert "shaft_recommendation" in recommendation
        assert "recommended_clubs" in recommendation 