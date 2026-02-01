import pytest

from app.envios.base.discount_service import calcular_descuento_por_volumen


def test_descuento_por_volumen() -> None:
    assert calcular_descuento_por_volumen(1) == pytest.approx(0.0)
    assert calcular_descuento_por_volumen(10) == pytest.approx(0.05)
    assert calcular_descuento_por_volumen(49) == pytest.approx(0.05)
    assert calcular_descuento_por_volumen(50) == pytest.approx(0.10)
