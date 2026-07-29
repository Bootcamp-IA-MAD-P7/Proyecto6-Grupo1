## Context

El baseline vigente usa TF-IDF y LogisticRegression sobre once clases y ya es el
modelo de inferencia local de ClaimVox. XGBoost, RF y LightGBM fueron comparados
para `MED-01`, pero su coste hace inviable una búsqueda completa en el entorno
de ejecución disponible. Esta decisión no promociona el baseline a Champion.

## Goals / Non-Goals

**Goals:**

- Obtener búsqueda reproducible de regularización lineal y evidencia de CV
  agrupada completa, respetando `narrative_hash` y el aislamiento de datos.
- Separar búsqueda económica y evaluación completa: la primera fija parámetros;
  la segunda no reabre la optimización.
- Producir solo manifiesto y métricas agregadas de las once clases.

**Non-Goals:**

- No comparar de nuevo ensembles, crear un Champion, cambiar ClaimVox ni
  persistir un artefacto nuevo de servicio.
- No usar `validation` o `test` para seleccionar, retunar o diagnosticar.
- No incluir narrativas, datos brutos, binarios, credenciales o logs sensibles.

## Decisions

### Dos fases aisladas

La fase A SHALL tomar una muestra determinista de hasta 20.000 filas de grupos
de `train.parquet`, estratificada por la clase contratada, con tres folds
`StratifiedGroupKFold`, semilla `42` y hasta 10 trials de LogisticRegression.
La muestra es exclusivamente de búsqueda y no acredita `MED-02` por sí sola.

La fase B SHALL usar todos los grupos de `train.parquet`, cinco folds
`StratifiedGroupKFold`, semilla `42` y los parámetros congelados de la fase A.
No realizará Optuna ni modificará parámetros dentro de los folds. Registrará
macro F1 de train y fold, media, desviación, gap, coste y métricas agregadas por
clase. Esta separación reduce el coste sin convertir un piloto en cierre.

Se descartan Random Forest y XGBoost para esta entrega porque el coste crece
mucho con texto TF-IDF y no mejora la evidencia requerida para validar el
protocolo lineal actual.

### Frontera de decisión

La selección técnica se limita a `train`. Tras revisión humana, se podrá hacer
una única confirmación contra `validation` sin retuning. El test no se carga.
Un resultado que exceda gap `0.05`, no cubra las once clases o no complete la
CV será evidencia insuficiente, no un Champion.

## Risks / Trade-offs

- [La búsqueda usa una muestra] → documentar su propósito y ejecutar CV completa
  con parámetros congelados antes de actualizar criterios.
- [CV completa aún consume tiempo] → usar el modelo lineal existente, registrar
  coste y no iniciar sin aprobación humana del entorno.
- [Clases minoritarias inestables] → usar grupos, resultados por clase y revisión
  humana; no decidir solo por macro F1.

## Migration Plan

1. Versionar el perfil lineal de dos fases y pruebas sintéticas.
2. Aprobar presupuesto y ejecutar fase A fuera de Git.
3. Congelar sus parámetros, ejecutar fase B y validar evidencia agregada.
4. Si falla una puerta, conservar el baseline local y registrar ausencia de
   selección aprobada; no hay cambio de servicio que revertir.

## Open Questions

- La confirmación sobre `validation` y cualquier selección posterior requieren
  revisión humana después de que ambas fases terminen correctamente.
