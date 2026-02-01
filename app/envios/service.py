from __future__ import annotations

from decimal import Decimal

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.bodegas.service import obtener_bodega
from app.clientes.service import obtener_cliente
from app.comun.excepciones import conflicto, no_encontrado
from app.envios.base.discount_service import calcular_monto_descuento
from app.envios import repository
from app.envios.schemas import ActualizarEnvioDTO, CrearEnvioDTO, TipoEnvio
from app.puertos.service import obtener_puerto
from app.tipos_producto.service import obtener_tipo_producto


def _to_dto_dict(envio, terrestre, maritimo) -> dict:
    tipo_envio: TipoEnvio
    if terrestre is not None:
        tipo_envio = "TERRESTRE"
    elif maritimo is not None:
        tipo_envio = "MARITIMO"
    else:
        raise conflicto("Envío sin detalle terrestre/marítimo")

    data = {
        "id_envio": envio.id_envio,
        "id_cliente": envio.id_cliente,
        "id_tipo_producto": envio.id_tipo_producto,
        "cantidad": envio.cantidad,
        "fecha_registro": envio.fecha_registro,
        "fecha_entrega": envio.fecha_entrega,
        "precio_base": envio.precio_base,
        "descuento": envio.descuento,
        "precio_final": envio.precio_final,
        "numero_guia": envio.numero_guia,
        "tipo_envio": tipo_envio,
        "id_bodega": None,
        "placa_vehiculo": None,
        "id_puerto": None,
        "numero_flota": None,
    }

    if terrestre is not None:
        data["id_bodega"] = terrestre.id_bodega
        data["placa_vehiculo"] = terrestre.placa_vehiculo

    if maritimo is not None:
        data["id_puerto"] = maritimo.id_puerto
        data["numero_flota"] = maritimo.numero_flota

    return data


def _resolver_fechas(envio, dto: ActualizarEnvioDTO) -> tuple:
    fecha_registro = dto.fecha_registro or envio.fecha_registro
    fecha_entrega = dto.fecha_entrega or envio.fecha_entrega
    if fecha_entrega < fecha_registro:
        raise conflicto("fecha_entrega no puede ser anterior a fecha_registro")
    return fecha_registro, fecha_entrega


def _resolver_precios(*, precio_base: Decimal, cantidad: int, tipo_envio: TipoEnvio) -> tuple[Decimal, Decimal, Decimal]:
    # Cuantiza a 2 decimales para consistencia con NUMERIC(10,2)
    q = Decimal("0.01")
    precio_base_q = precio_base.quantize(q)
    descuento_q = calcular_monto_descuento(precio_base=precio_base_q, cantidad=cantidad, tipo_envio=tipo_envio)
    precio_final_q = (precio_base_q - descuento_q).quantize(q)
    if precio_final_q < 0:
        raise conflicto("precio_final no puede ser negativo (precio_base - descuento)")
    return precio_base_q, descuento_q, precio_final_q


def _actualizar_detalle_terrestre(db: Session, terrestre, dto: ActualizarEnvioDTO) -> None:
    if terrestre is None:
        raise conflicto("Detalle terrestre no existe")
    if dto.id_puerto is not None or dto.numero_flota is not None:
        raise conflicto("Campos marítimos no aplican para TERRESTRE")
    if dto.id_bodega is not None:
        obtener_bodega(db, dto.id_bodega)
    repository.actualizar_terrestre(db, terrestre, id_bodega=dto.id_bodega, placa_vehiculo=dto.placa_vehiculo)


def _actualizar_detalle_maritimo(db: Session, maritimo, dto: ActualizarEnvioDTO) -> None:
    if maritimo is None:
        raise conflicto("Detalle marítimo no existe")
    if dto.id_bodega is not None or dto.placa_vehiculo is not None:
        raise conflicto("Campos terrestres no aplican para MARITIMO")
    if dto.id_puerto is not None:
        obtener_puerto(db, dto.id_puerto)
    repository.actualizar_maritimo(db, maritimo, id_puerto=dto.id_puerto, numero_flota=dto.numero_flota)


def _actualizar_detalle(db: Session, tipo_actual: TipoEnvio, terrestre, maritimo, dto: ActualizarEnvioDTO) -> None:
    if tipo_actual == "TERRESTRE":
        _actualizar_detalle_terrestre(db, terrestre, dto)
        return
    if tipo_actual == "MARITIMO":
        _actualizar_detalle_maritimo(db, maritimo, dto)
        return
    raise conflicto("tipo_envio inválido")


