from __future__ import annotations

from decimal import Decimal

from sqlalchemy import Select, delete as sa_delete, func, select
from sqlalchemy.orm import Session

from app.envios.base.models import Envio, EnvioMaritimo, EnvioTerrestre


def _base_query() -> Select[tuple[Envio]]:
    return select(Envio)


def crear_terrestre(
    db: Session,
    *,
    id_cliente: int,
    id_tipo_producto: int,
    cantidad: int,
    fecha_registro,
    fecha_entrega,
    precio_base: Decimal,
    descuento: Decimal,
    precio_final: Decimal,
    numero_guia: str,
    id_bodega: int,
    placa_vehiculo: str,
) -> tuple[Envio, EnvioTerrestre]:
    envio = Envio(
        id_cliente=id_cliente,
        id_tipo_producto=id_tipo_producto,
        cantidad=cantidad,
        fecha_registro=fecha_registro,
        fecha_entrega=fecha_entrega,
        precio_base=precio_base,
        descuento=descuento,
        precio_final=precio_final,
        numero_guia=numero_guia,
    )
    db.add(envio)
    db.flush()  # obtiene envio.id_envio

    detalle = EnvioTerrestre(id_envio=envio.id_envio, id_bodega=id_bodega, placa_vehiculo=placa_vehiculo)
    db.add(detalle)
    db.commit()
    db.refresh(envio)
    db.refresh(detalle)
    return envio, detalle


def crear_maritimo(
    db: Session,
    *,
    id_cliente: int,
    id_tipo_producto: int,
    cantidad: int,
    fecha_registro,
    fecha_entrega,
    precio_base: Decimal,
    descuento: Decimal,
    precio_final: Decimal,
    numero_guia: str,
    id_puerto: int,
    numero_flota: str,
) -> tuple[Envio, EnvioMaritimo]:
    envio = Envio(
        id_cliente=id_cliente,
        id_tipo_producto=id_tipo_producto,
        cantidad=cantidad,
        fecha_registro=fecha_registro,
        fecha_entrega=fecha_entrega,
        precio_base=precio_base,
        descuento=descuento,
        precio_final=precio_final,
        numero_guia=numero_guia,
    )
    db.add(envio)
    db.flush()

    detalle = EnvioMaritimo(id_envio=envio.id_envio, id_puerto=id_puerto, numero_flota=numero_flota)
    db.add(detalle)
    db.commit()
    db.refresh(envio)
    db.refresh(detalle)
    return envio, detalle


def obtener_por_id(
    db: Session,
    envio_id: int,
) -> tuple[Envio, EnvioTerrestre | None, EnvioMaritimo | None] | None:
    query = (
        _base_query()
        .where(Envio.id_envio == envio_id)
        .outerjoin(EnvioTerrestre, EnvioTerrestre.id_envio == Envio.id_envio)
        .outerjoin(EnvioMaritimo, EnvioMaritimo.id_envio == Envio.id_envio)
        .with_only_columns(Envio, EnvioTerrestre, EnvioMaritimo)
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
    id_cliente: int | None = None,
    id_tipo_producto: int | None = None,
    tipo_envio: str | None = None,
) -> tuple[list[tuple[Envio, EnvioTerrestre | None, EnvioMaritimo | None]], int]:
    base = (
        _base_query()
        .outerjoin(EnvioTerrestre, EnvioTerrestre.id_envio == Envio.id_envio)
        .outerjoin(EnvioMaritimo, EnvioMaritimo.id_envio == Envio.id_envio)
    )

    if q:
        like = f"%{q.strip()}%"
        base = base.where(Envio.numero_guia.ilike(like))
    if id_cliente is not None:
        base = base.where(Envio.id_cliente == id_cliente)
    if id_tipo_producto is not None:
        base = base.where(Envio.id_tipo_producto == id_tipo_producto)

    if tipo_envio == "TERRESTRE":
        base = base.where(EnvioTerrestre.id_envio.is_not(None))
    elif tipo_envio == "MARITIMO":
        base = base.where(EnvioMaritimo.id_envio.is_not(None))

    total_subq = base.with_only_columns(Envio.id_envio).subquery()
    total = db.scalar(select(func.count()).select_from(total_subq)) or 0
    offset = (page - 1) * page_size

    query = (
        base.order_by(Envio.id_envio.asc())
        .offset(offset)
        .limit(page_size)
        .with_only_columns(Envio, EnvioTerrestre, EnvioMaritimo)
    )

    rows = db.execute(query).all()
    items = [(r[0], r[1], r[2]) for r in rows]
    return items, int(total)


def actualizar_base(
    db: Session,
    envio: Envio,
    *,
    id_cliente: int | None = None,
    id_tipo_producto: int | None = None,
    cantidad: int | None = None,
    fecha_registro=None,
    fecha_entrega=None,
    precio_base: Decimal | None = None,
    descuento: Decimal | None = None,
    precio_final: Decimal | None = None,
    numero_guia: str | None = None,
) -> Envio:
    if id_cliente is not None:
        envio.id_cliente = id_cliente
    if id_tipo_producto is not None:
        envio.id_tipo_producto = id_tipo_producto
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
    id_bodega: int | None = None,
    placa_vehiculo: str | None = None,
) -> EnvioTerrestre:
    if id_bodega is not None:
        detalle.id_bodega = id_bodega
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
    id_puerto: int | None = None,
    numero_flota: str | None = None,
) -> EnvioMaritimo:
    if id_puerto is not None:
        detalle.id_puerto = id_puerto
    if numero_flota is not None:
        detalle.numero_flota = numero_flota

    db.add(detalle)
    db.commit()
    db.refresh(detalle)
    return detalle


def eliminar(db: Session, envio: Envio) -> None:
    # Importante: en Postgres, sin relaciones ORM configuradas, SQLAlchemy puede
    # intentar borrar primero el padre y violar FKs. Forzamos orden con DELETEs.
    envio_id = envio.id_envio
    db.execute(sa_delete(EnvioTerrestre).where(EnvioTerrestre.id_envio == envio_id))
    db.execute(sa_delete(EnvioMaritimo).where(EnvioMaritimo.id_envio == envio_id))
    db.execute(sa_delete(Envio).where(Envio.id_envio == envio_id))
    db.commit()
