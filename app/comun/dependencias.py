from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.base_de_datos.sesion import get_session

DBSession = Annotated[Session, Depends(get_session)]
