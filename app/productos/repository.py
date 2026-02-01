from datetime import datetime, timezone

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.productos.models import Producto


def _base_query() -> Select[tuple[Producto]]:
    return select(Producto).where(Producto.eliminado_en.is_(None))


def crear(db: Session, *, nombre: str, descripcion: str | None = None) -> Producto:
    obj = Producto(nombre=nombre, descripcion=descripcion)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def obtener_por_id(db: Session, producto_id: int) -> Producto | None:
    return db.scalar(_base_query().where(Producto.id == producto_id))


def listar(
    db: Session,
    *,
    page: int,
    page_size: int,
    q: str | None = None,
) -> tuple[list[Producto], int]:
    query = _base_query()
    if q:
        like = f"%{q.strip()}%"
        query = query.where(Producto.nombre.ilike(like))

    total = db.scalar(select(func.count()).select_from(query.subquery())) or 0
    offset = (page - 1) * page_size
    items = db.scalars(query.order_by(Producto.id.asc()).offset(offset).limit(page_size)).all()
    return items, int(total)


def actualizar(
    db: Session,
    producto: Producto,
    *,
    nombre: str | None = None,
    descripcion: str | None = None,
) -> Producto:
    if nombre is not None:
        producto.nombre = nombre
    if descripcion is not None:
        producto.descripcion = descripcion

    db.add(producto)
    db.commit()
    db.refresh(producto)
    return producto


def soft_delete(db: Session, producto: Producto) -> None:
    producto.eliminado_en = datetime.now(timezone.utc)
    db.add(producto)
    db.commit()
