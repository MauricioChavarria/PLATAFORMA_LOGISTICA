from fastapi import APIRouter, Depends, Query

from app.autenticacion.dependencies import obtener_admin_actual, obtener_usuario_actual
from app.clientes.schemas import ActualizarClienteDTO, ClienteDTO, CrearClienteDTO, ListaClientesDTO
from app.clientes.service import (
    actualizar_cliente,
    crear_cliente,
    eliminar_cliente,
    listar_clientes,
    obtener_cliente,
)
from app.comun.dependencias import DBSession

router = APIRouter()


@router.post("/clientes", response_model=ClienteDTO)
def crear(dto: CrearClienteDTO, db: DBSession, _: dict = Depends(obtener_usuario_actual)) -> ClienteDTO:
    obj = crear_cliente(db, dto)
    return ClienteDTO.model_validate(obj, from_attributes=True)


@router.get("/clientes", response_model=ListaClientesDTO)
def listar(
    db: DBSession,
    _: dict = Depends(obtener_usuario_actual),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    q: str | None = Query(None, min_length=1),
    email: str | None = None,
) -> ListaClientesDTO:
    items, total = listar_clientes(db, page=page, page_size=page_size, q=q, email=email)
    return ListaClientesDTO(
        page=page,
        page_size=page_size,
        total=total,
        items=[ClienteDTO.model_validate(o, from_attributes=True) for o in items],
    )


@router.get("/clientes/{cliente_id}", response_model=ClienteDTO)
def obtener(cliente_id: int, db: DBSession, _: dict = Depends(obtener_usuario_actual)) -> ClienteDTO:
    obj = obtener_cliente(db, cliente_id)
    return ClienteDTO.model_validate(obj, from_attributes=True)


@router.patch("/clientes/{cliente_id}", response_model=ClienteDTO)
def actualizar(
    cliente_id: int,
    dto: ActualizarClienteDTO,
    db: DBSession,
    _: dict = Depends(obtener_usuario_actual),
) -> ClienteDTO:
    obj = actualizar_cliente(db, cliente_id, dto)
    return ClienteDTO.model_validate(obj, from_attributes=True)


@router.delete("/clientes/{cliente_id}")
def eliminar(cliente_id: int, db: DBSession, _: dict = Depends(obtener_admin_actual)) -> dict:
    eliminar_cliente(db, cliente_id)
    return {"status": "ok"}