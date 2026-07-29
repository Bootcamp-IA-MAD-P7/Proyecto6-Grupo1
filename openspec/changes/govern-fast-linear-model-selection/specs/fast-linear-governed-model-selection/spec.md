## ADDED Requirements

### Requirement: Búsqueda lineal agrupada y acotada

El sistema SHALL optimizar exclusivamente el baseline lineal sobre una muestra
determinista y agrupada de `train.parquet`, mediante `StratifiedGroupKFold`,
semilla versionada y macro F1 como métrica primaria. La búsqueda SHALL registrar
su presupuesto y SHALL NOT cargar `validation` ni `test`.

#### Scenario: Búsqueda lineal conforme

- **WHEN** se inicia la fase de búsqueda
- **THEN** el ejecutor consume únicamente grupos de `train` y registra muestra,
  folds, semilla, trials y parámetros
- **AND** rechaza rutas de validation, test o corpus completo

### Requirement: CV completa con parámetros congelados

El sistema SHALL evaluar los parámetros lineales elegidos sobre todo
`train.parquet` mediante cinco folds `StratifiedGroupKFold` por `narrative_hash`.
La fase SHALL NOT retunar parámetros y SHALL registrar macro F1 de train y fold,
variabilidad, coste y métricas agregadas de las once clases.

#### Scenario: Evaluación completa conforme

- **WHEN** la fase de CV completa se ejecuta con parámetros de búsqueda
- **THEN** los cinco folds conservan grupos y generan evidencia agregada por
  clase, media, desviación y coste
- **AND** no se consulta validation ni test

### Requirement: Evidencia y decisión no promocional

El sistema SHALL exigir gap macro F1 train-fold estrictamente inferior a `0.05`
y evidencia completa antes de permitir actualizar `MED-02` o `MED-03`. El
sistema SHALL NOT declarar un Champion; una confirmación única sobre validation
MAY ocurrir solo tras revisión humana y sin retuning.

#### Scenario: Evidencia insuficiente o no promocional

- **WHEN** falta CV completa, una clase, el gap es igual o superior a `0.05` o
  no existe revisión humana
- **THEN** el informe registra evidencia insuficiente o sin selección aprobada
- **AND** no utiliza test ni presenta el baseline como Champion
