## Why

El piloto de PG-11 confirmó la viabilidad técnica, pero su alcance limitado no
verifica `MED-02` ni `MED-03`. Es necesario ejecutar una evaluación gobernada
con evidencia suficiente de validación cruzada y optimización reproducible,
sin debilitar el aislamiento de las particiones ni usar el test protegido para
seleccionar.

## What Changes

- Definir una ejecución de evaluación completa, acotada y reproducible sobre la
  partición `train` aprobada, con control de `narrative_hash`.
- Registrar estrategia de folds, semillas, resultados macro F1 por fold,
  variabilidad, coste y gap train-validación para candidatos autorizados.
- Ejecutar una búsqueda de hiperparámetros acotada que use únicamente folds de
  entrenamiento y produzca evidencia agregada versionable.
- Aplicar la regla de decisión aprobada y una revisión humana, que puede dejar
  explícitamente el resultado sin selección aprobada.
- Actualizar `MED-02` y `MED-03` solo si la evidencia mínima se obtiene; no
  crear ni promover un Champion.

## Capabilities

### New Capabilities

- `complete-governed-model-selection-evaluation`: evaluación estratificada y
  optimización reproducible de candidatos de clasificación, con evidencia
  agregada y frontera estricta respecto a validation reservada y test protegido.

### Modified Capabilities

- Ninguna.

## Impact

- Afectará el ejecutor aislado de selección, la integración de tuning, pruebas
  directas y evidencias agregadas de selección de modelo.
- Consumirá únicamente las particiones locales aprobadas y podrá requerir un
  entorno de cómputo explícitamente autorizado.
- No modifica la API, ClaimVox, contratos de predicción, datos versionados,
  despliegue, autenticación, feedback ni la condición de revisión humana.

## Tracking

- Jira: `PG-11`.
- Criterios de entrega: `MED-02` y `MED-03`.
