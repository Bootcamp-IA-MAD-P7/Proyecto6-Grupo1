# Quality gates locales de ClaimVox

Fecha de verificación: `2026-07-29`

Cambio OpenSpec: `add-claimvox-quality-gates`

Jira: `PG-12`

## Alcance de la evidencia

Esta evidencia registra puertas locales reproducibles sobre contratos y
artefactos sintéticos. No lee particiones CFPB, no entrena modelos, no genera
artefactos persistentes, no recalcula métricas y no acredita un servicio
desplegado, MLOps ni una decisión de Champion.

## Puertas implementadas

| Puerta | Contrato comprobado | Evidencia directa |
| --- | --- | --- |
| Integridad de datos (`ADV-04`) | Columnas mínimas, once clases, nulos críticos, objetivo conflictivo por `narrative_hash` y fuga entre particiones | `tests/unit/test_cfpb_data_quality_gate.py`: 6 pruebas sintéticas aprobadas |
| Contrato de modelo (`ADV-05`) | Ruta bajo `models`, feature permitida, once clases, forma de probabilidades e inferencia sintética | `tests/unit/test_cfpb_model_quality_gate.py`: 5 pruebas sintéticas aprobadas |
| Métricas mínimas (`ADV-06`) | Campos train/validation/por clase, once clases, gap macro F1 estrictamente menor que `0.05` y selección sin test protegido | `tests/unit/test_cfpb_metrics_quality_gate.py`: 5 pruebas sintéticas aprobadas |

La configuración versionada `config/cfpb_quality_gates.json` referencia los
contratos canónicos de target, preparación y métricas del baseline. Las puertas
devuelven solo estados y cifras agregadas; no imprimen entradas ni narrativas.

## Verificación ejecutada

```text
python -m unittest tests.unit.test_cfpb_data_quality_gate tests.unit.test_cfpb_model_quality_gate tests.unit.test_cfpb_metrics_quality_gate -v
Ran 16 tests in 0.047s
OK

npm exec -- openspec validate add-claimvox-quality-gates --type change --strict
Change 'add-claimvox-quality-gates' is valid

git diff --check
Passed
```

## Límites

- Los fixtures y artefactos de prueba son sintéticos y temporales.
- La evidencia protege los contratos locales; no sustituye ejecución de
  entrenamiento, validación cruzada completa, persistencia, observabilidad o
  despliegue.
- La puerta de métricas impide usar el test protegido para seleccionar o
  promover un modelo, pero no selecciona ningún Champion.
