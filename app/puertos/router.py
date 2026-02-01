from fastapi import APIRouter, Depends, Query

from app.autenticacion.dependencies import obtener_usuario_actual
from app.comun.dependencias import DBSession
from app.puertos.schemas import ActualizarPuertoDTO, CrearPuertoDTO, ListaPuertosDTO, PuertoDTO
from app.puertos.service import (
    actualizar_puerto,
    crear_puerto,
    eliminar_puerto,
    listar_puertos,
    obtener_puerto,
)

router = APIRouter()


@router.post("/puertos", response_model=PuertoDTO)
def crear(dto: CrearPuertoDTO, db: DBSession, _: dict = Depends(obtener_usuario_actual)) -> PuertoDTO:
    obj = crear_puerto(db, dto)
    return PuertoDTO.model_validate(obj, from_attributes=True)


@router.get("/puertos", response_model=ListaPuertosDTO)
def listar(
    db: DBSession,
    _: dict = Depends(obtener_usuario_actual),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    q: str | None = Query(None, min_length=1),
    ciudad: str | None = None,
) -> ListaPuertosDTO:
    items, total = listar_puertos(db, page=page, page_size=page_size, q=q, ciudad=ciudad)
    return ListaPuertosDTO(
        page=page,
        page_size=page_size,
        total=total,
        items=[PuertoDTO.model_validate(o, from_attributes=True) for o in items],
    )


@router.get("/puertos/{puerto_id}", response_model=PuertoDTO)
def obtener(puerto_id: int, db: DBSession, _: dict = Depends(obtener_usuario_actual)) -> PuertoDTO:
    obj = obtener_puerto(db, puerto_id)
    return PuertoDTO.model_validate(obj, from_attributes=True)


@router.patch("/puertos/{puerto_id}", response_model=PuertoDTO)
def actualizar(
    puerto_id: int,
    dto: ActualizarPuertoDTO,
    db: DBSession,
    _: dict = Depends(obtener_usuario_actual),
) -> PuertoDTO:
    obj = actualizar_puerto(db, puerto_id, dto)
    return PuertoDTO.model_validate(obj, from_attributes=True)


@router.delete("/puertos/{puerto_id}")
def eliminar(puerto_id: int, db: DBSession, _: dict = Depends(obtener_usuario_actual)) -> dict:
    eliminar_puerto(db, puerto_id)
    return {"status": "ok"}
