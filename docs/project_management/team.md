# Equipo

## Integrantes

| Integrante | Rol principal | Rol de respaldo | Estado |
|---|---|---|---|
| José | Backend | Pendiente de acordar | Activo |
| Abel | Frontend / UX | Pendiente de acordar | Activo |
| Víctor | Datos / EDA del CSV | Pendiente de acordar | Activo |
| Miguel | Arquitectura y coherencia transversal | Pendiente de acordar | Activo |

Estas responsabilidades fueron comunicadas el 22 de julio de 2026. Definen el área principal de coordinación, pero no autorizan trabajo que una spec mantenga bloqueado. Los roles de respaldo siguen pendientes para evitar silos y puntos únicos de conocimiento.

## Responsabilidades

### Miguel — Arquitectura

- Mantener límites, contratos y coherencia entre producto, datos, frontend, backend, seguridad y CI/CD.
- Coordinar specs, ADR y decisiones transversales.
- Revisar que README, changelog, dailies y fuentes de NotebookLM reflejen el estado real.
- No sustituir la validación de cada responsable de área.

### José — Backend

- Revisar el OpenAPI y preparar la futura implementación del servicio, validación de entrada, errores y health check.
- Mantener el backend desacoplado del modelo y respetar privacidad, trazabilidad y ausencia de persistencia por defecto.
- No integrar inferencia real hasta que `001/T-004` a `T-006` y el modelo lo permitan.

### Abel — Frontend / UX

- Mantener la React PWA en `app/interface/` y su cliente de inferencia sustituible.
- Revisar responsive, accesibilidad, instalabilidad, estados, capturas y calidad visual.
- No crear una aplicación `/frontend` paralela ni presentar mocks como predicciones reales.

### Víctor — Datos / EDA

- Estudiar el CSV conforme a `001-cfpb-target-contract`.
- Entregar evidencia agregada sobre clases, tiempo, ausencias, duplicados, conflictos, longitud, idioma y desbalanceo.
- No versionar ni compartir narrativas reales y no cambiar silenciosamente target, filtros o partición.

## Asignaciones operativas vigentes

| Integrante | Alcance | Referencia | Estado |
|---|---|---|---|
| Abel | Revisión y endurecimiento de la React PWA | `003/T-008`, PR #14 | En curso |
| Víctor | Análisis contratado del CSV y entrega de evidencia EDA | `001/T-004` | En curso |
| José | Revisión del contrato y preparación del backend | `003/T-007` | Asignado; implementación bloqueada |
| Miguel | Arquitectura, sincronización documental y gobierno | Specs activas y fuentes vivas | En curso |

Una asignación operativa concreta el trabajo inmediato, pero no levanta bloqueos, no sustituye los criterios de aceptación y no convierte una capacidad pendiente en implementada.

## Coordinación

- Jira comenzará a utilizarse el 23 de julio de 2026; el enlace se registrará cuando exista el proyecto.
- Jira refleja estado operativo; las specs y decisiones versionadas conservan el contrato.
- Cada responsable puede utilizar una IA distinta, pero debe entregar diff, verificaciones y evidencias revisadas.
- Las decisiones transversales se revisan con Miguel; la aceptación del resultado sigue perteneciendo al equipo.

## Acuerdo de trabajo con IA

- Cada integrante puede utilizar la herramienta de IA que considere adecuada.
- El repositorio, Jira, las specs y las Pull Requests son el contexto compartido.
- La persona asignada conserva la responsabilidad de revisar código, datos, decisiones y evidencias.
- No se comparten narrativas CFPB, secretos o datos brutos con servicios externos.
- El [flujo operativo](workflow.md) explica cómo preparar contexto y cerrar una tarea.

## Cambios de composición

| Fecha | Integrante | Cambio |
|---|---|---|
| 2026-07-22 | Josué | Baja del Bootcamp comunicada; deja de formar parte del equipo activo. |
