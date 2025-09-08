from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

# 注: 実際にAPIを叩くテストは、APIキーの設定やモックが必要です。
# ここではヘルスチェックのみをテストします。
# def test_regenerate_review():
#     response = client.post(
#         "/api/regenerate-review",
#         json={"original_review": "このラーメン、まあまあだった。"}
#     )
#     assert response.status_code == 200
#     assert "regenerated_review" in response.json()
