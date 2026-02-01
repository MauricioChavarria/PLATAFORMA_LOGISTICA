from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.comun.excepciones import conflicto, no_encontrado
from app.productos import repository
from app.productos.schemas import ActualizarProductoDTO, CrearProductoDTO


def crear_producto(db: Session, dto: CrearProductoDTO):
    try:
        return repository.crear(db, nombre=dto.nombre, descripcion=dto.descripcion)
    except IntegrityError as exc:
        raise conflicto("No se pudo crear el producto") from exc


def obtener_producto(db: Session, producto_id: int):
    obj = repository.obtener_por_id(db, producto_id)
    if obj is None:
        raise no_encontrado("Producto no encontrado")
    return obj


def listar_productos(db: Session, *, page: int, page_size: int, q: str | None = None):
    return repository.listar(db, page=page, page_size=page_size, q=q)


def actualizar_producto(db: Session, producto_id: int, dto: ActualizarProductoDTO):
    obj = obtener_producto(db, producto_id)
    try:
        return repository.actualizar(db, obj, nombre=dto.nombre, descripcion=dto.descripcion)
    except IntegrityError as exc:
        raise conflicto("No se pudo actualizar el producto") from exc


def eliminar_producto(db: Session, producto_id: int) -> None:
    obj = obtener_producto(db, producto_id)
    repository.soft_delete(db, obj)
