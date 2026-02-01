from fastapi.testclient import TestClient

from app.main import create_app


def test_token_ok() -> None:
    app = create_app()
    client = TestClient(app)

    resp = client.post("/api/v1/auth/token", json={"username": "admin", "password": "admin"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["token_type"] == "bearer"
    assert isinstance(data["access_token"], str)
    assert len(data["access_token"]) > 10