def crear_envio(db: Session, dto: CrearEnvioDTO):
    obtener_cliente(db, dto.id_cliente)
    # Valida existencia de FKs
    obtener_tipo_producto(db, dto.id_tipo_producto)

    tipo_envio: TipoEnvio = dto.tipo_envio
    precio_base, descuento, precio_final = _resolver_precios(
        precio_base=dto.precio_base,
        cantidad=dto.cantidad,
        tipo_envio=tipo_envio,
    )

    try:
        if dto.tipo_envio == "TERRESTRE":
            obtener_bodega(db, dto.id_bodega)  # type: ignore[arg-type]
            envio, terrestre = repository.crear_terrestre(
                db,
                id_cliente=dto.id_cliente,
                id_tipo_producto=dto.id_tipo_producto,
                cantidad=dto.cantidad,
                fecha_registro=dto.fecha_registro,
                fecha_entrega=dto.fecha_entrega,
                precio_base=precio_base,
                descuento=descuento,
                precio_final=precio_final,
                numero_guia=dto.numero_guia,
                id_bodega=dto.id_bodega,  # type: ignore[arg-type]
                placa_vehiculo=dto.placa_vehiculo or "",
            )
            return envio, terrestre, None

        obtener_puerto(db, dto.id_puerto)  # type: ignore[arg-type]
        envio, maritimo = repository.crear_maritimo(
            db,
            id_cliente=dto.id_cliente,
            id_tipo_producto=dto.id_tipo_producto,
            cantidad=dto.cantidad,
            fecha_registro=dto.fecha_registro,
            fecha_entrega=dto.fecha_entrega,
            precio_base=precio_base,
            descuento=descuento,
            precio_final=precio_final,
            numero_guia=dto.numero_guia,
            id_puerto=dto.id_puerto,  # type: ignore[arg-type]
            numero_flota=dto.numero_flota or "",
        )
        return envio, None, maritimo

    except IntegrityError as exc:
        raise conflicto("No se pudo crear el envío (posible número_guía duplicado)") from exc


def obtener_envio(db: Session, envio_id: int):
    row = repository.obtener_por_id(db, envio_id)
    if row is None:
        raise no_encontrado("Envío no encontrado")
    return row


def listar_envios(
    db: Session,
    *,
    page: int,
    page_size: int,
    q: str | None = None,
    id_cliente: int | None = None,
    id_tipo_producto: int | None = None,
    tipo_envio: TipoEnvio | None = None,
):
    return repository.listar(
        db,
        page=page,
        page_size=page_size,
        q=q,
        id_cliente=id_cliente,
        id_tipo_producto=id_tipo_producto,
        tipo_envio=tipo_envio,
    )


def actualizar_envio(db: Session, envio_id: int, dto: ActualizarEnvioDTO):
    envio, terrestre, maritimo = obtener_envio(db, envio_id)

    tipo_actual: TipoEnvio
    if terrestre is not None:
        tipo_actual = "TERRESTRE"
    elif maritimo is not None:
        tipo_actual = "MARITIMO"
    else:
        raise conflicto("Envío sin detalle terrestre/marítimo")

    _resolver_fechas(envio, dto)

    if dto.id_cliente is not None:
        obtener_cliente(db, dto.id_cliente)

    if dto.id_tipo_producto is not None:
        obtener_tipo_producto(db, dto.id_tipo_producto)

    cantidad = dto.cantidad if dto.cantidad is not None else envio.cantidad
    precio_base_in = dto.precio_base if dto.precio_base is not None else envio.precio_base
    precio_base, descuento, precio_final = _resolver_precios(
        precio_base=precio_base_in,
        cantidad=cantidad,
        tipo_envio=tipo_actual,
    )

    try:
        repository.actualizar_base(
            db,
            envio,
            id_cliente=dto.id_cliente,
            id_tipo_producto=dto.id_tipo_producto,
            cantidad=dto.cantidad,
            fecha_registro=dto.fecha_registro,
            fecha_entrega=dto.fecha_entrega,
            precio_base=precio_base,
            descuento=descuento,
            precio_final=precio_final,
            numero_guia=dto.numero_guia,
        )

        _actualizar_detalle(db, tipo_actual, terrestre, maritimo, dto)

    except IntegrityError as exc:
        raise conflicto("No se pudo actualizar el envío (posible número_guía duplicado)") from exc

    return obtener_envio(db, envio_id)


def eliminar_envio(db: Session, envio_id: int) -> None:
    envio, _, _ = obtener_envio(db, envio_id)
    repository.eliminar(db, envio)
