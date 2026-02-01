from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.clientes import repository
from app.clientes.schemas import ActualizarClienteDTO, CrearClienteDTO
from app.comun.excepciones import conflicto, no_encontrado
from app.envios.base.models import Envio


def crear_cliente(db: Session, dto: CrearClienteDTO):
    return repository.crear(
        db,
        nombre=dto.nombre,
        email=str(dto.email) if dto.email is not None else None,
        telefono=dto.telefono,
    )


def obtener_cliente(db: Session, cliente_id: int):
    obj = repository.obtener_por_id(db, cliente_id)
    if obj is None:
        raise no_encontrado("Cliente no encontrado")
    return obj


def listar_clientes(
    db: Session,
    *,
    page: int,
    page_size: int,
    q: str | None = None,
    email: str | None = None,
):
    return repository.listar(
        db,
        page=page,
        page_size=page_size,
        q=q,
        email=email,
    )


def actualizar_cliente(db: Session, cliente_id: int, dto: ActualizarClienteDTO):
    obj = obtener_cliente(db, cliente_id)
    return repository.actualizar(
        db,
        obj,
        nombre=dto.nombre,
        email=str(dto.email) if dto.email is not None else None,
        telefono=dto.telefono,
    )


def eliminar_cliente(db: Session, cliente_id: int) -> None:
    obj = obtener_cliente(db, cliente_id)

    total_envios = db.scalar(select(func.count()).select_from(Envio).where(Envio.id_cliente == cliente_id)) or 0
    if int(total_envios) > 0:
        raise conflicto("No se puede eliminar el cliente: tiene envíos asociados")

    try:
        repository.eliminar(db, obj)
    except IntegrityError as exc:
        db.rollback()
        raise conflicto("No se puede eliminar el cliente: tiene envíos asociados") from exc
