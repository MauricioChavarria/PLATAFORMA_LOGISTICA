from pydantic import BaseModel, Field


class CrearBodegaDTO(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)
    direccion: str | None = Field(default=None, max_length=200)


class ActualizarBodegaDTO(BaseModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=100)
    direccion: str | None = Field(default=None, max_length=200)


class BodegaDTO(BaseModel):
    id_bodega: int
    nombre: str
    direccion: str | None = None


class ListaBodegasDTO(BaseModel):
    page: int
    page_size: int
    total: int
    items: list[BodegaDTO]
