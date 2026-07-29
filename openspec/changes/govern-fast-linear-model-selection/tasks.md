## 1. Definir el protocolo lineal

- [x] 1.1 [Datos / ML] Versionar el perfil de dos fases: muestra agrupada determinista de hasta 50.000 filas, tres folds y 30 trials para búsqueda lineal; CV completa de cinco folds con parámetros congelados. Evidencia: `config/cfpb_fast_linear_selection_policy.json` validado con `python -m json.tool`; fija LogisticRegression, semilla 42, aislamiento de validation/test, ausencia de retuning en fase B y prohibición de Champion automático.
- [x] 1.2 [Datos / ML] Adaptar el ejecutor aislado para aceptar solo LogisticRegression, `train.parquet` y `narrative_hash`; rechazar validation, test, XGBoost/RF y retuning en la fase completa. Evidencia: `python -m py_compile scripts/ml/evaluate_model_selection.py` y `python -m unittest tests.unit.test_model_selection -v` superados (6 pruebas); el ejecutor distingue `search` y `full_cv`, valida política y mantiene la ejecución inactiva.

## 2. Generar evidencia privada

- [x] 2.1 [Datos / ML] Implementar salida agregada de búsqueda con semillas, presupuesto, parámetros, coste y limitaciones por clase, sin narrativas ni datos brutos. Evidencia: `reports/validation/cfpb_fast_linear_search.schema.json` y `tests/unit/test_fast_linear_search_schema.py`; JSON válido y 4 pruebas sintéticas superadas, incluidas fronteras de validation/test, Champion y campos no estructurados.
- [x] 2.2 [Datos / ML] Implementar salida de CV completa con macro F1 train/fold, desviación, gap estricto, coste y métricas de las once clases. Evidencia: `reports/validation/cfpb_fast_linear_full_cv.schema.json` y `tests/unit/test_fast_linear_full_cv_schema.py`; JSON válido y 4 pruebas sintéticas superadas, incluidas once clases, gap igual a 0.05, retuning, partitions reservadas y Champion.
- [ ] 2.3 [Tests / QA] Añadir pruebas sintéticas de aislamiento, grupos, parámetros congelados, once clases, gap, ausencia de Champion y prohibición de test. Evidencia: comando unitario focalizado superado.

## 3. Ejecutar con revisión humana

- [ ] 3.1 [Miguel / coordinación] Registrar la aprobación humana de entorno y presupuesto antes de fase A; no ejecutar si la aprobación falta.
- [ ] 3.2 [Datos / ML] Ejecutar fase A en entorno aprobado, versionar solo evidencia agregada y congelar parámetros si la salida es válida.
- [ ] 3.3 [Datos / ML] Ejecutar fase B sobre todo `train.parquet` con los parámetros congelados, sin retuning; generar evidencia agregada o registrar ejecución incompleta.
- [ ] 3.4 [Miguel / Datos] Revisar resultados y, solo si cumplen, permitir una única confirmación contra validation sin retuning ni test; no declarar Champion.

## 4. Cerrar con evidencia real

- [ ] 4.1 [Verificación] Ejecutar pruebas directas, quality gates afectados, `git diff --check` y validación estricta del cambio.
- [ ] 4.2 [Documentación] Actualizar evidencia y documentos canónicos solo si MED-02/MED-03 quedan realmente satisfechos; conservar límites y estado no Champion.
- [ ] 4.3 [Miguel / coordinación] Actualizar Jira PG-11, preparar PR hacia `dev` y no archivar sin revisión humana.
