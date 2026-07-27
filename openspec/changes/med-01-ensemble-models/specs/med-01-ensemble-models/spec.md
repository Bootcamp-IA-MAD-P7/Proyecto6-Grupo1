## Purpose

Comparar modelos ensemble (Random Forest, XGBoost) contra el baseline LogisticRegression sobre las once clases canónicas del contrato CFPB, usando el mismo split temporal, las mismas métricas y código reutilizable en `src/ml/`.

## ADDED Requirements

### Requirement: Modelos ensemble comparables
Los pipelines SHALL entrenar Random Forest y XGBoost con el mismo split temporal que el baseline (70/15/15) sobre las once clases de `config/cfpb_target_contract.json`, y SHALL reportar macro F1, weighted F1, accuracy, precision y recall sobre validation.

#### Scenario: Misma partición que baseline
- **WHEN** se entrena un modelo ensemble
- **THEN** usa la misma partición train/validation/test que el baseline (split temporal con fecha protegida)

#### Scenario: Métricas completas sobre validation
- **WHEN** el pipeline completa el entrenamiento y evalúa sobre validation
- **THEN** el reporte incluye macro F1, weighted F1, accuracy, precision macro, recall macro para cada modelo

### Requirement: Código reutilizable en src/ml/
Los componentes de vectorización, evaluación, modelos, tuning y visualización SHALL residir en `src/ml/` como módulos independientes, configurables desde diccionarios, para poder ser reutilizados por cualquier script de entrenamiento.

#### Scenario: Módulos independientes
- **WHEN** se importa cualquier módulo de `src/ml/`
- **THEN** funciona sin depender de otros módulos del proyecto (solo de sklearn, xgboost, matplotlib, numpy estándar)

#### Scenario: Configuración por diccionario
- **WHEN** se instancia un vectorizador, modelo o evaluador
- **THEN** acepta un diccionario `config` con todos sus parámetros

### Requirement: Optimización con Optuna
El pipeline SHALL usar Optuna para buscar hiperparámetros de Random Forest y XGBoost sobre validation, sin utilizar el test protegido.

#### Scenario: Búsqueda sobre validation
- **WHEN** Optuna completa una ejecución
- **THEN** todos los trials se evalúan sobre validation; el test nunca se usa para selección

#### Scenario: Mejor trial registrado
- **WHEN** la optimización termina
- **THEN** el mejor trial y sus hiperparámetros quedan registrados en el reporte

### Requirement: Matriz de confusión
El pipeline SHALL generar una matriz de confusión en validation para cada modelo (LR, RF, XGBoost) como figura reproducible (PNG).

#### Scenario: Figura guardada sin narrativas
- **WHEN** se genera la matriz de confusión
- **THEN** se guarda en `reports/validation/figures/` y no contiene textos CFPB reales

### Requirement: Feature importance
El pipeline SHALL reportar feature importance para cada modelo: coeficientes para LogisticRegression, permutation importance para RF y XGBoost.

#### Scenario: Importancia por modelo compatible
- **WHEN** se calcula feature importance
- **THEN** cada modelo usa el método compatible con su tipo (coeficientes lineales / impurity / permutation)

### Requirement: Informe comparativo
El pipeline SHALL generar un informe `reports/validation/med_01_comparison.md` con tabla comparativa de los 3 modelos (LR, RF, XGBoost), clases débiles, y lectura cualitativa.

#### Scenario: Tabla de tres modelos
- **WHEN** se genera el informe
- **THEN** contiene una tabla con macro F1, weighted F1 y accuracy de los 3 modelos sobre validation

#### Scenario: Sin narrativas
- **WHEN** se genera el informe
- **THEN** no contiene narrativas CFPB, solo cifras agregadas y configuraciones

## Extensiones verificadas durante la implementación

### LightGBM añadido como tercer modelo ensemble
Durante la implementación se añadió LightGBM (GPU) como extensión sobre el alcance original de RF + XGBoost. Resultados con sample 50K:

| Modelo | Macro F1 | Weighted F1 | Accuracy | ROC AUC | Gap |
|---|---|---|---|---|---|
| LogisticRegression (baseline) | 0.5973 | 0.8678 | 0.8484 | — | 0.0482 ✅ |
| Random Forest | 0.4704 | 0.8270 | 0.8082 | 0.9309 | 0.1073 ❌ |
| XGBoost | **0.6332** | **0.8963** | **0.9026** | **0.9663** | 0.2868 ❌ |
| LightGBM | 0.6175 | 0.8956 | 0.9017 | 0.9650 | 0.3067 ❌ |

**XGBoost obtiene el mejor macro F1 de validación de la comparación** (0.6332), superando al baseline LR (0.5973) sobre la muestra de 50K. No queda seleccionado como modelo definitivo: su gap supera el 5 % y requiere evaluación posterior bajo MED-03.
**LightGBM** (GPU) queda como referencia con defaults y sin tuning.
Todos los ensemble presentan overfitting >5%, transferido a MED-03 para optimización.

La optimización de hiperparámetros con Optuna se pospuso: LightGBM tuning con 500K filas abandonado tras 12/25 trials en 3+ horas (mejor trial 0.6538, marginal vs defaults 0.6404).
