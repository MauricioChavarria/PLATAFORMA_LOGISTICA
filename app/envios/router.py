from fastapi import APIRouter, Depends, Query

from app.autenticacion.dependencies import obtener_usuario_actual
from app.comun.dependencias import DBSession
from app.envios.schemas import ActualizarEnvioDTO, CrearEnvioDTO, EnvioDTO, ListaEnviosDTO, TipoEnvio
from app.envios.service import actualizar_envio, crear_envio, eliminar_envio, listar_envios, obtener_envio

router = APIRouter()


@router.post("/envios", response_model=EnvioDTO)
def crear(dto: CrearEnvioDTO, db: DBSession, _: dict = Depends(obtener_usuario_actual)) -> EnvioDTO:
    envio, terrestre, maritimo = crear_envio(db, dto)
    return EnvioDTO(**{
        "id": envio.id,
        "cliente_id": envio.cliente_id,
        "producto_id": envio.producto_id,
        "cantidad": envio.cantidad,
        "fecha_registro": envio.fecha_registro,
        "fecha_entrega": envio.fecha_entrega,
        "precio_base": envio.precio_base,
        "descuento": envio.descuento,
        "precio_final": envio.precio_final,
        "numero_guia": envio.numero_guia,
        "tipo_envio": envio.tipo_envio,
        "bodega_id": terrestre.bodega_id if terrestre is not None else None,
        "placa_vehiculo": terrestre.placa_vehiculo if terrestre is not None else None,
        "puerto_id": maritimo.puerto_id if maritimo is not None else None,
        "numero_flota": maritimo.numero_flota if maritimo is not None else None,
        "creado_en": envio.creado_en,
    })


@router.get("/envios", response_model=ListaEnviosDTO)
def listar(
    db: DBSession,
    _: dict = Depends(obtener_usuario_actual),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    q: str | None = Query(None, min_length=1),
    cliente_id: int | None = None,
    producto_id: int | None = None,
    tipo_envio: TipoEnvio | None = None,
) -> ListaEnviosDTO:
    items, total = listar_envios(
        db,
        page=page,
        page_size=page_size,
        q=q,
        cliente_id=cliente_id,
        producto_id=producto_id,
        tipo_envio=tipo_envio,
    )

    return ListaEnviosDTO(
        page=page,
        page_size=page_size,
        total=total,
        items=[
            EnvioDTO(**{
                "id": envio.id,
                "cliente_id": envio.cliente_id,
                "producto_id": envio.producto_id,
                "cantidad": envio.cantidad,
                "fecha_registro": envio.fecha_registro,
                "fecha_entrega": envio.fecha_entrega,
                "precio_base": envio.precio_base,
                "descuento": envio.descuento,
                "precio_final": envio.precio_final,
                "numero_guia": envio.numero_guia,
                "tipo_envio": envio.tipo_envio,
                "bodega_id": terrestre.bodega_id if terrestre is not None else None,
                "placa_vehiculo": terrestre.placa_vehiculo if terrestre is not None else None,
                "puerto_id": maritimo.puerto_id if maritimo is not None else None,
                "numero_flota": maritimo.numero_flota if maritimo is not None else None,
                "creado_en": envio.creado_en,
            })
            for (envio, terrestre, maritimo) in items
        ],
    )


@router.get("/envios/{envio_id}", response_model=EnvioDTO)
def obtener(envio_id: int, db: DBSession, _: dict = Depends(obtener_usuario_actual)) -> EnvioDTO:
    envio, terrestre, maritimo = obtener_envio(db, envio_id)
    return EnvioDTO(**{
        "id": envio.id,
        "cliente_id": envio.cliente_id,
        "producto_id": envio.producto_id,
        "cantidad": envio.cantidad,
        "fecha_registro": envio.fecha_registro,
        "fecha_entrega": envio.fecha_entrega,
        "precio_base": envio.precio_base,
        "descuento": envio.descuento,
        "precio_final": envio.precio_final,
        "numero_guia": envio.numero_guia,
        "tipo_envio": envio.tipo_envio,
        "bodega_id": terrestre.bodega_id if terrestre is not None else None,
        "placa_vehiculo": terrestre.placa_vehiculo if terrestre is not None else None,
        "puerto_id": maritimo.puerto_id if maritimo is not None else None,
        "numero_flota": maritimo.numero_flota if maritimo is not None else None,
        "creado_en": envio.creado_en,
    })


@router.patch("/envios/{envio_id}", response_model=EnvioDTO)
def actualizar(envio_id: int, dto: ActualizarEnvioDTO, db: DBSession, _: dict = Depends(obtener_usuario_actual)) -> EnvioDTO:
    envio, terrestre, maritimo = actualizar_envio(db, envio_id, dto)
    return EnvioDTO(**{
        "id": envio.id,
        "cliente_id": envio.cliente_id,
        "producto_id": envio.producto_id,
        "cantidad": envio.cantidad,
        "fecha_registro": envio.fecha_registro,
        "fecha_entrega": envio.fecha_entrega,
        "precio_base": envio.precio_base,
        "descuento": envio.descuento,
        "precio_final": envio.precio_final,
        "numero_guia": envio.numero_guia,
        "tipo_envio": envio.tipo_envio,
        "bodega_id": terrestre.bodega_id if terrestre is not None else None,
        "placa_vehiculo": terrestre.placa_vehiculo if terrestre is not None else None,
        "puerto_id": maritimo.puerto_id if maritimo is not None else None,
        "numero_flota": maritimo.numero_flota if maritimo is not None else None,
        "creado_en": envio.creado_en,
    })


@router.delete("/envios/{envio_id}")
def eliminar(envio_id: int, db: DBSession, _: dict = Depends(obtener_usuario_actual)) -> dict:
    eliminar_envio(db, envio_id)
    return {"status": "ok"}
