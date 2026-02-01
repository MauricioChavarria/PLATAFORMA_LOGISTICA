from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field, model_validator

TipoEnvio = Literal["TERRESTRE", "MARITIMO"]


class CrearEnvioDTO(BaseModel):
    cliente_id: int
    producto_id: int

    cantidad: int = Field(ge=1)
    fecha_registro: date
    fecha_entrega: date

    precio_base: Decimal = Field(ge=0)
    descuento: Decimal = Field(ge=0)

    numero_guia: str = Field(min_length=3, max_length=64)
    tipo_envio: TipoEnvio

    # Detalle terrestre
    bodega_id: int | None = None
    placa_vehiculo: str | None = Field(default=None, min_length=3, max_length=32)

    # Detalle marítimo
    puerto_id: int | None = None
    numero_flota: str | None = Field(default=None, min_length=1, max_length=32)

    @staticmethod
    def _validar_terrestre(dto: "CrearEnvioDTO") -> None:
        if dto.bodega_id is None or dto.placa_vehiculo is None:
            raise ValueError("Para TERRESTRE se requiere bodega_id y placa_vehiculo")
        if dto.puerto_id is not None or dto.numero_flota is not None:
            raise ValueError("Campos marítimos no aplican para TERRESTRE")

    @staticmethod
    def _validar_maritimo(dto: "CrearEnvioDTO") -> None:
        if dto.puerto_id is None or dto.numero_flota is None:
            raise ValueError("Para MARITIMO se requiere puerto_id y numero_flota")
        if dto.bodega_id is not None or dto.placa_vehiculo is not None:
            raise ValueError("Campos terrestres no aplican para MARITIMO")

    @model_validator(mode="after")
    def validar_detalle(self) -> "CrearEnvioDTO":
        if self.fecha_entrega < self.fecha_registro:
            raise ValueError("fecha_entrega no puede ser anterior a fecha_registro")
        if self.descuento > self.precio_base:
            raise ValueError("descuento no puede ser mayor a precio_base")

        if self.tipo_envio == "TERRESTRE":
            self._validar_terrestre(self)
            return self

        self._validar_maritimo(self)
        return self


class ActualizarEnvioDTO(BaseModel):
    cantidad: int | None = Field(default=None, ge=1)
    fecha_registro: date | None = None
    fecha_entrega: date | None = None

    precio_base: Decimal | None = Field(default=None, ge=0)
    descuento: Decimal | None = Field(default=None, ge=0)

    numero_guia: str | None = Field(default=None, min_length=3, max_length=64)
    tipo_envio: TipoEnvio | None = None

    # Detalle terrestre
    bodega_id: int | None = None
    placa_vehiculo: str | None = Field(default=None, min_length=3, max_length=32)

    # Detalle marítimo
    puerto_id: int | None = None
    numero_flota: str | None = Field(default=None, min_length=1, max_length=32)

    @model_validator(mode="after")
    def validar_fechas_y_descuento(self) -> "ActualizarEnvioDTO":
        if self.precio_base is not None and self.descuento is not None:
            if self.descuento > self.precio_base:
                raise ValueError("descuento no puede ser mayor a precio_base")

        if self.fecha_registro is not None and self.fecha_entrega is not None:
            if self.fecha_entrega < self.fecha_registro:
                raise ValueError("fecha_entrega no puede ser anterior a fecha_registro")

        return self


class EnvioDTO(BaseModel):
    id: int
    cliente_id: int
    producto_id: int

    cantidad: int
    fecha_registro: date
    fecha_entrega: date

    precio_base: Decimal
    descuento: Decimal
    precio_final: Decimal

    numero_guia: str
    tipo_envio: TipoEnvio

    bodega_id: int | None = None
    placa_vehiculo: str | None = None

    puerto_id: int | None = None
    numero_flota: str | None = None

    creado_en: datetime


class ListaEnviosDTO(BaseModel):
    page: int
    page_size: int
    total: int
    items: list[EnvioDTO]
