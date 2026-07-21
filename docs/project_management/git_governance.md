# Gobierno Git y GitHub

## Objetivo

Usar GitHub como sistema de trazabilidad, revisión, calidad y releases, no únicamente como copia remota del código.

## Ramas

```text
feature/fix/docs/test/ci
          ↓ Pull Request
         dev
          ↓ release PR
         main
          ↓ tag
       release
```

- `dev`: integración continua del equipo.
- `main`: versiones estables y desplegables.
- Ramas de trabajo: cambios pequeños y revisables.
- Hotfix: se definirá cuando exista producción.

## Reglas recomendadas para `dev`

- Pull Request obligatorio.
- Al menos una aprobación cuando el equipo pueda aplicarla.
- Conversaciones resueltas antes del merge.
- Checks de calidad obligatorios.
- Rama actualizada antes del merge.
- Sin force push ni borrado.

## Reglas recomendadas para `main`

- Pull Request de release desde `dev`.
- Aprobación adicional para cambios de seguridad, datos o despliegue.
- Todos los quality gates obligatorios.
- Sin push directo.
- Despliegue únicamente desde `main` o tags aprobados.

Estas reglas se aplicarán en GitHub cuando exista consenso del equipo y los workflows necesarios estén operativos.

## Issues y specs

- La spec conserva el contrato y las decisiones.
- El Issue sirve para coordinación, responsable y conversación.
- La tarea de `tasks.md` conserva criterio de cierre y evidencia.
- PR, Issue, spec y tarea deben enlazarse entre sí.

## Commits

Se utilizarán mensajes convencionales:

```text
feat, fix, docs, test, ci, build, refactor, perf, chore
```

Los commits deben representar unidades comprensibles. Se evitarán `cambios`, `update`, `final`, `final-final` o equivalentes.

## Tags y versiones

Se seguirá Semantic Versioning cuando exista una API o producto versionable:

- `MAJOR`: cambio incompatible.
- `MINOR`: funcionalidad compatible.
- `PATCH`: corrección compatible.

Durante la construcción pueden utilizarse hitos previos a `v1.0.0`, por ejemplo:

```text
v0.1.0-foundation
v0.2.0-data-contract
v0.3.0-essential-mvp
v0.4.0-model-champion
v0.5.0-deployed-mvp
v0.6.0-mlops-observability
v1.0.0
```

Los nombres son una guía y solo se crearán cuando el hito esté realmente verificado.

## Releases

Antes de etiquetar:

1. Actualizar changelog.
2. Ejecutar quality gates.
3. Validar aplicación y documentación.
4. Confirmar migraciones y rollback cuando aplique.
5. Mergear el release en `main`.
6. Verificar despliegue.
7. Crear tag anotado y GitHub Release.

`.github/release.yml` categoriza automáticamente las notas generadas por GitHub.

## Funcionalidades adicionales con sentido

- Plantillas estructuradas de Issues y Pull Requests.
- Dependabot para acciones y dependencias.
- CODEOWNERS cuando se conozcan handles y responsabilidades.
- Environments para staging y producción.
- Revisores requeridos para producción.
- Releases y changelog trazables.
- GitHub Projects o tablero equivalente enlazado con specs.
- Security scanning y CodeQL cuando exista código compatible.
- Artefactos y reportes de tests conservados por workflow.
