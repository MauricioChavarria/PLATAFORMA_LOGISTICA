from __future__ import annotations

from fastapi import APIRouter

from app.comun.dependencias import DBSession
from app.usuarios.schemas import RegistrarUsuarioDTO, UsuarioDTO
from app.usuarios.service import registrar_usuario

router = APIRouter()


@router.post("/auth/register", response_model=UsuarioDTO, summary="Registrar usuario")
def register(dto: RegistrarUsuarioDTO, db: DBSession) -> UsuarioDTO:
    user = registrar_usuario(db, dto)
    return UsuarioDTO.model_validate(user, from_attributes=True)
