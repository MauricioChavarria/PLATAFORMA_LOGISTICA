from fastapi import APIRouter, Depends

from app.autenticacion.dependencies import obtener_usuario_actual
from app.envios.terrestre.schemas import CrearEnvioTerrestreDTO, EnvioTerrestreDTO
from app.envios.terrestre.service import cotizar_envio

router = APIRouter()


@router.post("/envios/terrestres/cotizar", response_model=EnvioTerrestreDTO)
def cotizar(dto: CrearEnvioTerrestreDTO, _: dict = Depends(obtener_usuario_actual)) -> EnvioTerrestreDTO:
    return cotizar_envio(dto)
