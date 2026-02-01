from datetime import datetime, timezone

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.puertos.models import Puerto


def _base_query() -> Select[tuple[Puerto]]:
    return select(Puerto).where(Puerto.eliminado_en.is_(None))


def crear(db: Session, *, nombre: str, pais: str) -> Puerto:
    obj = Puerto(nombre=nombre, pais=pais)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def obtener_por_id(db: Session, puerto_id: int) -> Puerto | None:
    return db.scalar(_base_query().where(Puerto.id == puerto_id))


def listar(
    db: Session,
    *,
    page: int,
    page_size: int,
    q: str | None = None,
    pais: str | None = None,
) -> tuple[list[Puerto], int]:
    query = _base_query()
    if q:
        like = f"%{q.strip()}%"
        query = query.where(Puerto.nombre.ilike(like))
    if pais:
        query = query.where(Puerto.pais == pais)

    total = db.scalar(select(func.count()).select_from(query.subquery())) or 0
    offset = (page - 1) * page_size
    items = db.scalars(query.order_by(Puerto.id.asc()).offset(offset).limit(page_size)).all()
    return items, int(total)


def actualizar(
    db: Session,
    puerto: Puerto,
    *,
    nombre: str | None = None,
    pais: str | None = None,
) -> Puerto:
    if nombre is not None:
        puerto.nombre = nombre
    if pais is not None:
        puerto.pais = pais

    db.add(puerto)
    db.commit()
    db.refresh(puerto)
    return puerto


def soft_delete(db: Session, puerto: Puerto) -> None:
    puerto.eliminado_en = datetime.now(timezone.utc)
    db.add(puerto)
    db.commit()
