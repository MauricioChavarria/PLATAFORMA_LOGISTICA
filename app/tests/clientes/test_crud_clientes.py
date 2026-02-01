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


def test_no_elimina_cliente_con_envios_asociados(client: TestClient) -> None:
    token = _token(client)
    headers = {"Authorization": f"Bearer {token}"}

    # Crear cliente
    r = client.post(
        "/api/v1/clientes",
        headers=headers,
        json={"nombre": "Cliente Con Envio", "email": "cliente.envio@test.com", "telefono": "3001112222"},
    )
    assert r.status_code == 200
    cliente_id = r.json()["id_cliente"]

    # Crear tipo de producto
    r = client.post("/api/v1/tipos-producto", headers=headers, json={"nombre": "Caja"})
    assert r.status_code == 200
    tipo_producto_id = r.json()["id_tipo_producto"]

    # Crear bodega
    r = client.post(
        "/api/v1/bodegas",
        headers=headers,
        json={"nombre": "Bodega Norte", "direccion": "Calle 123"},
    )
    assert r.status_code == 200
    bodega_id = r.json()["id_bodega"]

    # Crear envío asociado
    r = client.post(
        "/api/v1/envios",
        headers=headers,
        json={
            "id_cliente": cliente_id,
            "id_tipo_producto": tipo_producto_id,
            "cantidad": 1,
            "fecha_registro": "2026-02-01",
            "fecha_entrega": "2026-02-10",
            "precio_base": 1000,
            "numero_guia": "G-CLI-001",
            "tipo_envio": "TERRESTRE",
            "id_bodega": bodega_id,
            "placa_vehiculo": "ABC123",
        },
    )
    assert r.status_code == 200

    # Intentar eliminar cliente debe dar 409 (no 500)
    r = client.delete(f"/api/v1/clientes/{cliente_id}", headers=headers)
    assert r.status_code == 409
