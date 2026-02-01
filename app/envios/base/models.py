from __future__ import annotations

from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.base_de_datos.base import Base
from app.comun.modelos import SoftDeleteMixin


class EnvioBase(Base, SoftDeleteMixin):
    __tablename__ = "envios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    cliente_id: Mapped[int] = mapped_column(ForeignKey("clientes.id"), index=True)
    producto_id: Mapped[int] = mapped_column(ForeignKey("productos.id"), index=True)

    cantidad: Mapped[int] = mapped_column(Integer)
    fecha_registro: Mapped[date] = mapped_column(Date)
    fecha_entrega: Mapped[date] = mapped_column(Date)

    precio_base: Mapped[float] = mapped_column(Numeric(14, 2))
    descuento: Mapped[float] = mapped_column(Numeric(14, 2))
    precio_final: Mapped[float] = mapped_column(Numeric(14, 2))

    numero_guia: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    tipo_envio: Mapped[str] = mapped_column(String(20), index=True)  # TERRESTRE | MARITIMO


class EnvioTerrestre(Base):
    __tablename__ = "envios_terrestres"

    envio_id: Mapped[int] = mapped_column(ForeignKey("envios.id"), primary_key=True)
    bodega_id: Mapped[int] = mapped_column(ForeignKey("bodegas.id"), index=True)
    placa_vehiculo: Mapped[str] = mapped_column(String(32))


class EnvioMaritimo(Base):
    __tablename__ = "envios_maritimos"

    envio_id: Mapped[int] = mapped_column(ForeignKey("envios.id"), primary_key=True)
    puerto_id: Mapped[int] = mapped_column(ForeignKey("puertos.id"), index=True)
    numero_flota: Mapped[str] = mapped_column(String(32))
