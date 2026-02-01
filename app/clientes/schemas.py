from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CrearClienteDTO(BaseModel):
    nombre: str = Field(min_length=2, max_length=120)
    email: EmailStr
    documento: str = Field(min_length=3, max_length=32)
    telefono: str | None = Field(default=None, max_length=32)


class ActualizarClienteDTO(BaseModel):
    nombre: str | None = Field(default=None, min_length=2, max_length=120)
    email: EmailStr | None = None
    documento: str | None = Field(default=None, min_length=3, max_length=32)
    telefono: str | None = Field(default=None, max_length=32)


class ClienteDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    email: EmailStr
    documento: str
    telefono: str | None = None
    creado_en: datetime


class ListaClientesDTO(BaseModel):
    page: int
    page_size: int
    total: int
    items: list[ClienteDTO]
