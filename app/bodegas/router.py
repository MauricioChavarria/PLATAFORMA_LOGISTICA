from fastapi import APIRouter, Depends, Query

from app.autenticacion.dependencies import obtener_admin_actual, obtener_usuario_actual
from app.bodegas.schemas import ActualizarBodegaDTO, BodegaDTO, CrearBodegaDTO, ListaBodegasDTO
from app.bodegas.service import (
    actualizar_bodega,
    crear_bodega,
    eliminar_bodega,
    listar_bodegas,
    obtener_bodega,
)
from app.comun.dependencias import DBSession

router = APIRouter()


@router.post("/bodegas", response_model=BodegaDTO)
def crear(dto: CrearBodegaDTO, db: DBSession, _: dict = Depends(obtener_admin_actual)) -> BodegaDTO:
    obj = crear_bodega(db, dto)
    return BodegaDTO.model_validate(obj, from_attributes=True)


@router.get("/bodegas", response_model=ListaBodegasDTO)
def listar(
    db: DBSession,
    _: dict = Depends(obtener_usuario_actual),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    q: str | None = Query(None, min_length=1),
) -> ListaBodegasDTO:
    items, total = listar_bodegas(db, page=page, page_size=page_size, q=q)
    return ListaBodegasDTO(
        page=page,
        page_size=page_size,
        total=total,
        items=[BodegaDTO.model_validate(o, from_attributes=True) for o in items],
    )


@router.get("/bodegas/{bodega_id}", response_model=BodegaDTO)
def obtener(bodega_id: int, db: DBSession, _: dict = Depends(obtener_usuario_actual)) -> BodegaDTO:
    obj = obtener_bodega(db, bodega_id)
    return BodegaDTO.model_validate(obj, from_attributes=True)


@router.patch("/bodegas/{bodega_id}", response_model=BodegaDTO)
def actualizar(
    bodega_id: int,
    dto: ActualizarBodegaDTO,
    db: DBSession,
    _: dict = Depends(obtener_admin_actual),
) -> BodegaDTO:
    obj = actualizar_bodega(db, bodega_id, dto)
    return BodegaDTO.model_validate(obj, from_attributes=True)


@router.delete("/bodegas/{bodega_id}")
def eliminar(bodega_id: int, db: DBSession, _: dict = Depends(obtener_admin_actual)) -> dict:
    eliminar_bodega(db, bodega_id)
    return {"status": "ok"}
