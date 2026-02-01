"""Registro central de modelos SQLAlchemy.

Importar este módulo garantiza que todos los modelos queden registrados en
`Base.metadata` (útil para `create_all()` en tests y para Alembic).
"""

# Importaciones intencionales para registrar modelos
from app.usuarios.models import Usuario  # noqa: F401
from app.clientes.models import Cliente  # noqa: F401
from app.tipos_producto.models import TipoProducto  # noqa: F401
from app.bodegas.models import Bodega  # noqa: F401
from app.puertos.models import Puerto  # noqa: F401
from app.envios.base.models import Envio, EnvioMaritimo, EnvioTerrestre  # noqa: F401
