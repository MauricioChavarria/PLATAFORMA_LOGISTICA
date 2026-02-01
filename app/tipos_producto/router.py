from fastapi import APIRouter, Depends, Query

from app.autenticacion.dependencies import obtener_admin_actual, obtener_usuario_actual
from app.comun.dependencias import DBSession
from app.tipos_producto.schemas import (
    ActualizarTipoProductoDTO,
    CrearTipoProductoDTO,
    ListaTiposProductoDTO,
    TipoProductoDTO,
)
from app.tipos_producto.service import (
    actualizar_tipo_producto,
    crear_tipo_producto,
    eliminar_tipo_producto,
    listar_tipos_producto,
    obtener_tipo_producto,
)

router = APIRouter()


@router.post('/tipos-producto', response_model=TipoProductoDTO)
def crear(dto: CrearTipoProductoDTO, db: DBSession, _: dict = Depends(obtener_admin_actual)) -> TipoProductoDTO:
    obj = crear_tipo_producto(db, dto)
    return TipoProductoDTO.model_validate(obj, from_attributes=True)


@router.get('/tipos-producto', response_model=ListaTiposProductoDTO)
def listar(
    db: DBSession,
    _: dict = Depends(obtener_usuario_actual),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    q: str | None = Query(None, min_length=1),
) -> ListaTiposProductoDTO:
    items, total = listar_tipos_producto(db, page=page, page_size=page_size, q=q)
    return ListaTiposProductoDTO(
        page=page,
        page_size=page_size,
        total=total,
        items=[TipoProductoDTO.model_validate(o, from_attributes=True) for o in items],
    )


@router.get('/tipos-producto/{tipo_producto_id}', response_model=TipoProductoDTO)
def obtener(tipo_producto_id: int, db: DBSession, _: dict = Depends(obtener_usuario_actual)) -> TipoProductoDTO:
    obj = obtener_tipo_producto(db, tipo_producto_id)
    return TipoProductoDTO.model_validate(obj, from_attributes=True)


@router.patch('/tipos-producto/{tipo_producto_id}', response_model=TipoProductoDTO)
def actualizar(
    tipo_producto_id: int,
    dto: ActualizarTipoProductoDTO,
    db: DBSession,
    _: dict = Depends(obtener_admin_actual),
) -> TipoProductoDTO:
    obj = actualizar_tipo_producto(db, tipo_producto_id, dto)
    return TipoProductoDTO.model_validate(obj, from_attributes=True)


@router.delete('/tipos-producto/{tipo_producto_id}')
def eliminar(tipo_producto_id: int, db: DBSession, _: dict = Depends(obtener_admin_actual)) -> dict:
    eliminar_tipo_producto(db, tipo_producto_id)
    return {'status': 'ok'}
