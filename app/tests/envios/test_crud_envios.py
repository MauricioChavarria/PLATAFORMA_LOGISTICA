from fastapi.testclient import TestClient


def _token(client: TestClient) -> str:
    resp = client.post("/api/v1/auth/token", json={"username": "admin", "password": "admin"})
    assert resp.status_code == 200
    return resp.json()["access_token"]


def _crear_tipo_producto(client: TestClient, headers: dict) -> int:
    r = client.post("/api/v1/tipos-producto", headers=headers, json={"nombre": "Caja"})
    assert r.status_code == 200
    return r.json()["id_tipo_producto"]


def _crear_bodega(client: TestClient, headers: dict) -> int:
    r = client.post(
        "/api/v1/bodegas",
        headers=headers,
        json={"nombre": "Bodega Norte", "direccion": "Calle 123"},
    )
    assert r.status_code == 200
    return r.json()["id_bodega"]


def _crear_puerto(client: TestClient, headers: dict) -> int:
    r = client.post("/api/v1/puertos", headers=headers, json={"nombre": "Cartagena", "ciudad": "Cartagena"})
    assert r.status_code == 200
    return r.json()["id_puerto"]


def _crear_cliente(client: TestClient, headers: dict) -> int:
    r = client.post(
        "/api/v1/clientes",
        headers=headers,
        json={"nombre": "Cliente 1", "email": "cliente1@test.com", "telefono": "3000000000"},
    )
    assert r.status_code == 200
    return r.json()["id_cliente"]


def test_crud_envios_terrestre_y_maritimo(client: TestClient) -> None:
    token = _token(client)
    headers = {"Authorization": f"Bearer {token}"}

    cliente_id = _crear_cliente(client, headers)
    tipo_producto_id = _crear_tipo_producto(client, headers)
    bodega_id = _crear_bodega(client, headers)
    puerto_id = _crear_puerto(client, headers)

    r = client.post(
        "/api/v1/envios",
        headers=headers,
        json={
            "id_cliente": cliente_id,
            "id_tipo_producto": tipo_producto_id,
            "cantidad": 2,
            "fecha_registro": "2026-02-01",
            "fecha_entrega": "2026-02-10",
            "precio_base": 1000,
            "numero_guia": "G-TER-001",
            "tipo_envio": "TERRESTRE",
            "id_bodega": bodega_id,
            "placa_vehiculo": "ABC123",
        },
    )
    assert r.status_code == 200
    envio_ter_id = r.json()["id_envio"]
    assert r.json()["precio_base"] == "1000.00"
    assert r.json()["descuento"] == "0.00"
    assert r.json()["precio_final"] == "1000.00"
    assert r.json()["id_bodega"] == bodega_id

    r = client.post(
        "/api/v1/envios",
        headers=headers,
        json={
            "id_cliente": cliente_id,
            "id_tipo_producto": tipo_producto_id,
            "cantidad": 1,
            "fecha_registro": "2026-02-01",
            "fecha_entrega": "2026-02-12",
            "precio_base": 2000,
            "numero_guia": "G-MAR-001",
            "tipo_envio": "MARITIMO",
            "id_puerto": puerto_id,
            "numero_flota": "ABC1234Z",
        },
    )
    assert r.status_code == 200
    assert r.json()["id_puerto"] == puerto_id

    r = client.get("/api/v1/envios?page=1&page_size=10", headers=headers)
    assert r.status_code == 200
    assert r.json()["total"] == 2

    r = client.get("/api/v1/envios?tipo_envio=TERRESTRE", headers=headers)
    assert r.status_code == 200
    assert r.json()["total"] == 1

    r = client.get("/api/v1/envios?q=G-TER", headers=headers)
    assert r.status_code == 200
    assert r.json()["total"] == 1

    r = client.patch(
        f"/api/v1/envios/{envio_ter_id}",
        headers=headers,
        json={"precio_base": 1500, "placa_vehiculo": "ZZZ999"},
    )
    assert r.status_code == 200
    assert r.json()["precio_base"] == "1500.00"
    assert r.json()["precio_final"] == "1500.00"
    assert r.json()["placa_vehiculo"] == "ZZZ999"


def test_descuento_automatico_por_cantidad_y_tipo(client: TestClient) -> None:
    token = _token(client)
    headers = {"Authorization": f"Bearer {token}"}

    cliente_id = _crear_cliente(client, headers)
    tipo_producto_id = _crear_tipo_producto(client, headers)
    bodega_id = _crear_bodega(client, headers)
    puerto_id = _crear_puerto(client, headers)

    r = client.post(
        "/api/v1/envios",
        headers=headers,
        json={
            "id_cliente": cliente_id,
            "id_tipo_producto": tipo_producto_id,
            "cantidad": 11,
            "fecha_registro": "2026-02-01",
            "fecha_entrega": "2026-02-10",
            "precio_base": 1000,
            "numero_guia": "G-TER-011",
            "tipo_envio": "TERRESTRE",
            "id_bodega": bodega_id,
            "placa_vehiculo": "ABC123",
        },
    )
    assert r.status_code == 200
    assert r.json()["precio_base"] == "1000.00"
    assert r.json()["descuento"] == "50.00"
    assert r.json()["precio_final"] == "950.00"

    r = client.post(
        "/api/v1/envios",
        headers=headers,
        json={
            "id_cliente": cliente_id,
            "id_tipo_producto": tipo_producto_id,
            "cantidad": 11,
            "fecha_registro": "2026-02-01",
            "fecha_entrega": "2026-02-12",
            "precio_base": 1000,
            "numero_guia": "G-MAR-011",
            "tipo_envio": "MARITIMO",
            "id_puerto": puerto_id,
            "numero_flota": "ABC1234Z",
        },
    )
    assert r.status_code == 200
    envio_mar_id = r.json()["id_envio"]
    assert r.json()["precio_base"] == "1000.00"
    assert r.json()["descuento"] == "30.00"
    assert r.json()["precio_final"] == "970.00"

    r = client.delete(f"/api/v1/envios/{envio_mar_id}", headers=headers)
    assert r.status_code == 200

    r = client.get("/api/v1/envios", headers=headers)
    assert r.status_code == 200
    assert r.json()["total"] == 1

    r = client.get(f"/api/v1/envios/{envio_mar_id}", headers=headers)
    assert r.status_code == 404
