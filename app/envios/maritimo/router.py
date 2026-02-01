from fastapi import APIRouter, Depends

from app.autenticacion.dependencies import obtener_usuario_actual
from app.envios.maritimo.schemas import CrearEnvioMaritimoDTO, EnvioMaritimoDTO
from app.envios.maritimo.service import cotizar_envio

router = APIRouter()


@router.post("/envios/maritimos/cotizar", response_model=EnvioMaritimoDTO)
def cotizar(dto: CrearEnvioMaritimoDTO, _: dict = Depends(obtener_usuario_actual)) -> EnvioMaritimoDTO:
    return cotizar_envio(dto)
