from fastapi.testclient import TestClient
from app.main import app
from app.schemas.review import UserProfile
import pytest

client = TestClient(app)

def test_health_check():
    """ヘルスチェックエンドポイントのテスト"""
    response = client.get("/health")
    print(f"\n--- Response: {test_health_check.__name__} ---")
    print(response.json())
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

# --- /user-profile のテスト ---

def test_get_user_profile_success(mocker):
    """/user-profile の正常系テスト"""
    # --- Arrange ---
    mock_profile_obj = UserProfile(
        taste_preference=["フルーティー", "軽快"],
        aroma_preference=["柑橘系"],
        sweetness_level="やや甘口",
        expression_habit="「甘い」という表現を多用する傾向"
    )
    mocker.patch(
        "app.services.review_service.create_user_profile",
        return_value=mock_profile_obj
    )
    request_data = {
        "review_history": ["前のワインは甘すぎて苦手だった。"],
        "product_info_history": ["貴腐ワイン 2020"]
    }

    # --- Act ---
    response = client.post("/api/user-profile", json=request_data)
    print(f"\n--- Response: {test_get_user_profile_success.__name__} ---")
    print(response.json())

    # --- Assert ---
    assert response.status_code == 200
    assert response.json() == mock_profile_obj.dict()

def test_get_user_profile_not_found(mocker):
    """/user-profile でプロファイルが作成できなかった場合のテスト (404)"""
    # --- Arrange ---
    mocker.patch(
        "app.services.review_service.create_user_profile",
        return_value=None
    )
    request_data = {
        "review_history": [],
        "product_info_history": []
    }

    # --- Act ---
    response = client.post("/api/user-profile", json=request_data)
    print(f"\n--- Response: {test_get_user_profile_not_found.__name__} ---")
    print(response.json())

    # --- Assert ---
    assert response.status_code == 404
    assert "失敗" in response.json()["detail"]


# --- /regenerate-review のテスト ---

def test_regenerate_review_with_profile(mocker):
    """/regenerate-review の正常系テスト (プロファイルあり)"""
    # --- Arrange ---
    mock_review = "プロファイルを考慮した素晴らしいレビュー"
    mocker.patch(
        "app.services.review_service.regenerate_review_text",
        return_value=mock_review
    )
    request_data = {
        "original_review": "まあまあ",
        "product_info": "新しいワイン",
        "user_profile": {
            "taste_preference": ["フルーティー"],
            "aroma_preference": ["柑橘系"],
            "sweetness_level": "やや甘口",
            "expression_habit": "「甘い」を多用"
        }
    }

    # --- Act ---
    response = client.post("/api/regenerate-review", json=request_data)
    print(f"\n--- Response: {test_regenerate_review_with_profile.__name__} ---")
    print(response.json())

    # --- Assert ---
    assert response.status_code == 200
    assert response.json() == {"regenerated_review": mock_review}

def test_regenerate_review_without_profile(mocker):
    """/regenerate-review の正常系テスト (プロファイルなし)"""
    # --- Arrange ---
    mock_review = "シンプルな素晴らしいレビュー"
    mocker.patch(
        "app.services.review_service.regenerate_review_text",
        return_value=mock_review
    )
    request_data = {
        "original_review": "まあまあ",
        "product_info": "新しいワイン",
        "user_profile": None
    }

    # --- Act ---
    response = client.post("/api/regenerate-review", json=request_data)
    print(f"\n--- Response: {test_regenerate_review_without_profile.__name__} ---")
    print(response.json())

    # --- Assert ---
    assert response.status_code == 200
    assert response.json() == {"regenerated_review": mock_review}
