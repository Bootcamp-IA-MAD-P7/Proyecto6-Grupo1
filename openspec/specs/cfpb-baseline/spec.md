## Purpose

Entrenar y evaluar un baseline reproducible de clasificación multiclase (TF-IDF +
LogisticRegression) sobre las once familias canónicas del contrato CFPB, usando
solo `complaint_what_happened` como entrada. Controlar overfitting, documentar
clases débiles y preservar el test para evaluación final.

## Requirements

### Requirement: Modelo funcional para once clases
El pipeline SHALL producir un modelo de clasificación multiclase que prediga exactamente las once clases canónicas definidas en `config/cfpb_target_contract.json`. La entrada SHALL ser exclusivamente el texto de `complaint_what_happened` vectorizado.

#### Scenario: Predicción sobre las once clases contratadas
- **WHEN** el pipeline recibe una muestra sintética de validación con narrativas de todas las once clases
- **THEN** la salida contiene una predicción por fila y todas las predicciones pertenecen al conjunto de etiquetas canónicas del contrato

#### Scenario: Rechazo de campos prohibidos
- **WHEN** el pipeline recibe datos que incluyen columnas prohibidas por el contrato (`product`, `sub_product`, `company`, `issue`, `sub_issue`)
- **THEN** el pipeline falla explícitamente o ignora esas columnas sin incorporarlas como features

### Requirement: Métricas por clase y agregadas
El pipeline SHALL calcular accuracy global, precision, recall y F1 por clase (macro y weighted) sobre el conjunto de validation.

#### Scenario: Cálculo de métricas sobre validation
- **WHEN** el pipeline completa el entrenamiento y evalúa sobre validation
- **THEN** el reporte incluye accuracy, precision, recall y F1 por clase, además de macro F1 y weighted F1

#### Scenario: Reporte sin narrativas
- **WHEN** se genera el reporte de métricas
- **THEN** el reporte versionado no contiene narrativas CFPB, solo cifras agregadas y configuraciones

### Requirement: Control de overfitting
La diferencia (gap) entre macro F1 de entrenamiento y macro F1 de validation SHALL ser inferior a 0.05.

#### Scenario: Gap dentro del umbral
- **WHEN** se calculan macro F1 en train y validation
- **THEN** `abs(macro_f1_train - macro_f1_val) < 0.05`

#### Scenario: Gap excede el umbral
- **WHEN** el gap es igual o superior a 0.05
- **THEN** el pipeline advierte explícitamente y registra el valor en el reporte

### Requirement: Reproducibilidad
El pipeline SHALL aceptar una semilla entera y registrar todas las configuraciones (vectorizador, modelo, hiperparámetros) para permitir reproducción exacta.

#### Scenario: Misma semilla produce mismo resultado
- **WHEN** se ejecuta el pipeline dos veces con la misma semilla y los mismos datos sintéticos
- **THEN** las métricas de ambas ejecuciones son idénticas

#### Scenario: Configuración registrada
- **WHEN** el pipeline finaliza
- **THEN** el reporte incluye la semilla, hiperparámetros, versión de scikit-learn y huella del contrato

### Requirement: Artefacto y tests
El pipeline SHALL persistir el modelo entrenado localmente (gitignored) y SHALL incluir tests de carga, forma de salida y cobertura de clases.

#### Scenario: Artefacto local gitignored
- **WHEN** el pipeline completa el entrenamiento
- **THEN** el modelo se guarda en `models/` (gitignored) y `git check-ignore` confirma que está excluido

#### Scenario: Tests de forma de salida
- **WHEN** se ejecutan los tests del pipeline
- **THEN** verifican que la salida tiene forma (n_muestras, 11) para probabilidades y que las predicciones son strings válidas del contrato

### Requirement: Clases débiles documentadas
El reporte SHALL identificar las clases con F1 por debajo de un umbral configurable (por defecto 0.5) y documentar sus limitaciones.

#### Scenario: Identificación de clases débiles
- **WHEN** el reporte se genera
- **THEN** lista las clases cuyo F1 < 0.5 junto con su soporte (número de muestras en validation)
