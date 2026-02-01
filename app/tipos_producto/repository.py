from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.tipos_producto.models import TipoProducto


def _base_query() -> Select[tuple[TipoProducto]]:
    return select(TipoProducto)


def crear(db: Session, *, nombre: str) -> TipoProducto:
    obj = TipoProducto(nombre=nombre)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def obtener_por_id(db: Session, tipo_producto_id: int) -> TipoProducto | None:
    return db.scalar(_base_query().where(TipoProducto.id_tipo_producto == tipo_producto_id))


def listar(
    db: Session,
    *,
    page: int,
    page_size: int,
    q: str | None = None,
) -> tuple[list[TipoProducto], int]:
    query = _base_query()
    if q:
        like = f"%{q.strip()}%"
        query = query.where(TipoProducto.nombre.ilike(like))

    total = db.scalar(select(func.count()).select_from(query.subquery())) or 0
    offset = (page - 1) * page_size
    items = db.scalars(query.order_by(TipoProducto.id_tipo_producto.asc()).offset(offset).limit(page_size)).all()
    return items, int(total)


def actualizar(db: Session, obj: TipoProducto, *, nombre: str | None = None) -> TipoProducto:
    if nombre is not None:
        obj.nombre = nombre

    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def eliminar(db: Session, obj: TipoProducto) -> None:
    db.delete(obj)
    db.commit()
