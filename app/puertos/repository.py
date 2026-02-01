from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.puertos.models import Puerto


def _base_query() -> Select[tuple[Puerto]]:
    return select(Puerto)


def crear(db: Session, *, nombre: str, ciudad: str | None) -> Puerto:
    obj = Puerto(nombre=nombre, ciudad=ciudad)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def obtener_por_id(db: Session, puerto_id: int) -> Puerto | None:
    return db.scalar(_base_query().where(Puerto.id_puerto == puerto_id))


def listar(
    db: Session,
    *,
    page: int,
    page_size: int,
    q: str | None = None,
    ciudad: str | None = None,
) -> tuple[list[Puerto], int]:
    query = _base_query()
    if q:
        like = f"%{q.strip()}%"
        query = query.where(Puerto.nombre.ilike(like))
    if ciudad:
        query = query.where(Puerto.ciudad == ciudad)

    total = db.scalar(select(func.count()).select_from(query.subquery())) or 0
    offset = (page - 1) * page_size
    items = db.scalars(query.order_by(Puerto.id_puerto.asc()).offset(offset).limit(page_size)).all()
    return items, int(total)


def actualizar(
    db: Session,
    puerto: Puerto,
    *,
    nombre: str | None = None,
    ciudad: str | None = None,
) -> Puerto:
    if nombre is not None:
        puerto.nombre = nombre
    if ciudad is not None:
        puerto.ciudad = ciudad

    db.add(puerto)
    db.commit()
    db.refresh(puerto)
    return puerto


def eliminar(db: Session, puerto: Puerto) -> None:
    db.delete(puerto)
    db.commit()
