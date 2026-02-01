from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.comun.excepciones import conflicto, no_encontrado
from app.puertos import repository
from app.puertos.schemas import ActualizarPuertoDTO, CrearPuertoDTO


def crear_puerto(db: Session, dto: CrearPuertoDTO):
    try:
        return repository.crear(db, nombre=dto.nombre, pais=dto.pais)
    except IntegrityError as exc:
        raise conflicto("No se pudo crear el puerto") from exc


def obtener_puerto(db: Session, puerto_id: int):
    obj = repository.obtener_por_id(db, puerto_id)
    if obj is None:
        raise no_encontrado("Puerto no encontrado")
    return obj


def listar_puertos(db: Session, *, page: int, page_size: int, q: str | None = None, pais: str | None = None):
    return repository.listar(db, page=page, page_size=page_size, q=q, pais=pais)


def actualizar_puerto(db: Session, puerto_id: int, dto: ActualizarPuertoDTO):
    obj = obtener_puerto(db, puerto_id)
    try:
        return repository.actualizar(db, obj, nombre=dto.nombre, pais=dto.pais)
    except IntegrityError as exc:
        raise conflicto("No se pudo actualizar el puerto") from exc


def eliminar_puerto(db: Session, puerto_id: int) -> None:
    obj = obtener_puerto(db, puerto_id)
    repository.soft_delete(db, obj)
