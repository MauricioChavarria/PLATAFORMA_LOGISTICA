# Plataforma Logística (API)

API REST (FastAPI) para gestionar envíos terrestres y marítimos, con monolito modular y Clean Architecture ligera.

## Ejecutar en local (Windows)

1) Instalar dependencias

- Activar el entorno y luego instalar:
  - `pip install -e .`

2) Variables de entorno

- El proyecto incluye un `.env` en la raíz. Ajusta al menos:
  - `DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/plataforma_logistica`
  - `JWT_SECRET=...` (ideal >= 32 bytes)

3) Correr API

- `uvicorn app.main:app --reload`

## Endpoints base

- `GET /api/v1/health`
- `POST /api/v1/auth/token` (demo: `admin`/`admin`)
- `POST /api/v1/envios/terrestres/cotizar` (requiere Bearer)
- `POST /api/v1/envios/maritimos/cotizar` (requiere Bearer)

## Estructura (carpetas en español)

- `app/autenticacion`: JWT y dependencias
- `app/envios`: módulos de envíos (base / terrestre / marítimo)
- `app/comun`: regex, excepciones, dependencias compartidas
- `app/base_de_datos`: configuración, engine y sesión
- `app/tests`: pruebas puntuales con pytest
