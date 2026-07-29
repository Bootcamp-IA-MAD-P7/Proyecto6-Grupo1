# Aprobación de ejecución — PG-11 fase A lineal

Fecha: `2026-07-29`  
Jira: `PG-11`  
Cambio OpenSpec: `govern-fast-linear-model-selection`

## Decisión humana

Miguel aprueba la ejecución de la fase A en Colab con LogisticRegression.

## Límite aprobado

- Entrada: muestra determinista y agrupada de hasta 50.000 filas de `train.parquet`.
- Control de fuga: `narrative_hash`, `StratifiedGroupKFold`, tres folds y semilla `42`.
- Búsqueda: hasta 30 trials y macro F1 como métrica primaria.
- Salida: únicamente evidencia agregada conforme al contrato versionado.

## Límites mantenidos

- No cargar `validation` ni `test` para selección o retuning.
- No persistir narrativas, datos brutos, binarios, credenciales ni logs sensibles.
- No declarar Champion ni sustituir el modelo local de ClaimVox.
- La fase B completa requiere parámetros congelados y evidencia propia.
