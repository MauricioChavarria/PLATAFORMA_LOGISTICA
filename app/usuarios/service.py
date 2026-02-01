from __future__ import annotations

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.comun.excepciones import conflicto, error_servidor
from app.usuarios import repository
from app.usuarios.passwords import hash_password, verify_password
from app.usuarios.schemas import RegistrarUsuarioDTO


def registrar_usuario(db: Session, dto: RegistrarUsuarioDTO):
    password_hash = hash_password(dto.password)
    try:
        return repository.crear(db, username=dto.username, password_hash=password_hash, role="user")
    except IntegrityError as exc:
        db.rollback()
        raise conflicto("Usuario ya existe") from exc
    except SQLAlchemyError as exc:
        db.rollback()
        raise error_servidor(
            "Error registrando usuario. Verifica la base de datos y migraciones (alembic upgrade head)."
        ) from exc


def validar_credenciales(db: Session, username: str, password: str):
    user = repository.obtener_por_username(db, username)
    if user is None:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user
