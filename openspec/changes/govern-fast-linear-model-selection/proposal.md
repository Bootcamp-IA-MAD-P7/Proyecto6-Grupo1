## Why

La ejecución XGBoost completa aprobada para PG-11 no es proporcional al entorno
disponible: el piloto de 20.000 filas ya consumió más de cuatro horas. El
baseline TF-IDF + LogisticRegression existente permite obtener evidencia real de
`MED-02` y `MED-03` con el mismo aislamiento de datos, en un presupuesto que
puede ejecutarse y revisarse.

## What Changes

- Definir una selección gobernada de dos fases para el candidato lineal ya
  evaluado: Optuna acotado sobre una muestra agrupada de `train`, seguido de CV
  agrupada de cinco folds sobre todo `train` con parámetros congelados.
- Registrar semillas, configuración, macro F1 de train y fold, variabilidad,
  coste, gap y métricas de las once clases en evidencia agregada.
- Mantener `validation` para una única confirmación posterior a la revisión
  humana y excluir absolutamente `test` de búsqueda, selección y diagnóstico.
- Mantener XGBoost, Random Forest y LightGBM como comparaciones históricas de
  `MED-01`, no como ruta obligatoria de esta entrega.

## Capabilities

### New Capabilities

- `fast-linear-governed-model-selection`: selección reproducible y de dos fases
  del baseline lineal, con CV completa agrupada y evidencia privada.

### Modified Capabilities

- Ninguna.

## Impact

- Afectará la política y el ejecutor aislado de PG-11, pruebas sintéticas y
  reportes agregados de selección.
- No modifica la API, ClaimVox, el artefacto local de inferencia, los contratos
  de predicción, despliegue, autenticación ni feedback.
- No declara Champion; el baseline local puede seguir siendo modelo de servicio
  mientras la revisión humana no apruebe una selección posterior.

## Tracking

- Jira: `PG-11`.
- Criterios: `MED-02` y `MED-03`.
