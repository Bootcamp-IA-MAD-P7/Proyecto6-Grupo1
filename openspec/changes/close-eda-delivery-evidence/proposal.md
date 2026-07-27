## Why

El EDA CFPB ya dispone de código reproducible, informe agregado, cuatro figuras
versionadas y decisiones posteriores de preparación. Sin embargo, `ESS-02`
continúa en curso porque el informe no explica expresamente por qué una matriz
de correlación no es pertinente para una entrada de texto y no enlaza sus
hallazgos con el cierre versionado de idioma, duplicados, partición y
desbalanceo.

Este cambio completa únicamente esa trazabilidad para poder decidir con
evidencia si `ESS-02` alcanza su definición mínima, sin reejecutar ni ampliar
el EDA.

## Tracking

- Jira: `PG-2`.

## What Changes

- Añadir al informe EDA una justificación explícita de las visualizaciones
  pertinentes para texto multiclase y de la no aplicabilidad de una correlación
  numérica convencional.
- Enlazar los hallazgos del EDA con la política aprobada de idioma, grupos,
  partición temporal y pesos balanceados, conservando la distinción entre la
  instantánea EDA y la fuente posterior de entrenamiento.
- Verificar la presencia y trazabilidad de las cuatro figuras agregadas, el
  notebook reproducible y las conclusiones sin incorporar narrativas reales.
- Actualizar los documentos de estado, niveles de entrega y fuentes de
  NotebookLM solo si la evidencia satisface `ESS-02`.

## Capabilities

### New Capabilities

- `eda-delivery-evidence`: define la evidencia mínima y la comunicación
  verificable para declarar completado el EDA orientado a clasificación
  multiclase.

### Modified Capabilities

- Ninguna.

## Impact

- Afecta documentación y evidencia agregada: `reports/validation/cfpb_eda.md`,
  criterios de entrega, README, changelog, daily y fuentes de NotebookLM.
- No modifica el notebook, conversor, corpus local, particiones, modelo,
  métricas, interfaz, backend, dependencias ni infraestructura.
- Contribuye únicamente a `ESS-02`. No modifica los estados de `ESS-01`,
  `ESS-03` a `ESS-10`, ni crea inferencia real.
- Mantiene los límites de privacidad: sin narrativas CFPB, datos brutos,
  identificadores, artefactos locales, credenciales o logs sensibles.
