from fastapi import APIRouter, Depends, Query

from app.autenticacion.dependencies import obtener_usuario_actual
from app.comun.dependencias import DBSession
from app.productos.schemas import ActualizarProductoDTO, CrearProductoDTO, ListaProductosDTO, ProductoDTO
from app.productos.service import (
    actualizar_producto,
    crear_producto,
    eliminar_producto,
    listar_productos,
    obtener_producto,
)

router = APIRouter()


@router.post("/productos", response_model=ProductoDTO)
def crear(dto: CrearProductoDTO, db: DBSession, _: dict = Depends(obtener_usuario_actual)) -> ProductoDTO:
    obj = crear_producto(db, dto)
    return ProductoDTO.model_validate(obj, from_attributes=True)


@router.get("/productos", response_model=ListaProductosDTO)
def listar(
    db: DBSession,
    _: dict = Depends(obtener_usuario_actual),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    q: str | None = Query(None, min_length=1),
) -> ListaProductosDTO:
    items, total = listar_productos(db, page=page, page_size=page_size, q=q)
    return ListaProductosDTO(
        page=page,
        page_size=page_size,
        total=total,
        items=[ProductoDTO.model_validate(o, from_attributes=True) for o in items],
    )


@router.get("/productos/{producto_id}", response_model=ProductoDTO)
def obtener(producto_id: int, db: DBSession, _: dict = Depends(obtener_usuario_actual)) -> ProductoDTO:
    obj = obtener_producto(db, producto_id)
    return ProductoDTO.model_validate(obj, from_attributes=True)


@router.patch("/productos/{producto_id}", response_model=ProductoDTO)
def actualizar(
    producto_id: int,
    dto: ActualizarProductoDTO,
    db: DBSession,
    _: dict = Depends(obtener_usuario_actual),
) -> ProductoDTO:
    obj = actualizar_producto(db, producto_id, dto)
    return ProductoDTO.model_validate(obj, from_attributes=True)


@router.delete("/productos/{producto_id}")
def eliminar(producto_id: int, db: DBSession, _: dict = Depends(obtener_usuario_actual)) -> dict:
    eliminar_producto(db, producto_id)
    return {"status": "ok"}
