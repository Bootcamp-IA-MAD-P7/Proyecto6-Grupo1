## 1. Preparar el protocolo

- [x] 1.1 [Datos / ML] Confirmar que los datos usados para CV pertenecen solo al conjunto de entrenamiento permitido y que se conserva la prevención de leakage vigente. Evidencia: `reports/validation/cfpb_model_selection_partition_review.md` confirma la partición temporal aislada por `narrative_hash`, el test protegido y la obligación de limitar CV a `train.parquet`.
- [x] 1.2 [Datos / ML] Definir y versionar la estrategia estratificada compatible, número de folds, semillas y presupuesto de ejecución antes de ejecutar candidatos. Evidencia: `config/cfpb_model_selection_policy.json` fija `StratifiedGroupKFold`, cinco folds, semilla `42` y 30 trials por candidato sin permitir el test protegido.
- [x] 1.3 [Datos / ML] Definir el formato agregado de resultados: macro F1 por fold, media, variabilidad, gap train-validación, coste y limitaciones por clase. Evidencia: `reports/validation/cfpb_model_selection_report.schema.json` fija el contrato agregado, excluye el test protegido y exige decisión humana.

## 2. Implementar evaluación gobernada

- [x] 2.1 [Datos / ML] Implementar un ejecutor aislado de PG-11 para ejecutar CV únicamente sobre `train.parquet` y `narrative_hash`, sin consultar validación reservada ni test protegido durante la selección. No reutilizar `scripts/ml/train_ensemble.py` como entrada de selección. Evidencia: `scripts/ml/evaluate_model_selection.py` rechaza corpus completo, validación y test; `python -m py_compile scripts/ml/evaluate_model_selection.py` superado.
- [x] 2.2 [Datos / ML] Integrar la búsqueda de hiperparámetros acotada con macro F1 como métrica primaria y registro de configuración, semillas y presupuesto. Evidencia: `src/ml/tuning.py` usa `StratifiedGroupKFold` y Optuna con los valores de la política; el ejecutor exige `--execute`. Compilación y `--help` superados sin entrenar.
- [x] 2.3 [Datos / ML] Implementar la regla de recomendación: gap inferior a `0.05`; dentro de la tolerancia de macro F1 `0.001`, menor variabilidad y coste; si no se cumple, registrar «sin selección aprobada». Evidencia: `recommend_candidate` superó una comprobación sintética sin entrenamiento; selecciona menor variabilidad dentro de la tolerancia y no consulta test.

## 3. Verificar y evidenciar

- [x] 3.1 [Tests / QA] Añadir o ajustar pruebas directas para impedir el uso del test protegido, comprobar semillas, estrategia de folds y la salida agregada. Evidencia: `python -m unittest tests.unit.test_model_selection -v` superado: 6 pruebas, 0 fallos; cubre entradas prohibidas, grupo, folds, semilla y decisión.
- [ ] 3.2 [Datos / ML] Ejecutar primero el piloto de viabilidad aprobado: 100.000 filas deterministas de `train.parquet`, 5 folds y 30 trials; generar solo evidencia agregada sin narrativas CFPB, datos brutos, binarios, credenciales ni logs sensibles. El piloto no verifica `MED-02` ni `MED-03`.
- [ ] 3.3 [Miguel / coordinación] Revisar humanamente la recomendación o la ausencia de selección, enlazar evidencias con `PG-11` y actualizar criterios `MED-02` y `MED-03` solo si su evidencia mínima queda satisfecha.

## 4. Cierre

- [ ] 4.1 [Verificación] Ejecutar las pruebas unitarias directamente afectadas, `git diff --check` y la validación estricta del cambio antes de preparar la Pull Request.
- [ ] 4.2 [Documentación] Actualizar únicamente la documentación cuyo significado cambie con resultados reales, límites y decisión; no presentar ningún candidato como Champion o desplegado sin aprobación y evidencia posterior.
