from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.base_de_datos.base import Base


class Bodega(Base):
    __tablename__ = "bodega"

    id_bodega: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    direccion: Mapped[str | None] = mapped_column(String(200), nullable=True)
