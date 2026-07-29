# Resolución humana de búsqueda lineal — PG-11

Fecha: `2026-07-29`  
Jira: `PG-11`  
Cambio OpenSpec: `govern-fast-linear-model-selection`

## Evidencia revisada

`cfpb_fast_linear_search.json` registra la búsqueda aprobada sobre 20.000 filas
agrupadas de `train.parquet`, tres folds y diez trials de LogisticRegression.
La mejor puntuación observada fue macro F1 `0.565097` con desviación `0.032584`,
pero su candidato alcanzó el límite de iteraciones en los folds y no se aprueba
para la CV completa.

## Decisión humana

Miguel aprueba congelar el candidato convergido observado en la búsqueda:

- `C`: `0.004207988669606638`
- `class_weight`: `balanced`
- `solver`: `saga`
- `max_iter`: `500`
- `random_state`: `42`

La decisión no declara un Champion ni modifica el modelo servido por ClaimVox.

## Siguiente frontera

La fase B debe ejecutar cinco folds sobre todo `train.parquet`, sin retuning,
registrar convergencia, métricas agregadas de las once clases, variabilidad y
gap estricto inferior a `0.05`. Cualquier aviso de convergencia o puerta no
satisfecha impide verificar `MED-02` o `MED-03`.
