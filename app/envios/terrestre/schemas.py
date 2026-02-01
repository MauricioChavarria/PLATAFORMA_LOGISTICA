from pydantic import BaseModel, Field

from app.comun.regex import FLOTA_RE, GUIA_RE, PLACA_RE


class CrearEnvioTerrestreDTO(BaseModel):
    guia: str = Field(pattern=GUIA_RE.pattern)
    cliente_id: int = Field(ge=1)

    placa_vehiculo: str = Field(pattern=PLACA_RE.pattern)
    codigo_flota: str = Field(pattern=FLOTA_RE.pattern)

    cantidad: int = Field(ge=1)


class EnvioTerrestreDTO(BaseModel):
    id: int
    guia: str
    cliente_id: int
    placa_vehiculo: str
    codigo_flota: str
    descuento: float
