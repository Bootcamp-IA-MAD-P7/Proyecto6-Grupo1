# Equipo

## Integrantes

| Integrante | Rol principal | Rol de respaldo | Estado |
|---|---|---|---|
<<<<<<< HEAD
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
=======
| José | Backend | Por acordar | Activo |
| Abel | Frontend y UX | Por acordar | Activo |
| Víctor | Datos y EDA | Por acordar | Activo |
| Miguel | Arquitectura, OpenSpec, arnés y coordinación transversal | Por acordar | Activo |

Los roles principales reflejan el acuerdo actual. Los respaldos y la cobertura estable de producto, MLOps y QA siguen pendientes; no deben asignarse por suposición.

## Asignaciones vigentes

| Área | Persona | Referencia | Estado |
|---|---|---|---|
| Datos y EDA | Víctor | `PG-2` · `001/T-004` | En curso y asignada en Jira |
| Arquitectura y arnés | Miguel | `integrate-jira-workflow` · excepción `bootstrap` | Activa |
| Frontend y UX | Abel | `PG-4` · `003/T-006` | En curso y asignada en Jira; desarrollo desde cero |
| Backend | José | `PG-5` · `003/T-007` | Bloqueada por `PG-2` y `PG-3` |

La tabla describe el estado de `dev`. Una rama o Pull Request abierta no se considera capacidad integrada ni cambia por sí sola estas asignaciones.
>>>>>>> 5558ae2204151767a53be0e45102bd04a3b6da83

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
