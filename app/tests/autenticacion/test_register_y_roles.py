from fastapi.testclient import TestClient


def _token_admin(client: TestClient) -> str:
    resp = client.post("/api/v1/auth/token", json={"username": "admin", "password": "admin"})
    assert resp.status_code == 200
    return resp.json()["access_token"]


def _token_user(client: TestClient, username: str, password: str) -> str:
    resp = client.post("/api/v1/auth/token", json={"username": username, "password": password})
    assert resp.status_code == 200
    return resp.json()["access_token"]


def test_register_login_me_y_prohibido_delete(client: TestClient) -> None:
    # register
    r = client.post(
        "/api/v1/auth/register",
        json={"username": "user1", "password": "secret123"},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["username"] == "user1"
    assert data["role"] == "user"

    # login user
    token_user = _token_user(client, "user1", "secret123")

    # me
    r = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token_user}"})
    assert r.status_code == 200
    me = r.json()
    assert me["sub"] == "user1"
    assert me["role"] == "user"

    # user puede crear cliente (solo delete es admin)
    r = client.post(
        "/api/v1/clientes",
        headers={"Authorization": f"Bearer {token_user}"},
        json={"nombre": "Cliente X", "email": "x@test.com", "telefono": "3001234567"},
    )
    assert r.status_code == 200
    cliente_id = r.json()["id_cliente"]

    # user NO puede eliminar (admin-only)
    r = client.delete(
        f"/api/v1/clientes/{cliente_id}",
        headers={"Authorization": f"Bearer {token_user}"},
    )
    assert r.status_code == 403

    # admin SÍ puede eliminar
    token_admin = _token_admin(client)
    r = client.delete(
        f"/api/v1/clientes/{cliente_id}",
        headers={"Authorization": f"Bearer {token_admin}"},
    )
    assert r.status_code == 200
