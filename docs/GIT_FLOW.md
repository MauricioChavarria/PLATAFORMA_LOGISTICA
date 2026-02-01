# Git-Flow (estructura del repositorio)

Este repositorio sigue el estándar **Git-Flow** con las ramas principales:

- `main`: rama estable / entregable.
- `develop`: rama de integración.

## Convención de ramas

- `feature/<nombre>`: desarrollo de nuevas funcionalidades (sale de `develop`, vuelve a `develop`).
- `release/<version>`: estabilización y preparación de release (sale de `develop`, vuelve a `main` y `develop`).
- `hotfix/<version>`: correcciones urgentes en producción (sale de `main`, vuelve a `main` y `develop`).

## Flujo recomendado

1) Crear rama feature desde `develop`

- `git checkout develop`
- `git pull`
- `git checkout -b feature/mi-cambio`

2) Trabajar, commitear y subir

- `git add -A`
- `git commit -m "feat: ..."`
- `git push -u origin feature/mi-cambio`

3) Integrar a `develop`

- Merge vía PR (recomendado) o merge local.

4) Release

- Crear `release/<version>` desde `develop`, estabilizar.
- Merge a `main` y tag (ej: `v0.1.0`).
- Merge de vuelta a `develop`.

## Nota sobre configuración de GitHub

La estructura de ramas queda en el repositorio, pero la protección de ramas (requerir PR, checks, etc.)
se configura en GitHub (Settings → Branch protection rules).
