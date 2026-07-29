# Piloto PG-11 de selección gobernada: XGBoost

Fecha de ejecución: `2026-07-29`  
Cambio OpenSpec: `govern-cfpb-model-selection`  
Jira: `PG-11`

## Alcance ejecutado

- Entrada: muestra determinista de 20.000 filas de `train.parquet`.
- Protección: no se cargaron validación reservada ni test protegido.
- Control de fuga: `StratifiedGroupKFold` con `narrative_hash`.
- Presupuesto: 3 folds, 5 trials, semilla `42`.
- Duración observada: aproximadamente 4 h 11 min.

## Resultado agregado

| Medida | Valor |
| --- | ---: |
| Mejor macro F1 de CV | 0.591854 |
| Desviación estándar entre folds | 0.009260 |
| Fold 1 | 0.602294 |
| Fold 2 | 0.579787 |
| Fold 3 | 0.593481 |

La mejor configuración del piloto usó 100 estimadores, profundidad máxima 10,
learning rate 0.266904 y los demás parámetros registrados por Optuna en la
salida agregada de Colab.

## Límites obligatorios

Este resultado es un piloto de viabilidad. No calcula gap train-validación, no
consulta el test protegido, no selecciona un Champion y no verifica `MED-02` ni
`MED-03`. No contiene narrativas CFPB, datos brutos, binarios ni credenciales.

## Decisión humana

El 29 de julio de 2026 se revisó el piloto y se decidió conservar XGBoost solo
como candidato explorado. No se aprueba un Champion ni se modifica el estado de
`MED-02` o `MED-03`: faltan una ejecución completa gobernada, el gap
train-validación y la evidencia mínima correspondiente. La ejecución completa
queda pendiente de una aprobación explícita de presupuesto y tiempo.
