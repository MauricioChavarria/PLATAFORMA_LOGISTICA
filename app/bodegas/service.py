from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.bodegas import repository
from app.bodegas.schemas import ActualizarBodegaDTO, CrearBodegaDTO
from app.comun.excepciones import conflicto, no_encontrado


def crear_bodega(db: Session, dto: CrearBodegaDTO):
    try:
        return repository.crear(db, nombre=dto.nombre, ubicacion=dto.ubicacion, pais=dto.pais)
    except IntegrityError as exc:
        raise conflicto("No se pudo crear la bodega") from exc


def obtener_bodega(db: Session, bodega_id: int):
    obj = repository.obtener_por_id(db, bodega_id)
    if obj is None:
        raise no_encontrado("Bodega no encontrada")
    return obj


def listar_bodegas(db: Session, *, page: int, page_size: int, q: str | None = None, pais: str | None = None):
    return repository.listar(db, page=page, page_size=page_size, q=q, pais=pais)


def actualizar_bodega(db: Session, bodega_id: int, dto: ActualizarBodegaDTO):
    obj = obtener_bodega(db, bodega_id)
    try:
        return repository.actualizar(db, obj, nombre=dto.nombre, ubicacion=dto.ubicacion, pais=dto.pais)
    except IntegrityError as exc:
        raise conflicto("No se pudo actualizar la bodega") from exc


def eliminar_bodega(db: Session, bodega_id: int) -> None:
    obj = obtener_bodega(db, bodega_id)
    repository.soft_delete(db, obj)
