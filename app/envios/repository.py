from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.envios.base.models import EnvioBase, EnvioMaritimo, EnvioTerrestre


def _base_query() -> Select[tuple[EnvioBase]]:
    return select(EnvioBase).where(EnvioBase.eliminado_en.is_(None))


def crear_terrestre(
    db: Session,
    *,
    cliente_id: int,
    producto_id: int,
    cantidad: int,
    fecha_registro,
    fecha_entrega,
    precio_base: Decimal,
    descuento: Decimal,
    precio_final: Decimal,
    numero_guia: str,
    bodega_id: int,
    placa_vehiculo: str,
) -> tuple[EnvioBase, EnvioTerrestre]:
    envio = EnvioBase(
        cliente_id=cliente_id,
        producto_id=producto_id,
        cantidad=cantidad,
        fecha_registro=fecha_registro,
        fecha_entrega=fecha_entrega,
        precio_base=precio_base,
        descuento=descuento,
        precio_final=precio_final,
        numero_guia=numero_guia,
        tipo_envio="TERRESTRE",
    )
    db.add(envio)
    db.flush()  # obtiene envio.id

    detalle = EnvioTerrestre(envio_id=envio.id, bodega_id=bodega_id, placa_vehiculo=placa_vehiculo)
    db.add(detalle)
    db.commit()
    db.refresh(envio)
    db.refresh(detalle)
    return envio, detalle


def crear_maritimo(
    db: Session,
    *,
    cliente_id: int,
    producto_id: int,
    cantidad: int,
    fecha_registro,
    fecha_entrega,
    precio_base: Decimal,
    descuento: Decimal,
    precio_final: Decimal,
    numero_guia: str,
    puerto_id: int,
    numero_flota: str,
) -> tuple[EnvioBase, EnvioMaritimo]:
    envio = EnvioBase(
        cliente_id=cliente_id,
        producto_id=producto_id,
        cantidad=cantidad,
        fecha_registro=fecha_registro,
        fecha_entrega=fecha_entrega,
        precio_base=precio_base,
        descuento=descuento,
        precio_final=precio_final,
        numero_guia=numero_guia,
        tipo_envio="MARITIMO",
    )
    db.add(envio)
    db.flush()

    detalle = EnvioMaritimo(envio_id=envio.id, puerto_id=puerto_id, numero_flota=numero_flota)
    db.add(detalle)
    db.commit()
    db.refresh(envio)
    db.refresh(detalle)
    return envio, detalle


def obtener_por_id(
    db: Session,
    envio_id: int,
) -> tuple[EnvioBase, EnvioTerrestre | None, EnvioMaritimo | None] | None:
    query = (
        _base_query()
        .where(EnvioBase.id == envio_id)
        .outerjoin(EnvioTerrestre, EnvioTerrestre.envio_id == EnvioBase.id)
        .outerjoin(EnvioMaritimo, EnvioMaritimo.envio_id == EnvioBase.id)
        .with_only_columns(EnvioBase, EnvioTerrestre, EnvioMaritimo)
    )

    row = db.execute(query).first()
    if row is None:
        return None

    envio, terrestre, maritimo = row
    return envio, terrestre, maritimo


def listar(
    db: Session,
    *,
    page: int,
    page_size: int,
    q: str | None = None,
    cliente_id: int | None = None,
    producto_id: int | None = None,
    tipo_envio: str | None = None,
) -> tuple[list[tuple[EnvioBase, EnvioTerrestre | None, EnvioMaritimo | None]], int]:
    base = _base_query()

    if q:
        like = f"%{q.strip()}%"
        base = base.where(EnvioBase.numero_guia.ilike(like))
    if cliente_id is not None:
        base = base.where(EnvioBase.cliente_id == cliente_id)
    if producto_id is not None:
        base = base.where(EnvioBase.producto_id == producto_id)
    if tipo_envio is not None:
        base = base.where(EnvioBase.tipo_envio == tipo_envio)

    total = db.scalar(select(func.count()).select_from(base.subquery())) or 0

    offset = (page - 1) * page_size

    query = (
        base.order_by(EnvioBase.id.asc())
        .offset(offset)
        .limit(page_size)
        .outerjoin(EnvioTerrestre, EnvioTerrestre.envio_id == EnvioBase.id)
        .outerjoin(EnvioMaritimo, EnvioMaritimo.envio_id == EnvioBase.id)
        .with_only_columns(EnvioBase, EnvioTerrestre, EnvioMaritimo)
    )

    rows = db.execute(query).all()
    items = [(r[0], r[1], r[2]) for r in rows]
    return items, int(total)


def actualizar_base(
    db: Session,
    envio: EnvioBase,
    *,
    cantidad: int | None = None,
    fecha_registro=None,
    fecha_entrega=None,
    precio_base: Decimal | None = None,
    descuento: Decimal | None = None,
    precio_final: Decimal | None = None,
    numero_guia: str | None = None,
) -> EnvioBase:
    if cantidad is not None:
        envio.cantidad = cantidad
    if fecha_registro is not None:
        envio.fecha_registro = fecha_registro
    if fecha_entrega is not None:
        envio.fecha_entrega = fecha_entrega

    if precio_base is not None:
        envio.precio_base = precio_base
    if descuento is not None:
        envio.descuento = descuento
    if precio_final is not None:
        envio.precio_final = precio_final

    if numero_guia is not None:
        envio.numero_guia = numero_guia

    db.add(envio)
    db.commit()
    db.refresh(envio)
    return envio


def actualizar_terrestre(
    db: Session,
    detalle: EnvioTerrestre,
    *,
    bodega_id: int | None = None,
    placa_vehiculo: str | None = None,
) -> EnvioTerrestre:
    if bodega_id is not None:
        detalle.bodega_id = bodega_id
    if placa_vehiculo is not None:
        detalle.placa_vehiculo = placa_vehiculo

    db.add(detalle)
    db.commit()
    db.refresh(detalle)
    return detalle


def actualizar_maritimo(
    db: Session,
    detalle: EnvioMaritimo,
    *,
    puerto_id: int | None = None,
    numero_flota: str | None = None,
) -> EnvioMaritimo:
    if puerto_id is not None:
        detalle.puerto_id = puerto_id
    if numero_flota is not None:
        detalle.numero_flota = numero_flota

    db.add(detalle)
    db.commit()
    db.refresh(detalle)
    return detalle


def soft_delete(db: Session, envio: EnvioBase) -> None:
    envio.eliminado_en = datetime.now(timezone.utc)
    db.add(envio)
    db.commit()
