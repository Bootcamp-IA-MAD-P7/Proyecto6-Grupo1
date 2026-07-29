# Revisión de partición para selección de modelo

Fecha: `2026-07-29`  
Cambio OpenSpec: `govern-cfpb-model-selection`  
Tarea: `1.1`

## Confirmación

La preparación vigente usa la estrategia `temporal_group_isolated` definida en
`config/cfpb_training_policy.json`: 70 % entrenamiento, 15 % validación y 15 %
test, con `test_protected: true`.

Los grupos de `narrative_hash` se conservan juntos. El preparador
`scripts/data/cfpb_training_preparation.py` rechaza grupos repartidos entre
particiones y comprueba el orden temporal y el soporte mínimo por clase.

`scripts/ml/train_baseline.py` carga las tres particiones aprobadas por separado
y solo calcula métricas del test con la opción explícita `--evaluate-test`.

## Implicación para PG-11

La futura validación cruzada debe usar únicamente `train.parquet`; no puede
mezclar validación ni test. Antes de ejecutarla se debe elegir una estrategia
estratificada compatible con los grupos y la prevención temporal de leakage.
No se han abierto datos, entrenado modelos ni generado métricas en esta revisión.
