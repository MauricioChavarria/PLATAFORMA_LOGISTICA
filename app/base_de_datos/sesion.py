from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.base_de_datos.configuracion import settings

engine = create_engine(settings.database_url, pool_pre_ping=True)


def get_session() -> Generator[Session, None, None]:
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()
