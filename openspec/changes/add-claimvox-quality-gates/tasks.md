## 1. Definir contratos de puertas de calidad

- [x] 1.1 [Quality Engineer] Inventariar los contratos existentes de datos, modelo y métricas que consumirá cada puerta, sin duplicar clases ni umbrales. Evidencia: `design.md` referencia `config/cfpb_target_contract.json`, `config/cfpb_training_policy.json` y `reports/validation/cfpb_baseline_metrics.json`; declara que no hay binario versionado y que el test protegido no participa en la puerta de métricas.
- [x] 1.2 [Quality Engineer] Versionar la configuración mínima de quality gates con rutas y umbrales aprobados, sin cambiar métricas, particiones ni políticas de entrenamiento. Evidencia: `config/cfpb_quality_gates.json` referencia los contratos canónicos, fija once clases, `narrative_hash`, raíz `models`, contrato de salida, campos agregados y gap estricto inferior a 0.05. Verificación: `python -m json.tool config/cfpb_quality_gates.json > /dev/null`.

## 2. Implementar puerta de integridad de datos

- [x] 2.1 [Quality Engineer] Implementar la validación local de esquema, clases, nulos críticos, duplicados conflictivos y separación de `narrative_hash` entre particiones mediante entradas explícitas y sin emitir textos de reclamaciones. Evidencia: `scripts/quality/cfpb_data_quality_gate.py`; `python -m py_compile scripts/quality/cfpb_data_quality_gate.py` superado. Los casos sintéticos se verifican en la tarea 2.2.
- [x] 2.2 [Tests / QA] Añadir fixtures y pruebas sintéticas que demuestren el rechazo de columna no autorizada, clase fuera del contrato, nulo crítico, duplicado conflictivo y fuga entre particiones. Evidencia: `tests/unit/test_cfpb_data_quality_gate.py`; `python -m unittest tests.unit.test_cfpb_data_quality_gate -v` superado: 6 pruebas, 0 fallos.

## 3. Implementar puerta del contrato de modelo

- [x] 3.1 [Quality Engineer] Implementar la validación de carga desde ubicación controlada, contrato de feature, forma de probabilidades, etiquetas canónicas e inferencia segura usando un artefacto sintético local temporal. Evidencia: `scripts/quality/cfpb_model_quality_gate.py` compila con `python -m py_compile scripts/quality/cfpb_model_quality_gate.py`; las pruebas sintéticas directas corresponden a la tarea 3.2.
- [x] 3.2 [Tests / QA] Añadir pruebas directas para artefacto no compatible, clase no autorizada, forma de salida inválida y entrada prohibida. Evidencia: `tests/unit/test_cfpb_model_quality_gate.py`; `python -m unittest tests.unit.test_cfpb_model_quality_gate -v` superado: 5 pruebas, 0 fallos.

## 4. Implementar puerta de métricas mínimas

- [x] 4.1 [Quality Engineer] Implementar la validación de reportes agregados contra campos y umbrales versionados para métricas por clase, agregados y gap train-validación, sin recalcular ni seleccionar modelos. Evidencia: `scripts/quality/cfpb_metrics_quality_gate.py` compila con `python -m py_compile scripts/quality/cfpb_metrics_quality_gate.py`; las pruebas sintéticas directas corresponden a la tarea 4.2.
- [x] 4.2 [Tests / QA] Añadir pruebas para evidencia incompleta, clase sin métricas obligatorias, uso prohibido del test protegido y salida privada sin narrativas. Evidencia: `tests/unit/test_cfpb_metrics_quality_gate.py`; `python -m unittest tests.unit.test_cfpb_metrics_quality_gate -v` superado: 5 pruebas, 0 fallos.

## 5. Verificar y cerrar

- [x] 5.1 [Quality Engineer] Ejecutar únicamente las pruebas unitarias afectadas, la validación estricta del cambio y `git diff --check`; registrar los resultados reales. Evidencia: `python -m unittest tests.unit.test_cfpb_data_quality_gate tests.unit.test_cfpb_model_quality_gate tests.unit.test_cfpb_metrics_quality_gate -v` superado: 16 pruebas, 0 fallos; `npm exec -- openspec validate add-claimvox-quality-gates --type change --strict` superado; sin entrenar modelos completos.
- [x] 5.2 [Documentation] Generar evidencia agregada de las puertas y actualizar solo `docs/project_management/delivery_levels.md`, README, CHANGELOG y fuentes NotebookLM si los criterios `ADV-04`, `ADV-05` o `ADV-06` quedan realmente verificados. Evidencia: `reports/validation/cfpb_quality_gates.md`, configuración versionada y 16 pruebas sintéticas directas; `ADV-04` a `ADV-06` quedan verificados como controles locales, no como entrenamiento, datos CFPB reales, persistencia, despliegue o MLOps.
- [ ] 5.3 [Miguel / coordinación] Preparar la Pull Request hacia `dev` con alcance, evidencia, límites y reversión; no fusionar ni archivar sin revisión humana.
