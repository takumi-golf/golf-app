import pytest
from fastapi import status

def test_recommendation_flow(client, test_user):
    """ユーザー登録からレコメンデーション取得までのエンドツーエンドフローをテスト"""
    # レコメンデーションを作成
    recommendation_data = {
        "user_id": test_user["id"],
        "club_name": "テストドライバー",
        "brand": "テストブランド",
        "loft": "10.5",
        "shaft": "テストシャフト",
        "flex": "S"
    }

    # レコメンデーション作成のテスト
    response = client.post("/api/v1/recommendations/", json=recommendation_data)
    assert response.status_code == status.HTTP_201_CREATED
    created_recommendation = response.json()
    assert created_recommendation["club_name"] == recommendation_data["club_name"]

    # 作成したレコメンデーションの取得テスト
    response = client.get(f"/api/v1/recommendations/{created_recommendation['id']}")
    assert response.status_code == status.HTTP_200_OK
    retrieved_recommendation = response.json()
    assert retrieved_recommendation["id"] == created_recommendation["id"]
    assert retrieved_recommendation["club_name"] == recommendation_data["club_name"]

def test_invalid_recommendation_data(client, test_user):
    """無効なレコメンデーションデータでの作成をテスト"""
    invalid_data = {
        "user_id": test_user["id"],
        "brand": "テストブランド",
        "loft": "10.5",
        "shaft": "テストシャフト",
        "flex": "S"
    }
    response = client.post("/api/v1/recommendations/", json=invalid_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "club_name" in response.json()["detail"][0]["loc"]

def test_nonexistent_user_recommendation(client):
    """存在しないユーザーIDでのレコメンデーション作成をテスト"""
    recommendation_data = {
        "user_id": 99999,  # 存在しないユーザーID
        "club_name": "テストドライバー",
        "brand": "テストブランド",
        "loft": "10.5",
        "shaft": "テストシャフト",
        "flex": "S"
    }
    response = client.post("/api/v1/recommendations/", json=recommendation_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "ユーザーID" in response.json()["detail"]

def test_recommendation_pagination(client, test_user):
    """レコメンデーションのページネーションをテスト"""
    # 複数のレコメンデーションを作成
    for i in range(3):
        recommendation_data = {
            "user_id": test_user["id"],
            "club_name": f"テストドライバー{i}",
            "brand": "テストブランド",
            "loft": "10.5",
            "shaft": "テストシャフト",
            "flex": "S"
        }
        response = client.post("/api/v1/recommendations/", json=recommendation_data)
        assert response.status_code == status.HTTP_201_CREATED

    # ページネーションのテスト
    response = client.get("/api/v1/recommendations/?skip=0&limit=2")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["recommendations"]) == 2
    assert data["total"] >= 3

def test_recommendation_filtering(client, test_user):
    """レコメンデーションのフィルタリングをテスト"""
    # テスト用のレコメンデーションを作成
    recommendation_data = {
        "user_id": test_user["id"],
        "club_name": "テストドライバー",
        "brand": "テストブランド",
        "loft": "10.5",
        "shaft": "テストシャフト",
        "flex": "S"
    }
    response = client.post("/api/v1/recommendations/", json=recommendation_data)
    assert response.status_code == status.HTTP_201_CREATED

    # ユーザーIDでフィルタリング
    response = client.get(f"/api/v1/recommendations/?user_id={test_user['id']}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["recommendations"]) > 0
    assert all(r["user_id"] == test_user["id"] for r in data["recommendations"])

def test_nonexistent_recommendation(client):
    """存在しないレコメンデーションIDでの取得をテスト"""
    response = client.get("/api/v1/recommendations/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "レコメンデーションID" in response.json()["detail"]

def test_duplicate_email_registration(client):
    """重複するメールアドレスでのユーザー登録をテスト"""
    # 最初のユーザー登録
    user_data = {
        "email": "duplicate@example.com",
        "password": "testpassword"
    }
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == status.HTTP_201_CREATED

    # 同じメールアドレスでの登録
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "メールアドレスは既に登録されています" in response.json()["detail"]

def test_invalid_user_id_format(client):
    """無効なユーザーID形式でのリクエストをテスト"""
    response = client.get("/api/v1/users/invalid")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "user_id" in response.json()["detail"][0]["loc"] 