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
        json={"nombre": "Cartagena", "ciudad": "Cartagena"},
    )
    assert r.status_code == 200
    puerto_id = r.json()["id_puerto"]

    r = client.get(f"/api/v1/puertos/{puerto_id}", headers=headers)
    assert r.status_code == 200
    assert r.json()["nombre"] == "Cartagena"

    r = client.get("/api/v1/puertos?page=1&page_size=10", headers=headers)
    assert r.status_code == 200
    assert r.json()["total"] == 1

    r = client.get("/api/v1/puertos?q=Cart", headers=headers)
    assert r.status_code == 200
    assert r.json()["total"] == 1

    r = client.delete(f"/api/v1/puertos/{puerto_id}", headers=headers)
    assert r.status_code == 200

    r = client.get("/api/v1/puertos", headers=headers)
    assert r.status_code == 200
    assert r.json()["total"] == 0

    r = client.get(f"/api/v1/puertos/{puerto_id}", headers=headers)
    assert r.status_code == 404


def test_no_elimina_puerto_con_envios_asociados(client: TestClient) -> None:
    token = _token(client)
    headers = {"Authorization": f"Bearer {token}"}

    # Crear cliente
    r = client.post(
        "/api/v1/clientes",
        headers=headers,
        json={"nombre": "Cliente 1", "email": "cliente1@test.com", "telefono": "3000000000"},
    )
    assert r.status_code == 200
    cliente_id = r.json()["id_cliente"]

    # Crear tipo de producto
    r = client.post("/api/v1/tipos-producto", headers=headers, json={"nombre": "Caja"})
    assert r.status_code == 200
    tipo_producto_id = r.json()["id_tipo_producto"]

    # Crear puerto
    r = client.post(
        "/api/v1/puertos",
        headers=headers,
        json={"nombre": "Cartagena", "ciudad": "Cartagena"},
    )
    assert r.status_code == 200
    puerto_id = r.json()["id_puerto"]

    # Crear envío marítimo asociado al puerto
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
            "numero_guia": "G-PUE-001",
            "tipo_envio": "MARITIMO",
            "id_puerto": puerto_id,
            "numero_flota": "ABC1234Z",
        },
    )
    assert r.status_code == 200

    # Intentar eliminar puerto debe dar 409 (no 500)
    r = client.delete(f"/api/v1/puertos/{puerto_id}", headers=headers)
    assert r.status_code == 409
