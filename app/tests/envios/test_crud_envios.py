from fastapi.testclient import TestClient

from decimal import Decimal


def _token(client: TestClient) -> str:
    resp = client.post("/api/v1/auth/token", json={"username": "admin", "password": "admin"})
    assert resp.status_code == 200
    return resp.json()["access_token"]


def _crear_cliente(client: TestClient, headers: dict) -> int:
    r = client.post(
        "/api/v1/clientes",
        headers=headers,
        json={
            "nombre": "Juan",
            "email": "juan@example.com",
            "documento": "123",
            "telefono": "3000000000",
        },
    )
    assert r.status_code == 200
    return r.json()["id"]


def _crear_producto(client: TestClient, headers: dict) -> int:
    r = client.post("/api/v1/productos", headers=headers, json={"nombre": "Caja", "descripcion": "Caja"})
    assert r.status_code == 200
    return r.json()["id"]


def _crear_bodega(client: TestClient, headers: dict) -> int:
    r = client.post(
        "/api/v1/bodegas",
        headers=headers,
        json={"nombre": "Bodega Norte", "ubicacion": "Zona 1", "pais": "CO"},
    )
    assert r.status_code == 200
    return r.json()["id"]


def _crear_puerto(client: TestClient, headers: dict) -> int:
    r = client.post("/api/v1/puertos", headers=headers, json={"nombre": "Cartagena", "pais": "CO"})
    assert r.status_code == 200
    return r.json()["id"]


def test_crud_envios_terrestre_y_maritimo(client: TestClient) -> None:
    token = _token(client)
    headers = {"Authorization": f"Bearer {token}"}

    cliente_id = _crear_cliente(client, headers)
    producto_id = _crear_producto(client, headers)
    bodega_id = _crear_bodega(client, headers)
    puerto_id = _crear_puerto(client, headers)

    r = client.post(
        "/api/v1/envios",
        headers=headers,
        json={
            "cliente_id": cliente_id,
            "producto_id": producto_id,
            "cantidad": 2,
            "fecha_registro": "2026-02-01",
            "fecha_entrega": "2026-02-10",
            "precio_base": 1000,
            "descuento": 100,
            "numero_guia": "G-TER-001",
            "tipo_envio": "TERRESTRE",
            "bodega_id": bodega_id,
            "placa_vehiculo": "ABC123",
        },
    )
    assert r.status_code == 200
    envio_ter_id = r.json()["id"]
    assert Decimal(r.json()["precio_final"]) == Decimal("900.00")
    assert r.json()["bodega_id"] == bodega_id

    r = client.post(
        "/api/v1/envios",
        headers=headers,
        json={
            "cliente_id": cliente_id,
            "producto_id": producto_id,
            "cantidad": 1,
            "fecha_registro": "2026-02-01",
            "fecha_entrega": "2026-02-12",
            "precio_base": 2000,
            "descuento": 0,
            "numero_guia": "G-MAR-001",
            "tipo_envio": "MARITIMO",
            "puerto_id": puerto_id,
            "numero_flota": "F-01",
        },
    )
    assert r.status_code == 200
    envio_mar_id = r.json()["id"]
    assert r.json()["puerto_id"] == puerto_id

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
        json={"descuento": 200, "placa_vehiculo": "ZZZ999"},
    )
    assert r.status_code == 200
    assert Decimal(r.json()["precio_final"]) == Decimal("800.00")
    assert r.json()["placa_vehiculo"] == "ZZZ999"

    r = client.delete(f"/api/v1/envios/{envio_mar_id}", headers=headers)
    assert r.status_code == 200

    r = client.get("/api/v1/envios", headers=headers)
    assert r.status_code == 200
    assert r.json()["total"] == 1

    r = client.get(f"/api/v1/envios/{envio_mar_id}", headers=headers)
    assert r.status_code == 404
