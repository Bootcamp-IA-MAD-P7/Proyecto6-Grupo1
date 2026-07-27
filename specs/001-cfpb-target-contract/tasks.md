# Tareas: Contrato de target CFPB

- Spec: [`spec.md`](spec.md)
- Plan: [`plan.md`](plan.md)

## T-001 Versionar la taxonomía y sus excepciones

- Estado: `[x]`
- Responsable: `Datos / ML`
- Requisitos cubiertos: `R-001, R-002, R-008, AC-001, AC-004`
- Trabajo: declarar once clases, dos aliases y una exclusión ambigua.
- Verificación: tests de cardinalidad, destinos y cobertura de etiquetas observadas.
- Evidencia obtenida: `config/cfpb_target_contract.json` y `tests/unit/test_cfpb_target_contract.py`.

## T-002 Fijar límites de features, privacidad y duplicados

- Estado: `[x]`
- Responsable: `Datos / seguridad`
- Dependencias: `T-001`
- Requisitos cubiertos: `R-003, R-004, R-005, AC-002, AC-003, AC-005`
- Trabajo: declarar entrada única, campos prohibidos, persistencia y agrupación anti-leakage.
- Verificación: revisión del contrato y tests de separación feature/target.
- Evidencia obtenida: spec, plan y contrato versionado.

## T-003 Entregar el contrato al EDA paralelo

- Estado: `[x]`
- Responsable: `Equipo EDA`
- Dependencias: `T-001, T-002`
- Requisitos cubiertos: `R-006, R-007, AC-006`
- Trabajo: usar esta spec como referencia y devolver únicamente evidencias agregadas.
- Verificación: checklist de población, clases, tiempo, ausencias, duplicados, conflictos, longitud e idioma.
- Evidencia obtenida: contrato de entrega definido; ejecución del EDA fuera de esta rama.

## T-004 Incorporar evidencia del EDA

- Estado: `[x]`
- Responsable: `Víctor / Datos y EDA`
- Dependencias: `T-003`
- Requisitos cubiertos: `R-006, R-007, R-009`
- Trabajo: contrastar soporte, drift, idioma, duplicados y alternativas de desbalanceo.
- Verificación: informe reproducible, revisión cruzada y ausencia de narrativas versionadas.
- Evidencia obtenida:
  - `scripts/data/convert_cfpb_to_parquet.py` — conversor CSV → Parquet con filtrado, mapping y hashing.
  - `notebooks/01_eda.py` — notebook EDA reproducible con análisis de clase, temporal, duplicados, longitud e idioma.
  - `reports/figures/class_distribution.png`, `temporal_trend.png`, `duplicates_analysis.png`, `length_distribution.png` — figuras agregadas.
  - `reports/validation/cfpb_eda.md` — informe EDA con respuestas a Q-001 a Q-004.
  - `data/interim/cfpb.parquet` — Parquet de 2.27M filas (gitignored).
  - La política y preparación de `T-006` cierran las decisiones de idioma, duplicados, split y desbalanceo para la instantánea de entrenamiento actual, sin mezclar sus cifras con el snapshot EDA anterior.

## T-005 Implementar el constructor reproducible

- Estado: `[x]`
- Responsable: `Datos / ML`
- Dependencias: `T-004`
- Requisitos cubiertos: `R-001 a R-008`
- Trabajo: aplicar filtros, mapping, exclusiones, huellas y salida agregada usando el contrato.
- Verificación: tests unitarios y de integración sobre una muestra local.
- Evidencia obtenida:
  - Cambio OpenSpec `build-cfpb-training-dataset` con propuesta, requisitos, diseño y tareas trazados a `PG-2`.
  - `scripts/data/convert_cfpb_to_parquet.py` con rutas explícitas, filtro contractual, aliases, exclusión ambigua, huella de narrativa, exclusión de conflictos y manifiesto agregado.
  - `tests/unit/test_cfpb_training_dataset.py` con seis pruebas exclusivamente sintéticas; también pasan los ocho tests del contrato.
  - `reports/validation/cfpb_training_dataset.md` y `reports/validation/cfpb_training_dataset_manifest.json` con recuentos agregados de la fuente actual, sin narrativas ni identificadores.
  - Corpus local `data/processed/cfpb_training.parquet` y etapa `data/interim/cfpb_training_candidates.parquet`, ambos ignorados por Git.
  - Límite: T-005 no decide idioma, tratamiento intra-grupo, partición, desbalanceo ni autoriza entrenamiento; esas puertas siguen en T-006.

## T-006 Cerrar idioma, privacidad y partición

- Estado: `[x]`
- Responsable: `Equipo`
- Dependencias: `T-004, T-005`
- Requisitos cubiertos: `R-004, R-005, R-009`
- Trabajo: resolver Q-001 a Q-004 y aplicar la política aprobada antes de entrenar.
- Verificación: revisión del equipo, tests sintéticos, evidencia local agregada y documentación sincronizada.
- Evidencia obtenida:
  - Cambio OpenSpec `decide-cfpb-training-policy`, vinculado a `PG-2`, con los requisitos y el diseño aprobados.
  - `config/cfpb_training_policy.json` fija la referencia de fuente y contrato, baseline inicial inglés, grupos completos, split temporal 70/15/15, macro F1 y pesos balanceados.
  - `scripts/data/cfpb_training_policy.py` y `tests/unit/test_cfpb_training_policy.py` verifican de forma sintética que una fuente o contrato diferente detiene la preparación sin exponer contenido.
  - `reports/validation/cfpb_training_preparation.md` y `reports/validation/cfpb_training_preparation_manifest.json` confirman 1.961.073 filas en inglés, split temporal por grupo sin leakage y soporte mínimo de 100 filas por clase en validation y test.
  - Límite: este cierre habilita el baseline de `PG-3`; no entrena ni evalúa un modelo y no verifica los criterios de entrega de modelado.

## T-007 Adoptar el flujo reproducible de notebooks

- Estado: `[x]`
- Responsable: `Víctor / Datos y EDA`
- Dependencias: ninguna (relacionada con T-004, no bloqueante)
- Requisitos cubiertos: `ADR-003`
- Trabajo: implementar ADR-003: crear `.jupytext.toml`, actualizar `.gitignore` con `*.ipynb`, crear `Makefile` opcional, actualizar `notebooks/README.md`.
- Límites: no modificar el EDA (T-004), no entrenar modelos, no crear spec de modelado, no marcar T-004 como completada.
- Verificación: `git diff --check`, `python scripts/quality/check_repository.py`, sincronización de prueba entre `.py` y `.ipynb`, ausencia de narrativas versionadas.
- Evidencia obtenida: `.jupytext.toml`, `.gitignore` actualizado, `Makefile`, `notebooks/README.md` actualizado, `pyproject.toml` con uv y dependencias, sincronización jupytext verificada.

## Checklist de cierre

- [x] Todos los criterios de aceptación están cubiertos.
- [x] Las pruebas acordadas pasan.
- [x] El informe EDA cumple el contrato de entrega.
- [x] Idioma, privacidad, duplicados y partición están decididos para el baseline inicial.
- [x] La documentación coincide con el comportamiento real.
- [x] No se han incorporado narrativas al repositorio.

## Continuidad posterior

La política cerrada en `T-006` habilitó el cambio OpenSpec archivado
`train-cfpb-baseline` / Jira `PG-3`, integrado mediante la PR #31. Ese cambio
entrenó y evaluó un baseline reproducible; sus métricas y límites están en
`reports/validation/cfpb_baseline.md`. No cambia retrospectivamente el alcance
de `T-004` a `T-006` ni acredita inferencia integrada.
