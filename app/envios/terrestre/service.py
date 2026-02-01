from app.envios.base.discount_service import calcular_descuento_por_volumen
from app.envios.terrestre.schemas import CrearEnvioTerrestreDTO, EnvioTerrestreDTO


def cotizar_envio(dto: CrearEnvioTerrestreDTO) -> EnvioTerrestreDTO:
    descuento = calcular_descuento_por_volumen(dto.cantidad)
    # Demo sin persistencia todavía.
    return EnvioTerrestreDTO(
        id=0,
        guia=dto.guia,
        cliente_id=dto.cliente_id,
        placa_vehiculo=dto.placa_vehiculo,
        codigo_flota=dto.codigo_flota,
        descuento=descuento,
    )
