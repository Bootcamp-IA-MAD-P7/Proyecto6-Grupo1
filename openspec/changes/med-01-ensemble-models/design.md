## Context

El baseline (PG-3) está entrenado y archivado con TF-IDF + LogisticRegression sobre 1.998.965 filas (split temporal 70/15/15). El gap es 0.0482 y el macro F1 es 0.5973 en validation / 0.6625 en test.

El código del baseline está en `scripts/ml/train_baseline.py` con toda la lógica inline (vectorización, entrenamiento, evaluación en un solo script). Para MED-01 necesitamos código reutilizable que permita:

- Comparar múltiples modelos con el mismo pipeline de evaluación.
- Optimizar hiperparámetros con Optuna.
- Generar figuras (matriz confusión, feature importance) de forma reproducible.
- Escalar a MED-02 (validación cruzada), MED-03 (más optimización), ADV/EXP (A/B testing, data drift) sin reescribir.

## Goals / Non-Goals

**Goals:**
- Crear `src/ml/` con módulos reutilizables: vectorizador, modelos, evaluación, tuning, visualización.
- Refactorizar `train_baseline.py` para usar `src/ml/`.
- Entrenar Random Forest (con defaults, rápido) y XGBoost (con Optuna + regularización) como ensemble.
- Generar informe comparativo (tabla LR + RF + XGBoost + figuras).
- Tests unitarios y de integración.

**Non-Goals:**
- Validación cruzada estratificada (MED-02).
- Despliegue, backend o API (PG-5 / PG-6).
- Data drift o A/B testing (ADV/EXP).
- LightGBM u otros modelos (solo RF + XGBoost, el foco de optimización es XGBoost).
- Modificar el split temporal, contrato de clases o política de entrenamiento.

## Decisions

### Arquitectura modular en `src/ml/`
Se crean 5 módulos independientes, cada uno con una responsabilidad única y configurable desde diccionarios. Esto permite reutilizarlos en cualquier script de entrenamiento, validación cruzada o inferencia.

### Random Forest + XGBoost como modelos ensemble
Se eligen por ser los estándar para clasificación multiclase sobre TF-IDF. RF es robusto y paralelizable; XGBoost suele dar mejor accuracy. RF se entrena con parámetros por defecto (sin tuning) para mantener la comparativa en la tabla; el foco de optimización recae en XGBoost. Alternativa considerada: LightGBM. Se descarta por ahora porque la ganancia sobre XGBoost es marginal y añade otra dependencia.

### Optuna para optimización de hiperparámetros con regularización
Se elige Optuna sobre GridSearchCV porque:
- Es más eficiente (TPE vs fuerza bruta).
- Soporta early stopping.
- Se integra bien con XGBoost (pruning).
- Escala a MED-03 sin cambios arquitectónicos.
- El espacio de búsqueda incluye `reg_lambda`, `reg_alpha` y `min_child_weight` para controlar overfitting.

### Estrategia sample → full para XGBoost
Para evitar tiempos de ejecución largos (Optuna sobre 1.4M filas puede tardar horas), el tuning de XGBoost se ejecuta sobre un sample de 100K filas con 40 trials. Los mejores hiperparámetros se usan para reentrenar con el dataset completo (1.4M) usando early_stopping sobre validation. Esto permite optimizar en ~10 min en lugar de ~2h.

### Refactor del baseline
`train_baseline.py` se refactoriza para usar `src/ml/vectorizer.py` (TF-IDF) y `src/ml/evaluation.py` (métricas). La LogisticRegression sigue inline porque es específica del baseline y no necesita Optuna. Esto minimiza el riesgo de romper el baseline ya verificado.

### Configuración desde diccionario
Cada clase acepta un dict de configuración (`config: dict`) en lugar de decenas de parámetros posicionales. Esto facilita serialización, logging y reproducción.

### Artefactos en formato joblib
Se usa `joblib.dump` en lugar de `pickle.dump` para persistir modelos y pipelines. Joblib es más eficiente con arrays grandes de numpy/scipy y es el formato recomendado por sklearn.

## Risks / Trade-offs

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Optuna 40 trials sobre sample 100K puede no encontrar los mejores params para full dataset | Suboptimización | La regularización (reg_lambda, reg_alpha) escala bien de sample a full; early_stopping ajusta n_estimators automáticamente |
| XGBoost con sparse TF-IDF consume mucha RAM | OOM en local | max_depth bajo (3-8), subsample 0.8, reg_lambda alto |
| Refactor del baseline puede romper tests | Baseline no reproducible | Tests existentes deben pasar igual; se validan antes y después |
| Figuras con matplotlib pueden fallar sin display | CI sin headless | Usar `plt.switch_backend("Agg")` y guardar a archivo |
| RF sin tuning puede infraestimar su rendimiento | Comparativa injusta | Se documenta que RF usa defaults; el foco de optimización es XGBoost |

## Migration Plan

1. Añadir dependencias (`xgboost`, `optuna`) a `pyproject.toml`.
2. Crear `src/ml/__init__.py` y módulos (vectorizer, evaluation, models, tuning, visualization).
3. Refactorizar `scripts/ml/train_baseline.py`.
4. Crear `scripts/ml/train_ensemble.py`.
5. Ejecutar entrenamiento local, generar reportes y figuras.
6. Tests.
7. Documentación y cierre.

Rollback: revertir el commit y eliminar `models/` local.

## Open Questions

- Ninguna.
