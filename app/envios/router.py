from fastapi import APIRouter, Depends, Query

from app.autenticacion.dependencies import obtener_admin_actual, obtener_usuario_actual
from app.comun.dependencias import DBSession
from app.envios.schemas import ActualizarEnvioDTO, CrearEnvioDTO, EnvioDTO, ListaEnviosDTO, TipoEnvio
from app.envios.service import actualizar_envio, crear_envio, eliminar_envio, listar_envios, obtener_envio

router = APIRouter()


@router.post("/envios", response_model=EnvioDTO)
def crear(dto: CrearEnvioDTO, db: DBSession, _: dict = Depends(obtener_usuario_actual)) -> EnvioDTO:
    envio, terrestre, maritimo = crear_envio(db, dto)
    tipo_envio: TipoEnvio = "TERRESTRE" if terrestre is not None else "MARITIMO"
    return EnvioDTO(**{
        "id_envio": envio.id_envio,
        "id_cliente": envio.id_cliente,
        "id_tipo_producto": envio.id_tipo_producto,
        "cantidad": envio.cantidad,
        "fecha_registro": envio.fecha_registro,
        "fecha_entrega": envio.fecha_entrega,
        "precio_base": envio.precio_base,
        "descuento": envio.descuento,
        "precio_final": envio.precio_final,
        "numero_guia": envio.numero_guia,
        "tipo_envio": tipo_envio,
        "id_bodega": terrestre.id_bodega if terrestre is not None else None,
        "placa_vehiculo": terrestre.placa_vehiculo if terrestre is not None else None,
        "id_puerto": maritimo.id_puerto if maritimo is not None else None,
        "numero_flota": maritimo.numero_flota if maritimo is not None else None,
    })


@router.get("/envios", response_model=ListaEnviosDTO)
def listar(
    db: DBSession,
    _: dict = Depends(obtener_usuario_actual),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    q: str | None = Query(None, min_length=1),
    id_cliente: int | None = None,
    id_tipo_producto: int | None = None,
    tipo_envio: TipoEnvio | None = None,
) -> ListaEnviosDTO:
    items, total = listar_envios(
        db,
        page=page,
        page_size=page_size,
        q=q,
        id_cliente=id_cliente,
        id_tipo_producto=id_tipo_producto,
        tipo_envio=tipo_envio,
    )

    return ListaEnviosDTO(
        page=page,
        page_size=page_size,
        total=total,
        items=[
            EnvioDTO(**{
                "id_envio": envio.id_envio,
                "id_cliente": envio.id_cliente,
                "id_tipo_producto": envio.id_tipo_producto,
                "cantidad": envio.cantidad,
                "fecha_registro": envio.fecha_registro,
                "fecha_entrega": envio.fecha_entrega,
                "precio_base": envio.precio_base,
                "descuento": envio.descuento,
                "precio_final": envio.precio_final,
                "numero_guia": envio.numero_guia,
                "tipo_envio": ("TERRESTRE" if terrestre is not None else "MARITIMO"),
                "id_bodega": terrestre.id_bodega if terrestre is not None else None,
                "placa_vehiculo": terrestre.placa_vehiculo if terrestre is not None else None,
                "id_puerto": maritimo.id_puerto if maritimo is not None else None,
                "numero_flota": maritimo.numero_flota if maritimo is not None else None,
            })
            for (envio, terrestre, maritimo) in items
        ],
    )


@router.get("/envios/{envio_id}", response_model=EnvioDTO)
def obtener(envio_id: int, db: DBSession, _: dict = Depends(obtener_usuario_actual)) -> EnvioDTO:
    envio, terrestre, maritimo = obtener_envio(db, envio_id)
    tipo_envio: TipoEnvio = "TERRESTRE" if terrestre is not None else "MARITIMO"
    return EnvioDTO(**{
        "id_envio": envio.id_envio,
        "id_cliente": envio.id_cliente,
        "id_tipo_producto": envio.id_tipo_producto,
        "cantidad": envio.cantidad,
        "fecha_registro": envio.fecha_registro,
        "fecha_entrega": envio.fecha_entrega,
        "precio_base": envio.precio_base,
        "descuento": envio.descuento,
        "precio_final": envio.precio_final,
        "numero_guia": envio.numero_guia,
        "tipo_envio": tipo_envio,
        "id_bodega": terrestre.id_bodega if terrestre is not None else None,
        "placa_vehiculo": terrestre.placa_vehiculo if terrestre is not None else None,
        "id_puerto": maritimo.id_puerto if maritimo is not None else None,
        "numero_flota": maritimo.numero_flota if maritimo is not None else None,
    })


@router.patch("/envios/{envio_id}", response_model=EnvioDTO)
def actualizar(envio_id: int, dto: ActualizarEnvioDTO, db: DBSession, _: dict = Depends(obtener_usuario_actual)) -> EnvioDTO:
    envio, terrestre, maritimo = actualizar_envio(db, envio_id, dto)
    tipo_envio: TipoEnvio = "TERRESTRE" if terrestre is not None else "MARITIMO"
    return EnvioDTO(**{
        "id_envio": envio.id_envio,
        "id_cliente": envio.id_cliente,
        "id_tipo_producto": envio.id_tipo_producto,
        "cantidad": envio.cantidad,
        "fecha_registro": envio.fecha_registro,
        "fecha_entrega": envio.fecha_entrega,
        "precio_base": envio.precio_base,
        "descuento": envio.descuento,
        "precio_final": envio.precio_final,
        "numero_guia": envio.numero_guia,
        "tipo_envio": tipo_envio,
        "id_bodega": terrestre.id_bodega if terrestre is not None else None,
        "placa_vehiculo": terrestre.placa_vehiculo if terrestre is not None else None,
        "id_puerto": maritimo.id_puerto if maritimo is not None else None,
        "numero_flota": maritimo.numero_flota if maritimo is not None else None,
    })


@router.delete("/envios/{envio_id}")
def eliminar(envio_id: int, db: DBSession, _: dict = Depends(obtener_admin_actual)) -> dict:
    eliminar_envio(db, envio_id)
    return {"status": "ok"}
