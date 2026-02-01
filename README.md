# Plataforma Logística (API)

API REST (FastAPI) para gestionar envíos terrestres y marítimos, con monolito modular y Clean Architecture ligera.

## Ejecutar en local (Windows)

1) Instalar dependencias

- Activar el entorno y luego instalar:
  - `pip install -e .`

2) Variables de entorno

- El proyecto incluye un `.env` en la raíz. Ajusta al menos:
  - `DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5433/plataforma_logistica`
  - `JWT_SECRET=...` (ideal >= 32 bytes)

3) Base de datos (PostgreSQL)

- Levantar Postgres:
  - `docker compose up -d`
- Aplica migraciones (si corresponde):
  - `alembic upgrade head`

4) Correr API

- `uvicorn app.main:app --reload`

## Frontend (React + Vite)

En otra terminal:

- `cd frontend`
- `npm install`
- `npm run dev`

Abre `http://localhost:5173/`.

## Endpoints base

- `GET /api/v1/health`
- `POST /api/v1/auth/token` (demo: `admin`/`admin`)

CRUD principal (todos requieren Bearer):

- `clientes`: `GET/POST /api/v1/clientes`, `GET/DELETE /api/v1/clientes/{id}`
- `tipos-producto`: `GET/POST /api/v1/tipos-producto`, `GET/PATCH/DELETE /api/v1/tipos-producto/{id}`
- `bodegas`: `GET/POST /api/v1/bodegas`, `GET/PATCH/DELETE /api/v1/bodegas/{id}`
- `puertos`: `GET/POST /api/v1/puertos`, `GET/PATCH/DELETE /api/v1/puertos/{id}`
- `envios`: `GET/POST /api/v1/envios`, `GET/PATCH/DELETE /api/v1/envios/{id}`

Filtros de búsqueda (según recurso):

- Paginación: `page`, `page_size`
- Búsqueda: `q`
- Envíos: `id_cliente`, `id_tipo_producto`, `tipo_envio`

Documentación API (Swagger):

- `GET /docs`
- `GET /openapi.json`

## Entregables

- Diagrama E-R: `docs/DIAGRAMA_ER.md`
- Script de base de datos (DDL): `scripts/schema.sql`
- Justificación de tecnologías/patrones y buenas prácticas: `docs/ENTREGABLES.md`

## Git-Flow

- Estructura y convención de ramas: `docs/GIT_FLOW.md`

## Estructura (carpetas en español)

- `app/autenticacion`: JWT y dependencias
- `app/envios`: módulos de envíos (base / terrestre / marítimo)
- `app/comun`: regex, excepciones, dependencias compartidas
- `app/base_de_datos`: configuración, engine y sesión
- `app/tests`: pruebas puntuales con pytest
