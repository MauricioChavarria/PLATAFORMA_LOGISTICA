from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.autenticacion.service import login
from app.autenticacion.dependencies import obtener_usuario_actual
from app.comun.excepciones import no_autorizado
from app.comun.dependencias import DBSession

router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/auth/token", response_model=TokenResponse)
def token(body: LoginRequest, db: DBSession) -> TokenResponse:
    try:
        token_str = login(db, body.username, body.password)
    except ValueError as exc:
        raise no_autorizado(str(exc)) from exc

    return TokenResponse(access_token=token_str)


@router.get("/auth/me", summary="Usuario actual")
def me(user: dict = Depends(obtener_usuario_actual)) -> dict:
    return user
