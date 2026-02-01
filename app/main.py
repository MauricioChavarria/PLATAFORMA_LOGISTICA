from fastapi import FastAPI

from app.autenticacion.router import router as autenticacion_router
from app.bodegas.router import router as bodegas_router
from app.clientes.router import router as clientes_router
from app.envios.router import router as envios_router
from app.puertos.router import router as puertos_router
from app.tipos_producto.router import router as tipos_producto_router
from app.usuarios.router import router as usuarios_router


API_PREFIX = "/api/v1"


def create_app() -> FastAPI:
    app = FastAPI(title="Plataforma Logística API", version="0.1.0")

    app.include_router(autenticacion_router, prefix=API_PREFIX, tags=["autenticacion"])
    app.include_router(usuarios_router, prefix=API_PREFIX, tags=["autenticacion"])
    app.include_router(clientes_router, prefix=API_PREFIX, tags=["clientes"])
    app.include_router(tipos_producto_router, prefix=API_PREFIX, tags=["tipos-producto"])
    app.include_router(bodegas_router, prefix=API_PREFIX, tags=["bodegas"])
    app.include_router(puertos_router, prefix=API_PREFIX, tags=["puertos"])
    app.include_router(envios_router, prefix=API_PREFIX, tags=["envios"])

    @app.get(f"{API_PREFIX}/health", tags=["health"])
    def health() -> dict:
        return {"status": "ok"}

    return app


app = create_app()
