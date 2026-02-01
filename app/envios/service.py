from __future__ import annotations

from decimal import Decimal

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.bodegas.service import obtener_bodega
from app.clientes.service import obtener_cliente
from app.comun.excepciones import conflicto, no_encontrado
from app.envios import repository
from app.envios.schemas import ActualizarEnvioDTO, CrearEnvioDTO, TipoEnvio
from app.productos.service import obtener_producto
from app.puertos.service import obtener_puerto


def _precio_final(precio_base: Decimal, descuento: Decimal) -> Decimal:
    return precio_base - descuento


def _to_dto_dict(envio, terrestre, maritimo) -> dict:
    data = {
        "id": envio.id,
        "cliente_id": envio.cliente_id,
        "producto_id": envio.producto_id,
        "cantidad": envio.cantidad,
        "fecha_registro": envio.fecha_registro,
        "fecha_entrega": envio.fecha_entrega,
        "precio_base": envio.precio_base,
        "descuento": envio.descuento,
        "precio_final": envio.precio_final,
        "numero_guia": envio.numero_guia,
        "tipo_envio": envio.tipo_envio,
        "creado_en": envio.creado_en,
        "bodega_id": None,
        "placa_vehiculo": None,
        "puerto_id": None,
        "numero_flota": None,
    }

    if terrestre is not None:
        data["bodega_id"] = terrestre.bodega_id
        data["placa_vehiculo"] = terrestre.placa_vehiculo

    if maritimo is not None:
        data["puerto_id"] = maritimo.puerto_id
        data["numero_flota"] = maritimo.numero_flota

    return data


def _validar_tipo_no_cambia(tipo_actual: str, tipo_nuevo: TipoEnvio | None) -> None:
    if tipo_nuevo is not None and tipo_nuevo != tipo_actual:
        raise conflicto("No se permite cambiar tipo_envio")


def _resolver_fechas(envio, dto: ActualizarEnvioDTO) -> tuple:
    fecha_registro = dto.fecha_registro or envio.fecha_registro
    fecha_entrega = dto.fecha_entrega or envio.fecha_entrega
    if fecha_entrega < fecha_registro:
        raise conflicto("fecha_entrega no puede ser anterior a fecha_registro")
    return fecha_registro, fecha_entrega


def _resolver_precios(envio, dto: ActualizarEnvioDTO) -> tuple[Decimal, Decimal, Decimal]:
    precio_base = dto.precio_base if dto.precio_base is not None else envio.precio_base
    descuento = dto.descuento if dto.descuento is not None else envio.descuento

    precio_base_dec = Decimal(str(precio_base))
    descuento_dec = Decimal(str(descuento))

    if descuento_dec > precio_base_dec:
        raise conflicto("descuento no puede ser mayor a precio_base")

    return precio_base_dec, descuento_dec, _precio_final(precio_base_dec, descuento_dec)


def _actualizar_detalle_terrestre(db: Session, terrestre, dto: ActualizarEnvioDTO) -> None:
    if terrestre is None:
        raise conflicto("Detalle terrestre no existe")
    if dto.puerto_id is not None or dto.numero_flota is not None:
        raise conflicto("Campos marítimos no aplican para TERRESTRE")
    if dto.bodega_id is not None:
        obtener_bodega(db, dto.bodega_id)
    repository.actualizar_terrestre(db, terrestre, bodega_id=dto.bodega_id, placa_vehiculo=dto.placa_vehiculo)


def _actualizar_detalle_maritimo(db: Session, maritimo, dto: ActualizarEnvioDTO) -> None:
    if maritimo is None:
        raise conflicto("Detalle marítimo no existe")
    if dto.bodega_id is not None or dto.placa_vehiculo is not None:
        raise conflicto("Campos terrestres no aplican para MARITIMO")
    if dto.puerto_id is not None:
        obtener_puerto(db, dto.puerto_id)
    repository.actualizar_maritimo(db, maritimo, puerto_id=dto.puerto_id, numero_flota=dto.numero_flota)


def _actualizar_detalle(db: Session, envio, terrestre, maritimo, dto: ActualizarEnvioDTO) -> None:
    if envio.tipo_envio == "TERRESTRE":
        _actualizar_detalle_terrestre(db, terrestre, dto)
        return

    if envio.tipo_envio == "MARITIMO":
        _actualizar_detalle_maritimo(db, maritimo, dto)
        return

    raise conflicto("tipo_envio inválido")


def crear_envio(db: Session, dto: CrearEnvioDTO):
    # Valida existencia de FKs
    obtener_cliente(db, dto.cliente_id)
    obtener_producto(db, dto.producto_id)

    precio_final = _precio_final(dto.precio_base, dto.descuento)

    try:
        if dto.tipo_envio == "TERRESTRE":
            obtener_bodega(db, dto.bodega_id)  # type: ignore[arg-type]
            envio, terrestre = repository.crear_terrestre(
                db,
                cliente_id=dto.cliente_id,
                producto_id=dto.producto_id,
                cantidad=dto.cantidad,
                fecha_registro=dto.fecha_registro,
                fecha_entrega=dto.fecha_entrega,
                precio_base=dto.precio_base,
                descuento=dto.descuento,
                precio_final=precio_final,
                numero_guia=dto.numero_guia,
                bodega_id=dto.bodega_id,  # type: ignore[arg-type]
                placa_vehiculo=dto.placa_vehiculo or "",
            )
            return envio, terrestre, None

        obtener_puerto(db, dto.puerto_id)  # type: ignore[arg-type]
        envio, maritimo = repository.crear_maritimo(
            db,
            cliente_id=dto.cliente_id,
            producto_id=dto.producto_id,
            cantidad=dto.cantidad,
            fecha_registro=dto.fecha_registro,
            fecha_entrega=dto.fecha_entrega,
            precio_base=dto.precio_base,
            descuento=dto.descuento,
            precio_final=precio_final,
            numero_guia=dto.numero_guia,
            puerto_id=dto.puerto_id,  # type: ignore[arg-type]
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
    cliente_id: int | None = None,
    producto_id: int | None = None,
    tipo_envio: TipoEnvio | None = None,
):
    return repository.listar(
        db,
        page=page,
        page_size=page_size,
        q=q,
        cliente_id=cliente_id,
        producto_id=producto_id,
        tipo_envio=tipo_envio,
    )


def actualizar_envio(db: Session, envio_id: int, dto: ActualizarEnvioDTO):
    envio, terrestre, maritimo = obtener_envio(db, envio_id)

    _validar_tipo_no_cambia(envio.tipo_envio, dto.tipo_envio)
    _resolver_fechas(envio, dto)
    _, _, precio_final = _resolver_precios(envio, dto)

    try:
        repository.actualizar_base(
            db,
            envio,
            cantidad=dto.cantidad,
            fecha_registro=dto.fecha_registro,
            fecha_entrega=dto.fecha_entrega,
            precio_base=dto.precio_base,
            descuento=dto.descuento,
            precio_final=precio_final,
            numero_guia=dto.numero_guia,
        )

        _actualizar_detalle(db, envio, terrestre, maritimo, dto)

    except IntegrityError as exc:
        raise conflicto("No se pudo actualizar el envío (posible número_guía duplicado)") from exc

    return obtener_envio(db, envio_id)


def eliminar_envio(db: Session, envio_id: int) -> None:
    envio, _, _ = obtener_envio(db, envio_id)
    repository.soft_delete(db, envio)
