from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.clientes.models import Cliente


def _base_query() -> Select[tuple[Cliente]]:
    return select(Cliente).where(Cliente.activo.is_(True))


def crear(db: Session, *, nombre: str, email: str | None = None, telefono: str | None = None) -> Cliente:
    obj = Cliente(nombre=nombre, email=email, telefono=telefono)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def obtener_por_id(db: Session, cliente_id: int) -> Cliente | None:
    return db.scalar(_base_query().where(Cliente.id_cliente == cliente_id))


def listar(
    db: Session,
    *,
    page: int,
    page_size: int,
    q: str | None = None,
    email: str | None = None,
) -> tuple[list[Cliente], int]:
    query = _base_query()

    if q:
        like = f"%{q.strip()}%"
        query = query.where(Cliente.nombre.ilike(like))
    if email:
        query = query.where(Cliente.email == email)

    total = db.scalar(select(func.count()).select_from(query.subquery())) or 0

    offset = (page - 1) * page_size
    items = db.scalars(query.order_by(Cliente.id_cliente.asc()).offset(offset).limit(page_size)).all()
    return items, int(total)


def actualizar(
    db: Session,
    cliente: Cliente,
    *,
    nombre: str | None = None,
    email: str | None = None,
    telefono: str | None = None,
) -> Cliente:
    if nombre is not None:
        cliente.nombre = nombre
    if email is not None:
        cliente.email = email
    if telefono is not None:
        cliente.telefono = telefono

    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente


def eliminar(db: Session, cliente: Cliente) -> None:
    cliente.activo = False
    db.add(cliente)
    db.commit()
