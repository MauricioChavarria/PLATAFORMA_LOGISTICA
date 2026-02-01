from datetime import datetime

from pydantic import BaseModel, Field


class CrearBodegaDTO(BaseModel):
    nombre: str = Field(min_length=2, max_length=160)
    ubicacion: str = Field(min_length=2, max_length=255)
    pais: str = Field(min_length=2, max_length=120)


class ActualizarBodegaDTO(BaseModel):
    nombre: str | None = Field(default=None, min_length=2, max_length=160)
    ubicacion: str | None = Field(default=None, min_length=2, max_length=255)
    pais: str | None = Field(default=None, min_length=2, max_length=120)


class BodegaDTO(BaseModel):
    id: int
    nombre: str
    ubicacion: str
    pais: str
    creado_en: datetime


class ListaBodegasDTO(BaseModel):
    page: int
    page_size: int
    total: int
    items: list[BodegaDTO]
