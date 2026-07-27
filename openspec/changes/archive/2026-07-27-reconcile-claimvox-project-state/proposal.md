## Why

La PR #28 integró en `dev` una evolución real de la interfaz React PWA: la
identidad visible pasa a ser ClaimVox y se incorporan preferencias de tema,
mejoras visuales y ajustes de accesibilidad. Parte del contexto que consumen
las personas, Jira y el arnés todavía describe el estado anterior de frontend
y sitúa a Víctor en un trabajo de datos ya cerrado, por lo que una IA nueva
podría recibir instrucciones contradictorias.

Esta reconciliación mantiene una fuente de verdad comprensible sin convertir el
prototipo en una capacidad que aún no existe. El resultado verificable es que
la documentación afectada diferencie con precisión el prototipo ClaimVox, el
baseline pendiente de `PG-3` y los límites vigentes de producto.

## What Changes

- Alinear el estado general, la identidad de la interfaz y sus límites en el
  README, sin presentar el mock como modelo, backend o producto operativo.
- Actualizar el contexto operativo entregado por `AGENTS.md`, la guía de Jira y
  el reparto de equipo para reflejar `PG-2` terminado, `PG-3` como siguiente
  hito de datos y `PG-4` integrado con la PR #28.
- Completar la daily del 27 de julio con contribuciones reales, coordinación,
  responsabilidades vigentes y bloqueos, sin inventar actividad o autoría.
- Sincronizar CHANGELOG, fuentes de NotebookLM y estado técnico solo cuando su
  significado haya cambiado, manteniendo una narrativa apta para cliente.
- Registrar la trazabilidad documental con `PG-4`, la PR #28 y el cambio
  archivado `integrate-frontend-foundation`.

### Non-goals

- No se modifica React, estilos, PWA, contratos, dependencias, código de datos
  ni infraestructura.
- No se cambian estados, asignaciones o bloqueos directamente en Jira.
- No se entrena ni evalúa un modelo, ni se implementan backend, inferencia,
  persistencia, despliegue o MLOps.
- No se inventan resultados, métricas, evidencias, revisiones manuales o
  contribuciones de integrantes.

## Capabilities

### New Capabilities

- `project-state-documentation`: documentación operativa y de presentación que
  mantiene alineados el estado integrado de GitHub, las referencias Jira y los
  límites del producto sin sustituir las evidencias técnicas.

### Modified Capabilities

- `openspec-governance`: el contexto operativo consumido por OpenSpec y el
  arnés debe conservar referencias vigentes de trabajo, responsables y límites
  tras una integración revisada.
- `complaint-routing-interface`: la documentación de la interfaz debe nombrar
  su identidad actual y mantener explícito que sus respuestas, autenticación y
  administración no son capacidades operativas.

## Impact

- Afecta documentación raíz, gobierno del proyecto, daily y fuentes de
  NotebookLM; no afecta APIs, contratos, dependencias, datos ni artefactos de
  aplicación.
- Contribuye indirectamente a `ESS-04` al comunicar correctamente el
  prototipo, pero no permite verificarlo: sigue faltando inferencia real de
  extremo a extremo.
- El impacto de privacidad es editorial: se conserva la prohibición de incluir
  narrativas CFPB reales, datos brutos, secretos o logs sensibles en cualquier
  documento o paquete de contexto.

## Tracking

- Jira: `PG-4`.
- Origen documental: PR #28 y
  `2026-07-24-integrate-frontend-foundation` archivado.
