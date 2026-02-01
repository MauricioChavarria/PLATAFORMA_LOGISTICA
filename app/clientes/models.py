from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.base_de_datos.base import Base
from app.comun.modelos import SoftDeleteMixin


class Cliente(Base, SoftDeleteMixin):
    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(120), index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    documento: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    telefono: Mapped[str | None] = mapped_column(String(32), nullable=True)
