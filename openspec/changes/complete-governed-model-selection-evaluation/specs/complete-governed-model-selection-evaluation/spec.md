## ADDED Requirements

### Requirement: Ejecución completa de validación cruzada agrupada

El sistema SHALL evaluar candidatos únicamente sobre la partición local
`train.parquet` aprobada mediante `StratifiedGroupKFold` de cinco folds, semilla
versionada y agrupación obligatoria por `narrative_hash`. El sistema SHALL NOT
cargar `validation`, `test` ni el corpus completo durante la selección.

#### Scenario: Ejecución conforme de CV

- **WHEN** se inicia la evaluación de entrega de un candidato
- **THEN** el ejecutor consume solo `train.parquet`, registra cinco folds,
  estrategia, semilla y métricas agregadas por fold
- **AND** rechaza entradas de validation, test o corpus completo

### Requirement: Optimización reproducible dentro de folds

El sistema SHALL ejecutar la búsqueda de hiperparámetros con macro F1 como
métrica primaria, hasta el presupuesto aprobado por candidato y únicamente
dentro de los folds de entrenamiento. El sistema SHALL registrar configuración,
semillas, resultados de train y validación de cada fold, media, variabilidad y
coste, sin consultar el test protegido.

#### Scenario: Búsqueda de entrega reproducible

- **WHEN** una búsqueda gobernada completa finaliza
- **THEN** la evidencia agregada permite reproducir el presupuesto, la
  configuración y la variabilidad entre folds
- **AND** no contiene narrativas, datos brutos, binarios, credenciales ni logs
  sensibles

### Requirement: Confirmación y decisión gobernadas

El sistema SHALL aplicar el límite estricto de gap macro F1 menor que `0.05` y
los desempates aprobados antes de recomendar un candidato. Tras revisión humana,
el sistema MAY confirmar una única recomendación contra `validation` sin volver
a ajustar parámetros. El sistema SHALL NOT usar `test` ni declarar un Champion
o un despliegue.

#### Scenario: Resultado elegible o sin selección

- **WHEN** la evidencia completa se revisa contra la política
- **THEN** el informe registra una recomendación condicionada o «sin selección
  aprobada», junto con sus limitaciones y decisión humana
- **AND** `MED-02` y `MED-03` cambian de estado solo si la evidencia mínima de
  cada criterio queda satisfecha
