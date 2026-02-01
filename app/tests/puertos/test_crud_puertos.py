from fastapi.testclient import TestClient


def _token(client: TestClient) -> str:
    resp = client.post("/api/v1/auth/token", json={"username": "admin", "password": "admin"})
    assert resp.status_code == 200
    return resp.json()["access_token"]


def test_crud_puertos_soft_delete_filtros_paginacion(client: TestClient) -> None:
    token = _token(client)
    headers = {"Authorization": f"Bearer {token}"}

    r = client.post(
        "/api/v1/puertos",
        headers=headers,
        json={"nombre": "Cartagena", "pais": "CO"},
    )
    assert r.status_code == 200
    puerto_id = r.json()["id"]

    r = client.get(f"/api/v1/puertos/{puerto_id}", headers=headers)
    assert r.status_code == 200
    assert r.json()["nombre"] == "Cartagena"

    r = client.get("/api/v1/puertos?page=1&page_size=10", headers=headers)
    assert r.status_code == 200
    assert r.json()["total"] == 1

    r = client.get("/api/v1/puertos?q=Cart", headers=headers)
    assert r.status_code == 200
    assert r.json()["total"] == 1

    r = client.get("/api/v1/puertos?pais=CO", headers=headers)
    assert r.status_code == 200
    assert r.json()["total"] == 1

    r = client.delete(f"/api/v1/puertos/{puerto_id}", headers=headers)
    assert r.status_code == 200

    r = client.get("/api/v1/puertos", headers=headers)
    assert r.status_code == 200
    assert r.json()["total"] == 0

    r = client.get(f"/api/v1/puertos/{puerto_id}", headers=headers)
    assert r.status_code == 404
