from fastapi.testclient import TestClient

from app.main import create_app


def _token(client: TestClient) -> str:
    resp = client.post("/api/v1/auth/token", json={"username": "admin", "password": "admin"})
    return resp.json()["access_token"]


def test_cotizar_terrestre_requiere_bearer() -> None:
    app = create_app()
    client = TestClient(app)

    resp = client.post(
        "/api/v1/envios/terrestres/cotizar",
        json={
            "guia": "GUIA-2026-000001",
            "cliente_id": 1,
            "placa_vehiculo": "ABC123",
            "codigo_flota": "FLT-0001",
            "cantidad": 10,
        },
    )
    assert resp.status_code == 401


def test_cotizar_terrestre_ok() -> None:
    app = create_app()
    client = TestClient(app)
    token = _token(client)

    resp = client.post(
        "/api/v1/envios/terrestres/cotizar",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "guia": "GUIA-2026-000001",
            "cliente_id": 1,
            "placa_vehiculo": "ABC123",
            "codigo_flota": "FLT-0001",
            "cantidad": 10,
        },
    )
    assert resp.status_code == 200
    assert resp.json()["descuento"] == 0.05
