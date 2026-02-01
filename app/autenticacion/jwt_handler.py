from datetime import datetime, timedelta, timezone
from typing import Any

import jwt

from app.base_de_datos.configuracion import settings


def crear_token(payload: dict[str, Any], exp_minutes: int | None = None) -> str:
    now = datetime.now(tz=timezone.utc)
    exp = now + timedelta(minutes=exp_minutes or settings.jwt_exp_minutes)

    to_encode = {**payload, "iat": int(now.timestamp()), "exp": int(exp.timestamp())}
    return jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decodificar_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
