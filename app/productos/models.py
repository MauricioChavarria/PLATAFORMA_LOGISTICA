from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.base_de_datos.base import Base
from app.comun.modelos import SoftDeleteMixin


class Producto(Base, SoftDeleteMixin):
    __tablename__ = "productos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(160), index=True)
    descripcion: Mapped[str | None] = mapped_column(String(500), nullable=True)
