from __future__ import annotations

import re
from datetime import date
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field, model_validator

TipoEnvio = Literal["TERRESTRE", "MARITIMO"]


class CrearEnvioDTO(BaseModel):
    id_cliente: int
    id_tipo_producto: int

    cantidad: int = Field(gt=0)
    fecha_registro: date
    fecha_entrega: date
    precio_base: Decimal = Field(ge=0)
    numero_guia: str = Field(min_length=1, max_length=10)

    tipo_envio: TipoEnvio

    # Detalle terrestre
    placa_vehiculo: str | None = Field(default=None, min_length=6, max_length=6)
    id_bodega: int | None = None

    # Detalle marítimo
    numero_flota: str | None = Field(default=None, min_length=8, max_length=8)
    id_puerto: int | None = None

    @model_validator(mode="after")
    def validar(self) -> "CrearEnvioDTO":
        if self.fecha_entrega < self.fecha_registro:
            raise ValueError("fecha_entrega no puede ser anterior a fecha_registro")

        if self.tipo_envio == "TERRESTRE":
            if self.id_bodega is None or self.placa_vehiculo is None:
                raise ValueError("Para TERRESTRE se requiere id_bodega y placa_vehiculo")
            if self.id_puerto is not None or self.numero_flota is not None:
                raise ValueError("Campos marítimos no aplican para TERRESTRE")
            if not re.fullmatch(r"^[A-Z]{3}\d{3}$", self.placa_vehiculo):
                raise ValueError("placa_vehiculo inválida (ej: ABC123)")
            return self

        if self.id_puerto is None or self.numero_flota is None:
            raise ValueError("Para MARITIMO se requiere id_puerto y numero_flota")
        if self.id_bodega is not None or self.placa_vehiculo is not None:
            raise ValueError("Campos terrestres no aplican para MARITIMO")
        if not re.fullmatch(r"^[A-Z]{3}\d{4}[A-Z]$", self.numero_flota):
            raise ValueError("numero_flota inválido (ej: ABC1234Z)")
        return self


class ActualizarEnvioDTO(BaseModel):
    id_cliente: int | None = None
    id_tipo_producto: int | None = None
    cantidad: int | None = Field(default=None, gt=0)
    fecha_registro: date | None = None
    fecha_entrega: date | None = None
    precio_base: Decimal | None = Field(default=None, ge=0)
    numero_guia: str | None = Field(default=None, min_length=1, max_length=10)

    # Detalle terrestre
    placa_vehiculo: str | None = Field(default=None, min_length=6, max_length=6)
    id_bodega: int | None = None

    # Detalle marítimo
    numero_flota: str | None = Field(default=None, min_length=8, max_length=8)
    id_puerto: int | None = None

    @model_validator(mode="after")
    def validar_fechas(self) -> "ActualizarEnvioDTO":
        if self.fecha_registro is not None and self.fecha_entrega is not None:
            if self.fecha_entrega < self.fecha_registro:
                raise ValueError("fecha_entrega no puede ser anterior a fecha_registro")
        if self.placa_vehiculo is not None and not re.fullmatch(r"^[A-Z]{3}\d{3}$", self.placa_vehiculo):
            raise ValueError("placa_vehiculo inválida (ej: ABC123)")
        if self.numero_flota is not None and not re.fullmatch(r"^[A-Z]{3}\d{4}[A-Z]$", self.numero_flota):
            raise ValueError("numero_flota inválido (ej: ABC1234Z)")
        return self


class EnvioDTO(BaseModel):
    id_envio: int
    id_cliente: int
    id_tipo_producto: int
    cantidad: int
    fecha_registro: date
    fecha_entrega: date
    precio_base: Decimal
    descuento: Decimal
    precio_final: Decimal
    numero_guia: str
    tipo_envio: TipoEnvio

    id_bodega: int | None = None
    placa_vehiculo: str | None = None

    id_puerto: int | None = None
    numero_flota: str | None = None


class ListaEnviosDTO(BaseModel):
    page: int
    page_size: int
    total: int
    items: list[EnvioDTO]
