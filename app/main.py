from fastapi import FastAPI

from app.autenticacion.router import router as autenticacion_router
from app.clientes.router import router as clientes_router
from app.envios.terrestre.router import router as envios_terrestres_router
from app.envios.maritimo.router import router as envios_maritimos_router


API_PREFIX = "/api/v1"


def create_app() -> FastAPI:
    app = FastAPI(title="Plataforma Logística API", version="0.1.0")

    app.include_router(autenticacion_router, prefix=API_PREFIX, tags=["autenticacion"])
    app.include_router(clientes_router, prefix=API_PREFIX, tags=["clientes"])
    app.include_router(envios_terrestres_router, prefix=API_PREFIX, tags=["envios-terrestres"])
    app.include_router(envios_maritimos_router, prefix=API_PREFIX, tags=["envios-maritimos"])

    @app.get(f"{API_PREFIX}/health", tags=["health"])
    def health() -> dict:
        return {"status": "ok"}

    return app


app = create_app()
