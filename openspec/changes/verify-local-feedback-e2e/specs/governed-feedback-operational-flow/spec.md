## ADDED Requirements

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
