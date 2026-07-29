## ADDED Requirements

### Requirement: Puerta de integridad del dataset

El sistema MUST proporcionar una puerta local que valide el contrato del dataset
elegible sin leer ni emitir narrativas CFPB. La puerta MUST comprobar columnas
autorizadas, once clases canónicas, nulos críticos, grupos duplicados
conflictivos y ausencia de fuga de `narrative_hash` entre particiones.

#### Scenario: Dataset sintético conforme

- **WHEN** la puerta recibe fixtures sintéticos que cumplen los contratos de
  clases, esquema y partición
- **THEN** finaliza correctamente y comunica únicamente resultados agregados

#### Scenario: Fuga de grupo entre particiones

- **WHEN** la puerta detecta un mismo `narrative_hash` en dos particiones
- **THEN** falla explícitamente sin imprimir filas ni textos de entrada

### Requirement: Puerta del contrato de modelo

El sistema MUST proporcionar una puerta local que compruebe que un artefacto de
modelo autorizado puede cargarse de forma controlada, acepta exclusivamente el
contrato de features permitido y devuelve probabilidades y clases compatibles
con las once etiquetas canónicas.

#### Scenario: Inferencia sintética compatible

- **WHEN** la puerta carga un artefacto sintético compatible y procesa una
  entrada sintética válida
- **THEN** valida la forma de salida, las probabilidades y las etiquetas sin
  exponer el contenido de la entrada

#### Scenario: Artefacto o clase no conforme

- **WHEN** el artefacto no puede cargarse de una ubicación controlada o produce
  una clase fuera del contrato
- **THEN** la puerta falla explícitamente y no permite tratarlo como elegible

### Requirement: Puerta de métricas mínimas

El sistema MUST validar un reporte agregado versionado contra umbrales aprobados
para accuracy, métricas por clase, macro F1 y gap train-validation. La puerta
MUST rechazar evidencia incompleta, un gap igual o superior a 0.05 o clases sin
las métricas exigidas, y MUST NOT usar el test protegido para seleccionar o
promover un modelo.

#### Scenario: Reporte agregado conforme

- **WHEN** la puerta recibe un reporte agregado completo con los umbrales
  aprobados y gap inferior a 0.05
- **THEN** registra que la evidencia satisface el contrato local de métricas
  sin declarar un Champion

#### Scenario: Gap o evidencia insuficiente

- **WHEN** falta una métrica obligatoria o el gap train-validation es igual o
  superior a 0.05
- **THEN** la puerta falla con el criterio incumplido y sin recalcular el modelo

### Requirement: Evidencia privada y verificable

Las puertas MUST ejecutarse con fixtures sintéticos o manifiestos y reportes
agregados versionables. Sus pruebas, logs y evidencias MUST NOT contener
narrativas CFPB, datos brutos, credenciales, binarios ni artefactos locales.

#### Scenario: Ejecución de quality gates

- **WHEN** se ejecutan las pruebas o el comprobador de quality gates
- **THEN** la salida versionable contiene solo nombres de contratos, estados y
  cifras agregadas necesarias para revisar el resultado
