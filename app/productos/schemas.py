from datetime import datetime

from pydantic import BaseModel, Field


class CrearProductoDTO(BaseModel):
    nombre: str = Field(min_length=2, max_length=160)
    descripcion: str | None = Field(default=None, max_length=500)


class ActualizarProductoDTO(BaseModel):
    nombre: str | None = Field(default=None, min_length=2, max_length=160)
    descripcion: str | None = Field(default=None, max_length=500)


class ProductoDTO(BaseModel):
    id: int
    nombre: str
    descripcion: str | None = None
    creado_en: datetime


class ListaProductosDTO(BaseModel):
    page: int
    page_size: int
    total: int
    items: list[ProductoDTO]
