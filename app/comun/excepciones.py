from fastapi import HTTPException, status


def no_autorizado(detalle: str = "No autorizado") -> HTTPException:
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=detalle)


def prohibido(detalle: str = "Prohibido") -> HTTPException:
    return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detalle)


def no_encontrado(detalle: str = "No encontrado") -> HTTPException:
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detalle)


def conflicto(detalle: str = "Conflicto") -> HTTPException:
    return HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detalle)
