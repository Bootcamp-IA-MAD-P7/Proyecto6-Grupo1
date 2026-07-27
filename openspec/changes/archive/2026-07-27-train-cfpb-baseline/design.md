## Context

El repositorio dispone de un pipeline completo de preparación de datos que produce particiones train/validation/test (70/15/15) en `data/processed/cfpb_training.parquet` con 1.96M filas en inglés, once clases canónicas y política de overfitting. El contrato `config/cfpb_target_contract.json` y la política `config/cfpb_training_policy.json` están versionados y probados. Sin embargo, no existe código de entrenamiento ni evaluación.

PG-3 debe implementar el primer baseline evaluable sobre esas particiones, sin usar el test protegido para selección. El resultado alimentará ESS-01, ESS-03, ESS-05 y ESS-06 del nivel esencial.

### Constraints

- Única entrada: `complaint_what_happened` (texto).
- Once clases mutuamente excluyentes.
- No usar columnas prohibidas por el contrato.
- Gap overfitting < 0.05 en macro F1.
- Test protegido: no se usa para selección de modelo ni hiperparámetros.
- Artefactos locales ignorados por Git.
- Dependencias mínimas: scikit-learn.

## Goals / Non-Goals

**Goals:**
- Pipeline reproducible de vectorización TF-IDF + regresión logística multinomial.
- Evaluación sobre validation: macro F1, accuracy, precision, recall por clase.
- Reporte de métricas agregado sin narrativas.
- Tests de carga, forma de salida y clases.
- Artefacto modelo en `models/` gitignored.

**Non-Goals:**
- Seleccionar el modelo final (solo baseline).
- Optimizar hiperparámetros (queda para MED-03).
- Entrenar redes neuronales, ensemble o transformers (queda para EXP-01, MED-01).
- Desplegar el modelo o crear servicio de inferencia (PG-5).
- Modificar el contrato de clases, la política de entrenamiento o el split.
- Evaluar sobre test (reservado para evaluación final).

## Decisions

### TF-IDF unigrama como vectorización inicial
Se elige `TfidfVectorizer` con unigrama, max_features=10000, stop_words='english'. Alternativa considerada: Word2Vec o embeddings pre-entrenados. Se descartan porque añaden complejidad sin beneficio demostrado para un baseline, y TF-IDF ofrece interpretabilidad directa.

### Regresión logística multinomial como modelo baseline
Se elige `LogisticRegression` con multi_class='multinomial', solver='lbfgs', class_weight='balanced', max_iter=1000. Alternativa considerada: LinearSVC, RidgeClassifier. Se elige regresión logística porque produce probabilidades calibradas, tiene interpretabilidad directa (coeficientes) y es el estándar para baselines multiclase.

### Semilla fija para reproducibilidad
Se usa `random_state=42` en vectorizador, modelo y splits internos. El valor se registra en el reporte. Cualquier ejecución con la misma semilla y datos debe producir métricas idénticas.

### Script único para entrenamiento+reporte
Se crea `scripts/ml/train_baseline.py` que carga datos, vectoriza, entrena, evalúa y genera reporte JSON. Separar entrenamiento y evaluación en scripts distintos añadiría complejidad sin necesidad para un baseline.

### Reporte JSON con métricas y config
El reporte (`reports/validation/cfpb_baseline_metrics.json`) contiene: config del pipeline, macro F1 train/val, gap, accuracy, precision/recall/F1 por clase, clases débiles, semilla y versiones. Sin narrativas ni identificadores.

## Risks / Trade-offs

| Riesgo | Impacto | Mitigación |
|---|---|---|
| TF-IDF con max_features bajo pierde señal de clases minoritarias | Clases débiles no representadas | El reporte identifica clases con F1 < 0.5; decisión de ajuste delegada a MED-03 |
| Regresión logística no captura relaciones no lineales | Baseline conservador | Es esperado; el gap bajo demostrará que no hay overfitting, no que el modelo sea óptimo |
| Gap de overfitting artificial por train pequeño | Falsa alarma de underfitting | Train tiene 1.37M filas; el gap real reflejará capacidad del modelo |
| Dependencia de scikit-learn no versionada | Reproducibilidad | Se fija versión en `pyproject.toml` y se registra en el reporte |

## Migration Plan

1. Añadir scikit-learn a `pyproject.toml`.
2. Crear `scripts/ml/train_baseline.py` con pipeline TF-IDF + LogisticRegression.
3. Ejecutar sobre particiones locales, generar reporte.
4. Crear `tests/unit/test_cfpb_baseline.py` con datos sintéticos.
5. Ejecutar tests, validar con OpenSpec, archivar y PR.

No hay migración porque no existe código anterior. Rollback: revertir el commit y eliminar `models/` local.

## Open Questions

- Ninguna. Las decisiones de preparación están cerradas en PG-2.
