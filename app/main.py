from fastapi import FastAPI

from app.autenticacion.router import router as autenticacion_router
from app.envios.terrestre.router import router as envios_terrestres_router
from app.envios.maritimo.router import router as envios_maritimos_router


def create_app() -> FastAPI:
    app = FastAPI(title="Plataforma Logística API", version="0.1.0")

    app.include_router(autenticacion_router, prefix="/api/v1", tags=["autenticacion"])
    app.include_router(envios_terrestres_router, prefix="/api/v1", tags=["envios-terrestres"])
    app.include_router(envios_maritimos_router, prefix="/api/v1", tags=["envios-maritimos"])

    @app.get("/api/v1/health", tags=["health"])
    def health() -> dict:
        return {"status": "ok"}

    return app


app = create_app()
