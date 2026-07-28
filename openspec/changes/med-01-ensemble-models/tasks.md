## 1. Dependencias

- [x] 1.1 [ML] Añadir `xgboost>=2.1.0` y `optuna>=4.0.0` a `pyproject.toml`. Verificación: `pip install -e .` y `python -c "import xgboost; import optuna; print(xgboost.__version__, optuna.__version__)"`.

## 2. Módulos reutilizables src/ml/

- [x] 2.1 [ML] Crear `src/ml/__init__.py` con el árbol de exportaciones. Verificación: `python -c "from src.ml import VectorizerConfig, evaluate, train_rf, train_xgb, tune_hyperparams, plot_confusion_matrix"`.
- [x] 2.2 [ML] Crear `src/ml/vectorizer.py` con clase `VectorizerConfig` que encapsula TfidfVectorizer configurable por diccionario. Verificación: importar, instanciar con config, fit_transform y transform sobre fixture sintético.
- [x] 2.3 [ML] Crear `src/ml/evaluation.py` con función `evaluate` que devuelve métricas (macro F1, weighted F1, accuracy, precision, recall, per-class, gap, weak classes) y genera reporte JSON. Verificación: ejecutar sobre predicciones sintéticas y comprobar la salida.
- [x] 2.4 [ML] Crear `src/ml/models.py` con funciones `train_rf` y `train_xgb` que aceptan X, y, config y devuelven modelo entrenado. Verificación: entrenar sobre fixture sintético y predecir.
- [x] 2.5 [ML] Crear `src/ml/tuning.py` con función `tune_hyperparams` que usa Optuna para buscar hiperparámetros de RF y XGBoost sobre validation. Verificación: ejecutar con pocos trials (n_trials=5) sobre fixture sintético.
- [x] 2.6 [ML] Crear `src/ml/visualization.py` con funciones `plot_confusion_matrix`, `plot_feature_importance` y `plot_model_comparison`. Verificación: generar PNG sobre fixture sintético.
- [x] 2.7 [ML] Añadir a `tuning.py` los parámetros de regularización `reg_lambda`, `reg_alpha`, `min_child_weight` al espacio de búsqueda de XGBoost. Verificación: el espacio de búsqueda incluye los 3 parámetros nuevos.
- [x] 2.8 [ML] Añadir `early_stopping_rounds=20` y `eval_set` a `train_xgb` en `models.py`. Verificación: `train_xgb` acepta `eval_set` opcional.

## 3. Refactor del baseline

- [x] 3.1 [ML] Refactorizar `scripts/ml/train_baseline.py` para usar `src/ml/vectorizer.py` y `src/ml/evaluation.py`. Verificación: los 6 tests existentes de baseline siguen pasando.
- [x] 3.2 [ML] Usar `joblib.dump` en `train_baseline.py` conservando el nombre de artefacto `cfpb_baseline.pkl` acordado con el backend. Verificación: `git check-ignore models/cfpb_baseline.pkl` devuelve el path.

## 4. Pipeline ensemble

- [x] 4.1 [ML] Crear `scripts/ml/train_ensemble.py` que: carga datos, vectoriza con `VectorizerConfig`, entrena RF (defaults) + XGBoost (Optuna con regularización + early_stopping), evalúa, genera figuras y guarda modelos en `.joblib`. Verificación: ejecutar sobre particiones locales y comprobar artefactos.

## 5. Ejecución y reportes

- [x] 5.1 [ML] Ejecutar `train_ensemble.py` sobre particiones reales y verificar que los modelos se guardan en `models/`. Verificación: `ls models/cfpb_rf.joblib models/cfpb_xgb.joblib` y `git check-ignore` los confirma.
- [x] 5.2 [ML] Verificar que `reports/validation/med_01_comparison.md` contiene tabla comparativa de los 3 modelos. Verificación: el archivo existe y tiene filas para LR, RF y XGBoost.
- [x] 5.3 [ML] Verificar que `reports/validation/figures/` contiene al menos 3 PNG (matriz confusión, feature importance, barras). Verificación: `ls reports/validation/figures/*.png`.

## 6. Tests

- [x] 6.1 [ML] Crear `tests/unit/test_ensemble_models.py` con tests: forma de salida, once clases, reproducibilidad, serialización. Verificación: `python -m unittest tests.unit.test_ensemble_models -v` con 0 fallos.
- [x] 6.2 [ML] Crear `tests/integration/test_ensemble_pipeline.py` con tests: pipeline completo sobre fixture sintético, comparación con baseline. Verificación: `python -m unittest tests.integration.test_ensemble_pipeline -v` con 0 fallos.

## 7. Documentación y cierre

- [x] 7.1 [ML] Actualizar README (MED-01 → `Verificado`), CHANGELOG, delivery_levels.md, SVG chart y NotebookLM. Verificación: `python scripts/quality/check_repository.py` sin errores.
- [x] 7.2 [ML] Ejecutar comprobaciones: `ruff check scripts/ src/ tests/`, `python -m unittest discover -s tests/unit -p "test_*.py" -v`, `python scripts/harness.py doctor`, `npm exec -- openspec validate --all --strict`. Verificación: todos pasan.
- [x] 7.3 [ML] Preparar la Pull Request con las limitaciones explícitas y las comprobaciones ejecutadas. Evidencia: PR #36 abierta; el archivo OpenSpec queda pendiente de la fusión y de una revisión humana posterior.
- [x] 7.4 [ML] Corregir la portabilidad de LightGBM: CPU por defecto, GPU opcional, y ejecutar las pruebas que reproducen el fallo de CI. Evidencia: `python -m unittest tests.unit.test_ensemble_models tests.integration.test_ensemble_pipeline -v` superado el 28 de julio de 2026 (20 pruebas, 0 fallos) sin OpenCL.
