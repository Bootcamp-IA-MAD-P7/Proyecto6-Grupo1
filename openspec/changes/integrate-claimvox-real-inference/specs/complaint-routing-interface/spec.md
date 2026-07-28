## MODIFIED Requirements

### Requirement: Cliente de predicción desacoplado y tipado

La interfaz MUST utilizar un contrato TypeScript alineado con
`PredictionRequest` y `PredictionResponse` de `docs/api/openapi.json`,
manteniendo el cliente de predicción separado de los componentes visuales. Con una
URL local de API configurada explícitamente, el cliente MAY solicitar el servicio
real; sin ella, MUST conservar el cliente mock. Ningún modo puede leer el CSV ni
acceder a artefactos de entrenamiento desde el navegador.

#### Scenario: Uso del cliente mock

- **GIVEN** que no hay una URL local de API configurada
- **WHEN** el formulario envía una narrativa válida
- **THEN** la interfaz invocará un cliente mock que respete el contrato TypeScript sin leer el CSV ni acceder a artefactos de entrenamiento

#### Scenario: Uso del cliente de servicio local

- **GIVEN** que una URL local de API está configurada explícitamente
- **WHEN** el formulario envía una narrativa válida con conexión disponible
- **THEN** la interfaz enviará únicamente `PredictionRequest.narrative` al endpoint versionado y validará la respuesta antes de mostrarla

#### Scenario: Respuesta incompatible

- **GIVEN** una respuesta que no cumple el contrato o contiene una clase fuera del contrato versionado
- **WHEN** el cliente la valida
- **THEN** la interfaz la tratará como error y no mostrará una recomendación aparentemente válida
