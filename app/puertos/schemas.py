from datetime import datetime

from pydantic import BaseModel, Field


class CrearPuertoDTO(BaseModel):
    nombre: str = Field(min_length=2, max_length=160)
    pais: str = Field(min_length=2, max_length=120)


class ActualizarPuertoDTO(BaseModel):
    nombre: str | None = Field(default=None, min_length=2, max_length=160)
    pais: str | None = Field(default=None, min_length=2, max_length=120)


class PuertoDTO(BaseModel):
    id: int
    nombre: str
    pais: str
    creado_en: datetime


class ListaPuertosDTO(BaseModel):
    page: int
    page_size: int
    total: int
    items: list[PuertoDTO]
