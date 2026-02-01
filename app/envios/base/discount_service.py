def calcular_descuento_por_volumen(cantidad: int) -> float:
    """Regla simple para mostrar 'base común'.

    - 0..9   => 0%
    - 10..49 => 5%
    - 50+    => 10%
    """
    if cantidad >= 50:
        return 0.10
    if cantidad >= 10:
        return 0.05
    return 0.0
