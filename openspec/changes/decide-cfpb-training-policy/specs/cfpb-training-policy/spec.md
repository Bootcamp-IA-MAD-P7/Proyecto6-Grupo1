## ADDED Requirements

### Requirement: Instantánea de referencia trazable

El sistema MUST usar para el baseline inicial la fuente local CFPB identificada por la huella `f1cb8b412f6af5039ae630b3d0a1e4b5eab93be900a247ae60ea33cea073b351` y el contrato `config/cfpb_target_contract.json` con huella `58b7ada8e6decdf0378aae4c042a381884ddda39143cbf0d6a0062c1f10fb9bd`. Toda ejecución posterior MUST registrar ambas huellas y MUST fallar si la fuente o el contrato no coinciden con la política aprobada.

#### Scenario: Fuente local coincidente
- **WHEN** se prepara el corpus para el baseline con la fuente y contrato aprobados
- **THEN** la evidencia registra sus huellas y permite reproducir los mismos recuentos de control
- **AND** no publica narrativas ni identificadores de reclamación

#### Scenario: Fuente o contrato distintos
- **WHEN** una ejecución usa una fuente o contrato con huella diferente
- **THEN** el proceso falla antes de generar particiones para entrenamiento
- **AND** solicita una nueva decisión versionada

### Requirement: Política inicial de idioma y privacidad

El sistema MUST incluir en el baseline inicial únicamente narrativas clasificadas como inglés por un detector determinista versionado en el cambio de preparación. Debe cuantificar de forma agregada las exclusiones y MUST mantener narrativas, textos de error y artefactos de datos exclusivamente en rutas locales ignoradas por Git.

#### Scenario: Narrativa no inglesa o no clasificable
- **WHEN** el detector determinista no clasifica una narrativa como inglés
- **THEN** la fila no entra en el corpus del baseline inicial
- **AND** el manifiesto conserva solamente el recuento agregado de exclusión

### Requirement: Grupos duplicados sin leakage

El sistema MUST excluir los grupos de huella con targets contradictorios conforme al constructor contractual. Los grupos no conflictivos MUST conservarse completos y MUST asignarse a una única partición; el baseline inicial MUST NOT colapsarlos, ponderarlos ni distribuirlos entre train, validation y test.

#### Scenario: Grupo duplicado no conflictivo
- **WHEN** varias filas comparten huella y target canónico
- **THEN** todas se asignan a la misma partición
- **AND** la evidencia agrega el número de grupos y filas por partición sin publicar narrativas

### Requirement: Partición temporal reproducible

El sistema MUST crear particiones train, validation y test en orden temporal, usando como referencia la fecha máxima de cada grupo de huella. La política MUST aspirar a proporciones 70/15/15 sobre el corpus elegible, exigir al menos 100 filas de cada clase en validation y test, y registrar los límites de fecha efectivos, recuentos, clases y semillas. El test MUST permanecer protegido frente a selección de modelo e hiperparámetros.

#### Scenario: Partición válida por grupo y tiempo
- **WHEN** se genera la partición inicial
- **THEN** ninguna huella aparece en más de una partición
- **AND** train no contiene grupos con fecha máxima posterior a validation o test
- **AND** validation no contiene grupos con fecha máxima posterior a test

### Requirement: Baseline equilibrado y evaluación honesta

El baseline inicial MUST usar `class_weight="balanced"` sin sobremuestreo ni submuestreo. La métrica primaria MUST ser macro F1; accuracy, F1 weighted, precision, recall y F1 por clase son métricas complementarias obligatorias. El control de sobreajuste MUST usar la diferencia absoluta de macro F1 entre train y validation y requerirá un valor inferior a `0.05` para cualquier candidato que se presente como aceptable.

#### Scenario: Comparación de candidatos
- **WHEN** se entrena un baseline o un candidato posterior
- **THEN** la selección usa validation y macro F1 como métrica primaria
- **AND** el test protegido no participa en la selección
- **AND** la evidencia muestra la diferencia train-validation y las métricas por clase

### Requirement: Límites antes del entrenamiento

Esta política MUST NOT entrenar modelos, modificar la interfaz, conectar backend, cambiar el target contractual ni verificar criterios de entrega. Debe preparar únicamente la configuración y pruebas necesarias para un cambio posterior de partición y baseline.

#### Scenario: Intento de ampliar el alcance
- **WHEN** una tarea introduce un modelo entrenado, una inferencia real o una métrica reportada como resultado
- **THEN** se considera fuera de alcance de este cambio
- **AND** requiere un cambio OpenSpec posterior con evidencia propia
