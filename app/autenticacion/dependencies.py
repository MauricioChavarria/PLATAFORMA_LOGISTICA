from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.autenticacion.jwt_handler import decodificar_token
from app.comun.excepciones import no_autorizado, prohibido

bearer = HTTPBearer(auto_error=False)


def obtener_usuario_actual(
    cred: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)],
) -> dict:
    if cred is None or not cred.credentials:
        raise no_autorizado("Falta token Bearer")

    try:
        payload = decodificar_token(cred.credentials)
    except Exception as exc:
        raise no_autorizado("Token inválido") from exc

    # En un proyecto real, aquí se validaría contra BD.
    return {"sub": payload.get("sub"), "role": payload.get("role")}


def obtener_admin_actual(user: Annotated[dict, Depends(obtener_usuario_actual)]) -> dict:
    if user.get("role") != "admin":
        raise prohibido("Se requiere rol admin")
    return user
