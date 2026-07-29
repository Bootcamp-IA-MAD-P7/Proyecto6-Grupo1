# governed-feedback-operational-flow Specification

## Purpose
TBD - created by archiving change add-feedback-operational-flow. Update Purpose after archive.
## Requirements
### Requirement: Registro local explícito de revisión

El sistema SHALL aceptar feedback solo mediante una operación local posterior a
una predicción y SHALL validar los campos, clases, decisiones, finalidades y
retención contra `config/claimvox_feedback_persistence_policy.json`. El sistema
SHALL NOT aceptar ni persistir narrativas, identidad, texto libre, audio,
transcripciones, probabilidades completas ni propiedades no autorizadas.

#### Scenario: Revisión local conforme

- **WHEN** una persona registra una decisión permitida con identificadores,
  versiones, clases canónicas y marcas UTC válidas
- **THEN** el sistema persiste exclusivamente el registro minimizado bajo la
  raíz local controlada

#### Scenario: Campo prohibido

- **WHEN** la operación de feedback contiene una propiedad prohibida o una
  clase, decisión o finalidad fuera de la política
- **THEN** el sistema la rechaza sin incluir el valor sensible en la respuesta
  de error ni crear un registro

### Requirement: Resumen local agregado de feedback

El sistema SHALL devolver solo contadores agregados por `model_version`,
`suggested_class` y `decision`, y SHALL purgar registros vencidos antes de
generar el resumen. El sistema SHALL NOT devolver UUID, registros individuales,
narrativas ni datos de identidad.

#### Scenario: Consulta de resumen local

- **WHEN** el cliente solicita el resumen de feedback local
- **THEN** recibe exclusivamente grupos agregados y contadores tras la purga
  idempotente de registros vencidos

### Requirement: Frontera de recolección para reentrenamiento

El sistema SHALL tratar la finalidad `future_retraining_candidate` como una
señal trazable pendiente de revisión. El sistema SHALL NOT añadir feedback al
corpus, entrenar, seleccionar un modelo ni promover un Champion de forma
automática.

#### Scenario: Candidato registrado

- **WHEN** una persona registra feedback con la finalidad de candidato futuro
- **THEN** el sistema conserva solo el metadato permitido y comunica que no se
  ha incorporado ningún dato a entrenamiento ni a selección de modelo

### Requirement: Evidencia extrema a extremo de feedback local

El sistema SHALL aportar una comprobación reproducible que conecte una
predicción local real con la creación explícita de feedback permitido y la
consulta de su resumen agregado. La evidencia SHALL usar contenido sintético y
SHALL demostrar que el feedback no modifica la predicción ni devuelve
identificadores, registros individuales, narrativas, identidad o texto libre.

#### Scenario: Recorrido local conforme

- **WHEN** una persona ejecuta la comprobación con una API local configurada y
  un artefacto reproducible disponible
- **THEN** obtiene una predicción local válida, registra solo metadatos
  aprobados y recibe exclusivamente grupos agregados por versión, clase sugerida
  y decisión
- **AND** la evidencia declara que no existen autenticación, permisos reales,
  base compartida, despliegue, MLOps ni reentrenamiento automático

#### Scenario: Evidencia local no disponible o no conforme

- **WHEN** falta el artefacto local, la API no está disponible o una operación
  devuelve datos fuera del contrato
- **THEN** la comprobación informa un bloqueo seguro sin fabricar feedback,
  resumen ni estado verificado para `MED-04`

