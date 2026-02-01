from fastapi.testclient import TestClient


def _token(client: TestClient) -> str:
    resp = client.post("/api/v1/auth/token", json={"username": "admin", "password": "admin"})
    assert resp.status_code == 200
    return resp.json()["access_token"]


def test_crud_tipos_producto_filtros_paginacion(client: TestClient) -> None:
    token = _token(client)
    headers = {"Authorization": f"Bearer {token}"}

    r = client.post(
        "/api/v1/tipos-producto",
        headers=headers,
        json={"nombre": "Caja"},
    )
    assert r.status_code == 200
    tipo_producto_id = r.json()["id_tipo_producto"]

    r = client.get(f"/api/v1/tipos-producto/{tipo_producto_id}", headers=headers)
    assert r.status_code == 200
    assert r.json()["nombre"] == "Caja"

    r = client.get("/api/v1/tipos-producto?page=1&page_size=10", headers=headers)
    assert r.status_code == 200
    assert r.json()["total"] == 1

    r = client.get("/api/v1/tipos-producto?q=Caj", headers=headers)
    assert r.status_code == 200
    assert r.json()["total"] == 1

    r = client.delete(f"/api/v1/tipos-producto/{tipo_producto_id}", headers=headers)
    assert r.status_code == 200

    r = client.get("/api/v1/tipos-producto", headers=headers)
    assert r.status_code == 200
    assert r.json()["total"] == 0

    r = client.get(f"/api/v1/tipos-producto/{tipo_producto_id}", headers=headers)
    assert r.status_code == 404


def test_no_elimina_tipo_producto_con_envios_asociados(client: TestClient) -> None:
    token = _token(client)
    headers = {"Authorization": f"Bearer {token}"}

    # Crea tipo producto
    r = client.post("/api/v1/tipos-producto", headers=headers, json={"nombre": "Caja-FK"})
    assert r.status_code == 200
    tipo_producto_id = r.json()["id_tipo_producto"]

    # Crea cliente y bodega para un envío terrestre
    r = client.post(
        "/api/v1/clientes",
        headers=headers,
        json={"nombre": "Cliente-FK", "email": "fk@test.com", "telefono": "300"},
    )
    assert r.status_code == 200
    cliente_id = r.json()["id_cliente"]

    r = client.post(
        "/api/v1/bodegas",
        headers=headers,
        json={"nombre": "Bodega-FK", "direccion": "Calle"},
    )
    assert r.status_code == 200
    bodega_id = r.json()["id_bodega"]

    r = client.post(
        "/api/v1/envios",
        headers=headers,
        json={
            "id_cliente": cliente_id,
            "id_tipo_producto": tipo_producto_id,
            "cantidad": 1,
            "fecha_registro": "2026-02-01",
            "fecha_entrega": "2026-02-10",
            "precio_base": 100,
            "numero_guia": "GFKTP001",
            "tipo_envio": "TERRESTRE",
            "id_bodega": bodega_id,
            "placa_vehiculo": "ABC123",
        },
    )
    assert r.status_code == 200

    # Intentar eliminar el tipo: debe fallar por FK (409)
    r = client.delete(f"/api/v1/tipos-producto/{tipo_producto_id}", headers=headers)
    assert r.status_code == 409
