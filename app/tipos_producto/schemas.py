from pydantic import BaseModel, Field


class CrearTipoProductoDTO(BaseModel):
    nombre: str = Field(min_length=1, max_length=50)


class ActualizarTipoProductoDTO(BaseModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=50)


class TipoProductoDTO(BaseModel):
    id_tipo_producto: int
    nombre: str


class ListaTiposProductoDTO(BaseModel):
    page: int
    page_size: int
    total: int
    items: list[TipoProductoDTO]
