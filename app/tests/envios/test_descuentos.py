from decimal import Decimal

from app.envios.base.discount_service import calcular_monto_descuento, calcular_tasa_descuento


def test_tasa_descuento_segun_enunciado() -> None:
    assert calcular_tasa_descuento(cantidad=10, tipo_envio="TERRESTRE") == Decimal("0")
    assert calcular_tasa_descuento(cantidad=11, tipo_envio="TERRESTRE") == Decimal("0.05")
    assert calcular_tasa_descuento(cantidad=11, tipo_envio="MARITIMO") == Decimal("0.03")


def test_monto_descuento_cuantizado() -> None:
    assert calcular_monto_descuento(precio_base=Decimal("1000.00"), cantidad=11, tipo_envio="TERRESTRE") == Decimal("50.00")
    assert calcular_monto_descuento(precio_base=Decimal("1000.00"), cantidad=11, tipo_envio="MARITIMO") == Decimal("30.00")
