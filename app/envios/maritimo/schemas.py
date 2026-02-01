from pydantic import BaseModel, Field

from app.comun.regex import GUIA_RE


class CrearEnvioMaritimoDTO(BaseModel):
    guia: str = Field(pattern=GUIA_RE.pattern)
    cliente_id: int = Field(ge=1)

    puerto_origen_id: int = Field(ge=1)
    puerto_destino_id: int = Field(ge=1)

    cantidad: int = Field(ge=1)


class EnvioMaritimoDTO(BaseModel):
    id: int
    guia: str
    cliente_id: int
    puerto_origen_id: int
    puerto_destino_id: int
    descuento: float
