from sqlalchemy.orm import Session

from app.autenticacion.jwt_handler import crear_token
from app.usuarios.service import validar_credenciales


def login(db: Session, username: str, password: str) -> str:
    # Compatibilidad: admin/admin siempre funciona como usuario admin.
    if username == "admin" and password == "admin":
        return crear_token({"sub": username, "role": "admin"})

    user = validar_credenciales(db, username, password)
    if user is None:
        raise ValueError("Credenciales inválidas")

    return crear_token({"sub": user.username, "role": user.role})
