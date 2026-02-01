from __future__ import annotations

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.usuarios.models import Usuario


def _base_query() -> Select[tuple[Usuario]]:
    return select(Usuario)


def obtener_por_username(db: Session, username: str) -> Usuario | None:
    return db.scalar(_base_query().where(Usuario.username == username))


def crear(db: Session, *, username: str, password_hash: str, role: str = "user") -> Usuario:
    obj = Usuario(username=username, password_hash=password_hash, role=role)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj
