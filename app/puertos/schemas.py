from pydantic import BaseModel, Field


class CrearPuertoDTO(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)
    ciudad: str | None = Field(default=None, max_length=100)


class ActualizarPuertoDTO(BaseModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=100)
    ciudad: str | None = Field(default=None, max_length=100)


class PuertoDTO(BaseModel):
    id_puerto: int
    nombre: str
    ciudad: str | None = None


class ListaPuertosDTO(BaseModel):
    page: int
    page_size: int
    total: int
    items: list[PuertoDTO]
