from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.bodegas.models import Bodega


def _base_query() -> Select[tuple[Bodega]]:
    return select(Bodega)


def crear(db: Session, *, nombre: str, direccion: str | None) -> Bodega:
    obj = Bodega(nombre=nombre, direccion=direccion)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def obtener_por_id(db: Session, bodega_id: int) -> Bodega | None:
    return db.scalar(_base_query().where(Bodega.id_bodega == bodega_id))


def listar(
    db: Session,
    *,
    page: int,
    page_size: int,
    q: str | None = None,
) -> tuple[list[Bodega], int]:
    query = _base_query()
    if q:
        like = f"%{q.strip()}%"
        query = query.where(Bodega.nombre.ilike(like))

    total = db.scalar(select(func.count()).select_from(query.subquery())) or 0
    offset = (page - 1) * page_size
    items = db.scalars(query.order_by(Bodega.id_bodega.asc()).offset(offset).limit(page_size)).all()
    return items, int(total)


def actualizar(
    db: Session,
    bodega: Bodega,
    *,
    nombre: str | None = None,
    direccion: str | None = None,
) -> Bodega:
    if nombre is not None:
        bodega.nombre = nombre
    if direccion is not None:
        bodega.direccion = direccion

    db.add(bodega)
    db.commit()
    db.refresh(bodega)
    return bodega


def eliminar(db: Session, bodega: Bodega) -> None:
    db.delete(bodega)
    db.commit()
