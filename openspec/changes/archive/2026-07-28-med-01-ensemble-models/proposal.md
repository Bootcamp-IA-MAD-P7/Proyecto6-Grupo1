## Why

PG-3 ha cerrado el baseline (TF-IDF + LogisticRegression) con gap 0.0482 y macro F1 0.5973/0.6625 (val/test). MED-01 es el siguiente nivel de entrega: comparar modelos ensemble (Random Forest, XGBoost) contra ese baseline, añadiendo matriz de confusión, feature importance, optimización con Optuna y un informe comparativo. Esto desbloquea ESS-07, ESS-08 y parte de ESS-10.

## What Changes

- Añadir `xgboost` y `optuna` como dependencias.
- Crear `src/ml/` con módulos reutilizables: vectorizador, modelos, evaluación, tuning, visualización.
- Refactorizar `scripts/ml/train_baseline.py` para que use los módulos de `src/ml/` en lugar de lógica inline.
- Crear `scripts/ml/train_ensemble.py` que entrena RF + XGBoost, optimiza con Optuna y genera reporte.
- Generar `reports/validation/med_01_comparison.md` con tabla comparativa de los 3 modelos.
- Generar figuras: matriz de confusión, feature importance, barras de comparación.
- Tests unitarios y de integración para los nuevos modelos y pipeline.
- Actualizar README, CHANGELOG y delivery_levels.md (MED-01 → `En curso`).

## Capabilities

### New Capabilities
- `ensemble-models`: entrenar, optimizar y comparar modelos ensemble (RF + XGBoost) contra el baseline CFPB, con matriz de confusión, feature importance e informe comparativo.

### Modified Capabilities
- `cfpb-baseline`: el pipeline baseline se refactoriza para compartir código con los modelos ensemble a través de `src/ml/`.

## Impact

- Dependencias: se añaden `xgboost` y `optuna` a `pyproject.toml`.
- Código: nueva carpeta `src/ml/` con 5 módulos reutilizables; refactor de `scripts/ml/train_baseline.py`.
- Privacidad: las figuras solo contienen métricas agregadas, no narrativas.
- Seguridad: sin cambios.

## Tracking

- Jira: `PG-8`.
