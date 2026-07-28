# Equipo

## Integrantes

| Integrante | Rol principal | Rol de respaldo | Estado |
|---|---|---|---|
| José | Backend | Por acordar | Activo |
| Abel | Frontend y UX | Por acordar | Activo |
| Víctor | Datos y EDA | Por acordar | Activo |
| Miguel | Arquitectura, OpenSpec, arnés y coordinación transversal | Por acordar | Activo |

Los roles principales reflejan el acuerdo actual. Los respaldos y la cobertura estable de producto, MLOps y QA siguen pendientes; no deben asignarse por suposición.

## Asignaciones vigentes

| Área | Persona | Referencia | Estado |
|---|---|---|---|
| Datos y EDA | Víctor | `PG-3` · baseline multiclase reproducible | Baseline evaluado; quedan selección posterior y `MED-03` |
| Arquitectura y arnés | Miguel | `integrate-jira-workflow` · excepción `bootstrap` | Activa |
| Frontend y UX | Abel | `PG-4` · `003/T-006` | Prototipo ClaimVox integrado; el flujo local de `PG-6` reutiliza su contrato y experiencia |
| Backend | José | `PG-5` · `003/T-007` | Servicio FastAPI integrado y verificado localmente; usado por `PG-6` |

La tabla describe el estado de `dev`. Una rama o Pull Request abierta no se considera capacidad integrada ni cambia por sí sola estas asignaciones.

## Acuerdo de trabajo con IA

- Cada integrante puede utilizar la herramienta de IA que considere adecuada.
- El repositorio, Jira, OpenSpec y las Pull Requests son el contexto compartido.
- Cada integrante instala las herramientas del propio clon mediante `npm ci`; no depende de archivos preparados por otra persona.
- La persona asignada conserva la responsabilidad de revisar código, datos, decisiones y evidencias.
- No se comparten narrativas CFPB, secretos o datos brutos con servicios externos.
- El [flujo operativo](workflow.md) explica cómo preparar contexto y cerrar una tarea.
- El [manual de Jira](jira_workflow.md) explica qué actualizar y qué no duplicar.

## Cambios de composición

| Fecha | Integrante | Cambio |
|---|---|---|
| 2026-07-22 | Josué | Baja del Bootcamp comunicada; deja de formar parte del equipo activo. |
| 2026-07-23 | Equipo activo | Responsabilidades principales confirmadas y trabajo activo limitado al EDA y al arnés. |
