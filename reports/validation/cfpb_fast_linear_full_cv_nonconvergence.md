# Ejecución no convergente de CV lineal completa — PG-11

Fecha: `2026-07-29`  
Jira: `PG-11`  
Cambio OpenSpec: `govern-fast-linear-model-selection`

## Alcance ejecutado

Se inició la fase B aprobada sobre `train.parquet` completo, con control de
grupos por `narrative_hash`, cinco folds y los parámetros lineales congelados
en la política vigente. No se cargaron `validation` ni `test` para selección.

## Resultado agregado

El candidato congelado `LogisticRegression` no convergió durante la CV
completa. El ejecutor rechazó la ejecución y no escribió el manifiesto de
evidencia delivery ni una salida de métricas que pudiera utilizarse para una
decisión.

## Decisión y límites

- No existe selección aprobada ni Champion.
- `MED-02` y `MED-03` permanecen en curso: falta una CV completa convergida y
  conforme, con variabilidad, gap estricto y métricas de las once clases.
- El baseline local de ClaimVox no cambia por esta ejecución fallida.
- Cualquier alternativa requerirá una nueva decisión versionada y aprobación
  humana antes de reintentarla.
