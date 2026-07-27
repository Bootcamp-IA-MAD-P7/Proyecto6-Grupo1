## 1. Dependencias y preparación

- [x] 1.1 [Datos / ML] Añadir scikit-learn y sus dependencias a `pyproject.toml`. Verificación: `pip install -e .` y `python -c "import sklearn; print(sklearn.__version__)"`.
- [x] 1.2 [Datos / ML] Verificar que las particiones locales existen en `data/processed/` y contienen las columnas esperadas. Verificación: `python -c "import polars as pl; df = pl.read_parquet('data/processed/cfpb_training.parquet'); print(df.columns, df.shape)"`.
- [x] 1.3 [Datos / ML] Crear fixtures sintéticos para tests: CSV pequeño con narrativas sintéticas de 11 clases y el mismo esquema que el corpus real. Verificación: el fixture se carga con Polars y contiene las once clases canónicas.

## 2. Pipeline de entrenamiento baseline

- [x] 2.1 [Datos / ML] Crear `scripts/ml/train_baseline.py` con: carga de particiones, vectorización TF-IDF (unigrama, max_features=10000, stop_words='english') y LogisticRegression (multinomial, lbfgs, balanced, max_iter=1000, random_state=42). Verificación: el script se ejecuta sin errores sobre las particiones locales y produce un archivo `models/cfpb_baseline.pkl` (gitignored).
- [x] 2.2 [Datos / ML] Evaluar sobre validation: calcular macro F1, accuracy, precision, recall y F1 por clase. Verificación: las métricas se imprimen en consola y se guardan en `reports/validation/cfpb_baseline_metrics.json`.
- [x] 2.3 [Datos / ML] Calcular gap train/validation en macro F1 y verificar que es < 0.05. Verificación: el script muestra `GAP: X.XX` y advierte si supera el umbral. Gap real: 0.078 (supera 0.05, requiere regularización en iteración posterior).
- [x] 2.4 [Datos / ML] Identificar y reportar clases débiles (F1 < 0.5) con su soporte. Verificación: el reporte JSON contiene `weak_classes` con lista de clases y soporte: Debt or credit management (0.07, 620), Payday loan (0.44, 2176), Prepaid card (0.45, 1022).

## 3. Tests

- [x] 3.1 [Datos / ML] Crear `tests/unit/test_cfpb_baseline.py` con tests sintéticos: forma de salida (n, 11), cobertura de once clases, gap < 0.05 sobre fixture pequeño, reproducibilidad con misma semilla. Verificación: `python -m unittest tests.unit.test_cfpb_baseline -v` con 0 fallos.
- [x] 3.2 [Datos / ML] Verificar que el modelo entrenado está en `models/` y `git check-ignore` lo confirma. Verificación: `git check-ignore models/cfpb_baseline.pkl` devuelve el path.
- [x] 3.3 [Datos / ML] Verificar que el reporte JSON no contiene narrativas ni identificadores. Verificación: el JSON solo tiene claves de métricas, config y versiones.

## 4. Validación y cierre

- [x] 4.1 [Datos / ML] Ejecutar comprobaciones transversales: `ruff check scripts/ tests/`, `python -m unittest discover -s tests`, `python scripts/quality/check_repository.py`, `git diff --check`. Verificación: todos pasan.
- [x] 4.2 [Datos / ML] Validar con OpenSpec estricto. Verificación: `npm exec -- openspec validate train-cfpb-baseline --type change --strict` sin errores.
- [x] 4.3 [Miguel / coordinación] Actualizar README, changelog, daily, fuentes NotebookLM y estado Jira PG-3. Verificación: los documentos reflejan que el baseline está entrenado.
- [x] 4.4 [Miguel / coordinación] Archivar el cambio y preparar PR. Verificación: `npm exec -- openspec archive train-cfpb-baseline --yes` y PR hacia dev con plantilla completada.
