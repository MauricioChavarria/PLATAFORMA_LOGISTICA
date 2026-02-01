from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.comun.excepciones import conflicto, no_encontrado
from app.envios.base.models import Envio
from app.tipos_producto import repository
from app.tipos_producto.schemas import ActualizarTipoProductoDTO, CrearTipoProductoDTO


def crear_tipo_producto(db: Session, dto: CrearTipoProductoDTO):
    try:
        return repository.crear(db, nombre=dto.nombre)
    except IntegrityError as exc:
        raise conflicto("No se pudo crear el tipo de producto") from exc


def listar_tipos_producto(db: Session, *, page: int, page_size: int, q: str | None = None):
    return repository.listar(db, page=page, page_size=page_size, q=q)


def obtener_tipo_producto(db: Session, tipo_producto_id: int):
    obj = repository.obtener_por_id(db, tipo_producto_id)
    if obj is None:
        raise no_encontrado("Tipo de producto no encontrado")
    return obj


def actualizar_tipo_producto(db: Session, tipo_producto_id: int, dto: ActualizarTipoProductoDTO):
    obj = obtener_tipo_producto(db, tipo_producto_id)
    try:
        return repository.actualizar(db, obj, nombre=dto.nombre)
    except IntegrityError as exc:
        raise conflicto("No se pudo actualizar el tipo de producto") from exc


def eliminar_tipo_producto(db: Session, tipo_producto_id: int) -> None:
    obj = obtener_tipo_producto(db, tipo_producto_id)

    total_envios = db.scalar(select(func.count()).select_from(Envio).where(Envio.id_tipo_producto == tipo_producto_id)) or 0
    if int(total_envios) > 0:
        raise conflicto("No se puede eliminar el tipo de producto: tiene envíos asociados")

    try:
        repository.eliminar(db, obj)
    except IntegrityError as exc:
        db.rollback()
        raise conflicto("No se puede eliminar el tipo de producto: tiene envíos asociados") from exc
