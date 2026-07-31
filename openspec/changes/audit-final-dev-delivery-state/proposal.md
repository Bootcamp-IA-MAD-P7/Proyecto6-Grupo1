## Why

`dev` incorpora cambios recientes de Docker, PostgreSQL y estado operativo que
todavía no están reconciliados con README, niveles de entrega, fuentes de
NotebookLM y gráficos. Es necesaria una auditoría final basada en evidencia para
que el repositorio describa con precisión lo integrado, lo verificable y lo que
continúa pendiente antes de cualquier cierre o presentación.

## What Changes

- Auditar el SHA vigente de `origin/dev`, sus Pull Requests y las ramas que no
  están contenidas en la rama integrada.
- Verificar localmente frontend, backend, baseline, feedback, persistencia,
  Docker y contratos sin entrenar modelos ni usar narrativas CFPB reales.
- Reconciliar los 25 criterios `ESS`, `MED`, `ADV` y `EXP` exclusivamente con
  evidencia versionada y comprobaciones reproducibles.
- Actualizar las fuentes documentales activas, el paquete NotebookLM y el
  gráfico de estado vigente, conservando los cortes históricos.
- Crear una evidencia agregada y fechada de la auditoría.
- Corregir únicamente inconsistencias seguras encontradas durante la revisión.

Resultados medibles:

- `dev` queda auditado contra un SHA explícito.
- Los 25 criterios y el gráfico activo presentan los mismos estados.
- README, AGENTS, intent, changelog y NotebookLM no contradicen las capacidades
  realmente integradas.
- Las suites y quality gates aplicables quedan registrados con resultados
  reales.

No objetivos:

- seleccionar o presentar un Champion;
- completar `MED-02`, `MED-03` o `MED-05` sin su evidencia mínima;
- acreditar cloud, observabilidad o MLOps sin smoke, rollback y evidencia;
- entrenar, retunar o ejecutar validación cruzada;
- fusionar o eliminar ramas;
- publicar en `main`, crear tags o releases.

Niveles afectados: documentación y posible reevaluación basada en evidencia de
`ADV-01` y `ADV-02`; revisión sin cierre automático de `MED-02`, `MED-03`,
`MED-05`, `ADV-03` y `EXP-01` a `EXP-04`.

Privacidad y seguridad: la auditoría utilizará únicamente evidencia agregada y
fixtures sintéticos. No versionará narrativas, datos, credenciales, modelos,
logs sensibles ni artefactos locales.

## Capabilities

### New Capabilities

Ninguna.

### Modified Capabilities

- `project-state-documentation`: exigir que la auditoría final reconcilie el
  estado integrado de Git, capacidades, niveles, NotebookLM y límites
  operativos contra evidencia versionada.
- `repository-presentation-quality`: exigir que el gráfico activo y los
  resúmenes profesionales reflejen el corte auditado y conserven los cortes
  históricos.

## Impact

- Documentación activa del repositorio, fuentes de NotebookLM, evidencia de
  validación y activos gráficos.
- Artefactos del cambio OpenSpec `audit-final-dev-delivery-state`.
- Posibles correcciones mínimas de documentación o código si una prueba
  reproduce una inconsistencia segura dentro del alcance.
- Sin cambios intencionados en contratos de predicción, datos, modelos,
  secretos, infraestructura desplegada ni ramas remotas.

## Tracking

- Jira: `PG-16`.
