from __future__ import annotations

from pydantic import BaseModel, Field


class RegistrarUsuarioDTO(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=200)


class UsuarioDTO(BaseModel):
    id_usuario: int
    username: str
    role: str
