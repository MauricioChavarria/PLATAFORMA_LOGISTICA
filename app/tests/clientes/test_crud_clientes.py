from fastapi.testclient import TestClient


def _token(client: TestClient) -> str:
    resp = client.post("/api/v1/auth/token", json={"username": "admin", "password": "admin"})
    assert resp.status_code == 200
    return resp.json()["access_token"]


def test_crud_clientes_filtros_paginacion(client: TestClient) -> None:
    token = _token(client)
    headers = {"Authorization": f"Bearer {token}"}

    # create
    r = client.post(
        "/api/v1/clientes",
        headers=headers,
        json={"nombre": "Mauricio", "email": "mauricio@test.com", "telefono": "3001234567"},
    )
    assert r.status_code == 200
    cliente_id = r.json()["id_cliente"]

    # get
    r = client.get(f"/api/v1/clientes/{cliente_id}", headers=headers)
    assert r.status_code == 200
    assert r.json()["email"] == "mauricio@test.com"

    # list (paginación)
    r = client.get("/api/v1/clientes?page=1&page_size=10", headers=headers)
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 1
    assert len(data["items"]) == 1

    # filtros (q)
    r = client.get("/api/v1/clientes?q=Maur", headers=headers)
    assert r.status_code == 200
    assert r.json()["total"] == 1

    r = client.get("/api/v1/clientes?q=NoExiste", headers=headers)
    assert r.status_code == 200
    assert r.json()["total"] == 0

    # delete físico
    r = client.delete(f"/api/v1/clientes/{cliente_id}", headers=headers)
    assert r.status_code == 200

    # no debe aparecer en list
    r = client.get("/api/v1/clientes", headers=headers)
    assert r.status_code == 200
    assert r.json()["total"] == 0

    # get debe ser 404
    r = client.get(f"/api/v1/clientes/{cliente_id}", headers=headers)
    assert r.status_code == 404
