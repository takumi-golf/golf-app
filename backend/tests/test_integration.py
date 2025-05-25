import pytest
from fastapi import status
from app.error_handlers import ErrorMessages

def test_recommendation_flow(client, test_user):
    """ユーザー登録からレコメンデーション取得までのエンドツーエンドフローをテスト"""
    # レコメンデーションを作成
    recommendation_data = {
        "head_speed": 40.0,
        "handicap": 15.0,
        "age": 35,
        "gender": "male"
    }

    # レコメンデーション作成のテスト
    response = client.post("/api/v1/recommendations/", json=recommendation_data)
    assert response.status_code == status.HTTP_201_CREATED
    recommendation = response.json()
    assert "id" in recommendation
    assert "segment" in recommendation
    assert "shaft_recommendation" in recommendation

    # レコメンデーション取得のテスト
    response = client.get(f"/api/v1/recommendations/{recommendation['id']}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == recommendation["id"]

    # フィードバック追加のテスト
    feedback_data = {
        "feedback": "とても良い推奨でした",
        "rating": 5
    }
    response = client.post(f"/api/v1/recommendations/{recommendation['id']}/feedback", json=feedback_data)
    assert response.status_code == status.HTTP_200_OK

def test_invalid_recommendation_data(client, test_user):
    """無効なレコメンデーションデータでの作成をテスト"""
    invalid_data = {
        "head_speed": -1.0,  # 無効な値
        "handicap": 100.0,  # 無効な値
        "age": 0,  # 無効な値
        "gender": "invalid"  # 無効な値
    }
    response = client.post("/api/v1/recommendations/", json=invalid_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    errors = response.json()["errors"]
    assert len(errors) > 0

def test_nonexistent_user_recommendation(client):
    """存在しないユーザーIDでのレコメンデーション作成をテスト"""
    response = client.get("/api/v1/recommendations/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == ErrorMessages.RECOMMENDATION_NOT_FOUND

def test_recommendation_pagination(client, test_user):
    """レコメンデーションのページネーションをテスト"""
    # 複数のレコメンデーションを作成
    for i in range(3):
        recommendation_data = {
            "head_speed": 40.0 + i,
            "handicap": 15.0,
            "age": 35,
            "gender": "male"
        }
        response = client.post("/api/v1/recommendations/", json=recommendation_data)
        assert response.status_code == status.HTTP_201_CREATED

    # ページネーションのテスト
    response = client.get("/api/v1/recommendations/?skip=0&limit=2")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2

def test_recommendation_filtering(client, test_user):
    """レコメンデーションのフィルタリングをテスト"""
    # テスト用のレコメンデーションを作成
    recommendation_data = {
        "head_speed": 40.0,
        "handicap": 15.0,
        "age": 35,
        "gender": "male"
    }
    response = client.post("/api/v1/recommendations/", json=recommendation_data)
    assert response.status_code == status.HTTP_201_CREATED
    recommendation = response.json()

    # フィルタリングのテスト
    response = client.get(f"/api/v1/recommendations/?segment={recommendation['segment']}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert all(item["segment"] == recommendation["segment"] for item in data)

def test_nonexistent_recommendation(client):
    """存在しないレコメンデーションIDでの取得をテスト"""
    response = client.get("/api/v1/recommendations/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == ErrorMessages.RECOMMENDATION_NOT_FOUND

def test_duplicate_email_registration(client):
    """重複するメールアドレスでのユーザー登録をテスト"""
    # 最初のユーザー登録
    user_data = {
        "email": "duplicate@example.com",
        "password": "testpassword123"
    }
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == status.HTTP_201_CREATED

    # 同じメールアドレスでの登録
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == ErrorMessages.DUPLICATE_EMAIL

def test_invalid_user_id_format(client):
    """無効なユーザーID形式でのリクエストをテスト"""
    response = client.get("/api/v1/users/invalid")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    errors = response.json()["errors"]
    assert any(error["field"] == "path.user_id" for error in errors) 