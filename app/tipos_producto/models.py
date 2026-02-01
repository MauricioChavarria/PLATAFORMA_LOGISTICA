from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.base_de_datos.base import Base


class TipoProducto(Base):
    __tablename__ = "tipo_producto"

    id_tipo_producto: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
