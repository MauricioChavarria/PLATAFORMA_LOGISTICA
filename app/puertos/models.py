from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.base_de_datos.base import Base


class Puerto(Base):
    __tablename__ = "puerto"

    id_puerto: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    ciudad: Mapped[str | None] = mapped_column(String(100), nullable=True)
