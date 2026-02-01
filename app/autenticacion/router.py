from fastapi import APIRouter
from pydantic import BaseModel

from app.autenticacion.service import login
from app.comun.excepciones import no_autorizado

router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/auth/token", response_model=TokenResponse)
def token(body: LoginRequest) -> TokenResponse:
    try:
        token_str = login(body.username, body.password)
    except ValueError as exc:
        raise no_autorizado(str(exc)) from exc

    return TokenResponse(access_token=token_str)
