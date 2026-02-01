from pydantic import BaseModel, Field


class Paginacion(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)


class RespuestaPaginada(BaseModel):
    page: int
    page_size: int
    total: int
