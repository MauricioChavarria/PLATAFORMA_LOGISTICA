# Entregables y decisiones

## Tecnologías

- Backend: FastAPI + Pydantic + SQLAlchemy + Alembic.
- Persistencia: PostgreSQL (docker-compose).
- Frontend: React + Vite + TypeScript.
- Pruebas: pytest.

## Patrones aplicados

- Separación por capas ligera:
  - `router` (HTTP) → `service` (reglas de negocio) → `repository` (persistencia).
- DTOs con Pydantic para validación/contratos.
- Manejo de errores de integridad (`IntegrityError`) traducido a `409` cuando aplica.

## Buenas prácticas (resumen)

- Validaciones:
  - Validación de payloads (422) por Pydantic.
  - Validación de reglas de negocio (409/400 según corresponda).
- Seguridad:
  - Token tipo Bearer y validación del token en endpoints protegidos.
- Migraciones:
  - Alembic para versionamiento del esquema.
- Calidad:
  - Pruebas unitarias de CRUD y regla de descuentos.

## Cómo evidenciar cumplimiento

- Diagrama E-R: ver `docs/DIAGRAMA_ER.png`.
- Script de base de datos: ver `scripts/schema.sql` (generado desde Alembic).
- URL repositorio: remoto `origin` en GitHub.
- Artefactos de despliegue: `docker-compose.yml` + instrucciones en README.
