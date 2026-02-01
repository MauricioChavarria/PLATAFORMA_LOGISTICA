from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.base_de_datos.base import Base


class Envio(Base):
    __tablename__ = "envio"

    id_envio: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_cliente: Mapped[int] = mapped_column(ForeignKey("cliente.id_cliente"), index=True)
    id_tipo_producto: Mapped[int] = mapped_column(ForeignKey("tipo_producto.id_tipo_producto"), index=True)

    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    fecha_registro: Mapped[date] = mapped_column(Date, nullable=False)
    fecha_entrega: Mapped[date] = mapped_column(Date, nullable=False)

    precio_base: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    descuento: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    precio_final: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    numero_guia: Mapped[str] = mapped_column(String(10), unique=True, index=True, nullable=False)


class EnvioTerrestre(Base):
    __tablename__ = "envio_terrestre"

    id_envio: Mapped[int] = mapped_column(ForeignKey("envio.id_envio"), primary_key=True)
    placa_vehiculo: Mapped[str] = mapped_column(String(6), nullable=False)
    id_bodega: Mapped[int] = mapped_column(ForeignKey("bodega.id_bodega"), index=True, nullable=False)


class EnvioMaritimo(Base):
    __tablename__ = "envio_maritimo"

    id_envio: Mapped[int] = mapped_column(ForeignKey("envio.id_envio"), primary_key=True)
    numero_flota: Mapped[str] = mapped_column(String(8), nullable=False)
    id_puerto: Mapped[int] = mapped_column(ForeignKey("puerto.id_puerto"), index=True, nullable=False)
