## Why

La documentación canónica de ClaimVox contiene contradicciones con el estado
integrado en `dev`: todavía niega capacidades locales verificadas, presenta un
resumen avanzado obsoleto y enlaza un gráfico anterior al corte actual. Antes
del relevo al equipo, el repositorio necesita una auditoría reproducible que
separe con claridad lo implementado, lo verificado y lo pendiente.

## What Changes

- Auditar de forma proporcional Git, OpenSpec, aplicación, ML, pruebas,
  seguridad, CI y evidencias versionadas, corrigiendo únicamente defectos
  reproducibles y seguros.
- Reconciliar README, contexto operativo, intención, niveles de entrega,
  arquitectura, seguridad, API, NotebookLM, presentación, daily y changelog
  contra las fuentes de verdad vigentes.
- Sustituir el resumen visual obsoleto por un gráfico accesible fechado que
  represente los 25 criterios: 15 verificados, 3 en curso y 7 no iniciados.
- Mantener explícitos los límites: ejecución local, sin Champion seleccionado,
  Docker, base compartida, autenticación, despliegue ni MLOps.
- Conservar como históricos los cambios archivados, dailies e informes de
  cortes anteriores, sin reescribir sus afirmaciones en retrospectiva.
- No incorporar datasets, narrativas CFPB, artefactos de modelo, credenciales
  ni resultados locales no versionados.

Resultados medibles:

- README y fuentes canónicas coinciden con
  `docs/project_management/delivery_levels.md`.
- Los enlaces y activos documentales activos existen y superan las puertas de
  calidad del repositorio.
- `ESS-01` a `ESS-10`, `MED-01`, `MED-04` y `ADV-04` a `ADV-06` conservan su
  estado verificado; `MED-02`, `MED-03` y `MED-05` permanecen en curso.
- Las comprobaciones focalizadas y la validación OpenSpec finalizan sin fallos.

No objetivos: ejecutar entrenamiento completo, seleccionar o promover un
Champion, incorporar ramas no fusionadas, dockerizar, crear una base de datos,
desplegar, cambiar contratos públicos o publicar una release.

## Tracking

- Jira: `PG-9`.

## Capabilities

### New Capabilities

Ninguna.

### Modified Capabilities

- `project-state-documentation`: exigir que el inventario documental activo,
  los resúmenes visuales y las afirmaciones de capacidad se validen contra
  evidencia versionada y distingan alcance local de operación desplegada.
- `repository-presentation-quality`: exigir que el gráfico activo y los
  conteos resumidos del README se comprueben automáticamente contra el estado
  canónico de los niveles de entrega.

## Impact

- Documentación activa del repositorio, fuentes de NotebookLM, daily, catálogo
  de activos y changelog.
- Activos SVG de estado y comprobaciones documentales del repositorio.
- No cambia APIs, contratos de predicción o feedback, dependencias, datos,
  modelos ni infraestructura.
- Impacto de privacidad positivo: se refuerza la prohibición de incorporar
  narrativas, datos brutos, binarios, credenciales o artefactos locales.
