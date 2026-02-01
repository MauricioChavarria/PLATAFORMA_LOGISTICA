from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CrearClienteDTO(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)
    email: EmailStr | None = None
    telefono: str | None = Field(default=None, max_length=20)


class ActualizarClienteDTO(BaseModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=100)
    email: EmailStr | None = None
    telefono: str | None = Field(default=None, max_length=20)


class ClienteDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_cliente: int
    nombre: str
    email: EmailStr | None = None
    telefono: str | None = None


class ListaClientesDTO(BaseModel):
    page: int
    page_size: int
    total: int
    items: list[ClienteDTO]
