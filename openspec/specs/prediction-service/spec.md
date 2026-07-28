## Purpose

Expose an HTTP endpoint that receives a complaint narrative and returns a multiclass
prediction conforming to `docs/api/openapi.json`, using a real baseline when locally
available or a clearly identified mock otherwise.

## Requirements

### Requirement: Prediction endpoint accepts PredictionRequest

The service SHALL expose `POST /api/v1/predictions` accepting a body that conforms
to `PredictionRequest` in `docs/api/openapi.json`.

#### Scenario: Valid narrative produces a prediction

- **GIVEN** the service is running and a predictor is loaded
- **WHEN** a client submits a valid `PredictionRequest`
- **THEN** it returns status 200 and a `PredictionResponse` whose class is one of the 11 canonical labels

#### Scenario: Invalid narrative is rejected

- **GIVEN** the service is running
- **WHEN** a client submits an empty, whitespace-only, missing, or additional field
- **THEN** the response is a contract-conformant safe validation error

### Requirement: Prediction response preserves the contract and privacy

The service SHALL return every required `PredictionResponse` field, use canonical
classes, and never echo a submitted narrative in a success or error response.

#### Scenario: Response contains contract fields

- **GIVEN** a valid request is submitted
- **WHEN** the service responds
- **THEN** its identifier, class, alternatives, confidence, review state, versions, timestamp, and warnings conform to the contract

#### Scenario: Response does not expose the narrative

- **GIVEN** any request
- **WHEN** the service returns a response
- **THEN** the response contains no submitted narrative, stack trace, model path, or internal detail

### Requirement: No narrative logging or persistence

The service SHALL NOT log, persist, or include a complaint narrative in outputs
outside internal vectorization during prediction.

#### Scenario: Backend handles a request

- **WHEN** a prediction is processed
- **THEN** no application output or file persistence contains its narrative text

### Requirement: Protección proporcional de la API local

El servicio de predicción SHALL aplicar un límite configurable de tamaño de
entrada, una frecuencia configurable en memoria y cabeceras de respuesta de
seguridad compatibles con una API local. SHALL devolver errores contractuales y
no revelar contenido, rutas internas ni detalles de implementación.

#### Scenario: Entrada fuera del límite

- **WHEN** una solicitud excede el límite configurado de narrativa
- **THEN** el servicio la rechaza con un error seguro conforme al contrato sin cargar el modelo ni registrar el cuerpo

#### Scenario: Frecuencia superada

- **WHEN** una fuente local supera el umbral de frecuencia configurado
- **THEN** el servicio devuelve una respuesta `429` segura y el cliente puede comunicar una recuperación sin mostrar detalles internos

#### Scenario: Respuesta de la API

- **WHEN** el servicio responde a una ruta de salud o predicción
- **THEN** incluye las cabeceras de seguridad aprobadas y mantiene CORS explícito sin comodines ni credenciales
