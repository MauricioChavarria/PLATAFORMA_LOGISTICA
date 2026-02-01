from datetime import datetime, timezone

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.bodegas.models import Bodega


def _base_query() -> Select[tuple[Bodega]]:
    return select(Bodega).where(Bodega.eliminado_en.is_(None))


def crear(db: Session, *, nombre: str, ubicacion: str, pais: str) -> Bodega:
    obj = Bodega(nombre=nombre, ubicacion=ubicacion, pais=pais)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def obtener_por_id(db: Session, bodega_id: int) -> Bodega | None:
    return db.scalar(_base_query().where(Bodega.id == bodega_id))


def listar(
    db: Session,
    *,
    page: int,
    page_size: int,
    q: str | None = None,
    pais: str | None = None,
) -> tuple[list[Bodega], int]:
    query = _base_query()
    if q:
        like = f"%{q.strip()}%"
        query = query.where(Bodega.nombre.ilike(like))
    if pais:
        query = query.where(Bodega.pais == pais)

    total = db.scalar(select(func.count()).select_from(query.subquery())) or 0
    offset = (page - 1) * page_size
    items = db.scalars(query.order_by(Bodega.id.asc()).offset(offset).limit(page_size)).all()
    return items, int(total)


def actualizar(
    db: Session,
    bodega: Bodega,
    *,
    nombre: str | None = None,
    ubicacion: str | None = None,
    pais: str | None = None,
) -> Bodega:
    if nombre is not None:
        bodega.nombre = nombre
    if ubicacion is not None:
        bodega.ubicacion = ubicacion
    if pais is not None:
        bodega.pais = pais

    db.add(bodega)
    db.commit()
    db.refresh(bodega)
    return bodega


def soft_delete(db: Session, bodega: Bodega) -> None:
    bodega.eliminado_en = datetime.now(timezone.utc)
    db.add(bodega)
    db.commit()
