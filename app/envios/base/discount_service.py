from __future__ import annotations

from decimal import Decimal
from typing import Literal


TipoEnvio = Literal["TERRESTRE", "MARITIMO"]


def calcular_tasa_descuento(*, cantidad: int, tipo_envio: TipoEnvio) -> Decimal:
    """Reglas del enunciado.

    - Si cantidad > 10:
      - TERRESTRE: 5%
      - MARITIMO: 3%
    - Caso contrario: 0%
    """
    if cantidad <= 10:
        return Decimal("0")
    return Decimal("0.05") if tipo_envio == "TERRESTRE" else Decimal("0.03")


def calcular_monto_descuento(*, precio_base: Decimal, cantidad: int, tipo_envio: TipoEnvio) -> Decimal:
    """Retorna el monto de descuento (no el porcentaje)."""
    tasa = calcular_tasa_descuento(cantidad=cantidad, tipo_envio=tipo_envio)
    q = Decimal("0.01")
    return (precio_base * tasa).quantize(q)
