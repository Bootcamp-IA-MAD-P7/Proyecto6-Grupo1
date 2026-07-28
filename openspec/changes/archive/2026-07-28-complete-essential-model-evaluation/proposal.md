## Why

El proyecto ya dispone de un baseline reproducible, comparativas de ensembles
sobre una muestra y una integración local entre ClaimVox y el servicio de
inferencia. Sin embargo, el nivel esencial no puede declararse completo hasta
seleccionar de forma gobernada un modelo final evaluable y producir evidencia
completa sobre el split aprobado: matriz de confusión, importancia de variables,
análisis agregado de errores e informe técnico reproducible.

Este cambio concentra esa última evaluación para evitar mezclar resultados de
muestras exploratorias con la evidencia final. Su resultado debe permitir cerrar
`ESS-01`, `ESS-07`, `ESS-08`, `ESS-09` y `ESS-10`, solo si cada criterio cumple
su evidencia mínima.

## What Changes

- Define una selección de candidato basada únicamente en validation, respetando
  el test protegido y el umbral aprobado de overfitting.
- Ejecuta la evaluación final reproducible del candidato elegible sobre el split
  completo, con artefacto local ignorado por Git y manifiestos agregados
  versionables.
- Produce matriz de confusión, importancia de variables compatible con el
  modelo seleccionado y análisis de errores agregado por clase, sin narrativas
  CFPB.
- Publica un informe técnico y una guía de ejecución que enlacen datos,
  decisiones, métricas, limitaciones, backend local y ClaimVox.
- Actualiza los criterios de entrega y la documentación solo cuando la evidencia
  real permita verificarlos.

## Capabilities

### New Capabilities

- `essential-model-evaluation`: selección gobernada, evaluación final y
  evidencia reproducible del modelo multiclase esencial.
- `essential-delivery-report`: informe técnico y guía reproducible para la
  entrega esencial.

### Modified Capabilities

- `cfpb-baseline`: amplía la evaluación del baseline o candidato seleccionado
  con artefacto final, predicciones válidas y evidencia de cierre.
- `complaint-routing-interface`: documenta la compatibilidad de ClaimVox con el
  artefacto de modelo seleccionado, sin cambiar su revisión humana ni convertir
  la integración local en despliegue.

## Impact

- Jira: `PG-7` como seguimiento operativo de métricas, análisis de errores e
  informe final.
- ML: scripts de entrenamiento/evaluación, módulos reutilizables, tests y
  reportes agregados bajo `reports/validation/`.
- Producto: la PWA y el backend local solo consumirán un contrato de modelo
  compatible; no se añadirá autenticación, persistencia ni despliegue.
- Privacidad: no se versionarán narrativas, datasets, predicciones por fila ni
  binarios de modelos; los artefactos de modelo permanecen locales e ignorados.

## Tracking

- Jira: `PG-7`.
