from app.envios.base.discount_service import calcular_descuento_por_volumen
from app.envios.maritimo.schemas import CrearEnvioMaritimoDTO, EnvioMaritimoDTO


def cotizar_envio(dto: CrearEnvioMaritimoDTO) -> EnvioMaritimoDTO:
    descuento = calcular_descuento_por_volumen(dto.cantidad)
    return EnvioMaritimoDTO(
        id=0,
        guia=dto.guia,
        cliente_id=dto.cliente_id,
        puerto_origen_id=dto.puerto_origen_id,
        puerto_destino_id=dto.puerto_destino_id,
        descuento=descuento,
    )
