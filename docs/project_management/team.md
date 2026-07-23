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
| Datos y EDA | Víctor | `001-cfpb-target-contract/T-004` | Activa |
| Arquitectura y arnés | Miguel | `openspec-governance` | Operativo; mantenimiento y coordinación |
| Frontend y UX | Abel | `003-complaint-routing-experience/T-006` | Activa; desarrollo desde cero |
| Backend | José | `003-complaint-routing-experience/T-007` | Bloqueada por datos y modelo |

La tabla describe el estado de `dev`. Una rama o Pull Request abierta no se considera capacidad integrada ni cambia por sí sola estas asignaciones.

## Acuerdo de trabajo con IA

- Cada integrante puede utilizar la herramienta de IA que considere adecuada.
- El repositorio, Jira, OpenSpec y las Pull Requests son el contexto compartido.
- Cada integrante instala las herramientas del propio clon mediante `npm ci`; no depende de archivos preparados por otra persona.
- La persona asignada conserva la responsabilidad de revisar código, datos, decisiones y evidencias.
- No se comparten narrativas CFPB, secretos o datos brutos con servicios externos.
- El [flujo operativo](workflow.md) explica cómo preparar contexto y cerrar una tarea.

## Cambios de composición

| Fecha | Integrante | Cambio |
|---|---|---|
| 2026-07-22 | Josué | Baja del Bootcamp comunicada; deja de formar parte del equipo activo. |
| 2026-07-23 | Equipo activo | Responsabilidades principales confirmadas y trabajo activo limitado al EDA y al arnés. |
