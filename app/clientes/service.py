from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.clientes import repository
from app.clientes.schemas import ActualizarClienteDTO, CrearClienteDTO
from app.comun.excepciones import conflicto, no_encontrado


def crear_cliente(db: Session, dto: CrearClienteDTO):
    try:
        return repository.crear(
            db,
            nombre=dto.nombre,
            email=str(dto.email),
            documento=dto.documento,
            telefono=dto.telefono,
        )
    except IntegrityError as exc:
        raise conflicto("Cliente ya existe (email o documento duplicado)") from exc


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
    documento: str | None = None,
):
    return repository.listar(
        db,
        page=page,
        page_size=page_size,
        q=q,
        email=email,
        documento=documento,
    )


def actualizar_cliente(db: Session, cliente_id: int, dto: ActualizarClienteDTO):
    obj = obtener_cliente(db, cliente_id)
    try:
        return repository.actualizar(
            db,
            obj,
            nombre=dto.nombre,
            email=str(dto.email) if dto.email is not None else None,
            documento=dto.documento,
            telefono=dto.telefono,
        )
    except IntegrityError as exc:
        raise conflicto("No se pudo actualizar (email o documento duplicado)") from exc


def eliminar_cliente(db: Session, cliente_id: int) -> None:
    obj = obtener_cliente(db, cliente_id)
    repository.soft_delete(db, obj)
