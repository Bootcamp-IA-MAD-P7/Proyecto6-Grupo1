# local-classification-usability Specification

## Purpose
TBD - created by archiving change improve-local-classification-usability. Update Purpose after archive.
## Requirements
### Requirement: Resultado de clasificación comprensible

La interfaz SHALL mostrar la clase sugerida, la fuente contractual de la
respuesta, la confianza disponible, la versión disponible y el requisito de
revisión humana sin presentar una recomendación como decisión final.

#### Scenario: Predicción local real

- **WHEN** el cliente recibe una respuesta contractual desde la API local
- **THEN** la interfaz MUST identificarla como predicción local y mostrar los
  metadatos disponibles de forma secundaria y legible

#### Scenario: Respuesta mock

- **WHEN** el cliente usa la respuesta mock segura
- **THEN** la interfaz MUST identificarla como mock y no como salida de modelo

### Requirement: Alternativas y motivo de revisión seguros

La interfaz SHALL mostrar como máximo tres alternativas contractuales y SHALL
mantener un motivo de revisión visible, contractual o seguro por defecto. La
interfaz SHALL NOT inventar confianza, razones técnicas ni clases.

#### Scenario: Alternativas disponibles

- **WHEN** la respuesta incluye más de tres alternativas
- **THEN** la interfaz MUST presentar solo las tres primeras en el orden del
  contrato

#### Scenario: Motivo no proporcionado

- **WHEN** la respuesta requiere revisión humana sin motivo textual
- **THEN** la interfaz MUST mostrar un motivo seguro que no atribuya una causa
  inexistente al modelo

### Requirement: Estados del recorrido local

La interfaz SHALL comunicar carga, error recuperable y reinicio de la
clasificación. Las rutas administrativas conceptuales SHALL NOT usarse como
parte del recorrido funcional ni como evidencia de operación.

#### Scenario: Solicitud en curso

- **WHEN** la persona envía una clasificación válida
- **THEN** la interfaz MUST impedir el doble envío y comunicar que espera la
  respuesta local

#### Scenario: Error local recuperable

- **WHEN** la API local no está disponible o devuelve una respuesta inválida
- **THEN** la interfaz MUST mostrar un mensaje seguro y permitir iniciar una
  nueva clasificación
