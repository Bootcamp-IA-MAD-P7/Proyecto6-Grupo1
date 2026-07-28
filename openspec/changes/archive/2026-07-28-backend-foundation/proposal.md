# Proposal: backend-foundation

## Why

ClaimVox (React PWA) está integrada y funcional en `dev`, pero consume respuestas
simuladas locales. No existe un servicio HTTP que cargue el baseline evaluado
(`models/cfpb_baseline.pkl`, TF-IDF + LogisticRegression, gap 0.0482) y devuelva
predicciones reales conforme al contrato `docs/api/openapi.json`.

Sin este servicio:

- `ESS-04` (aplicación que productiviza el modelo) no puede verificarse;
- `003/T-007` (integrar servicio real) permanece bloqueada;
- el equipo no puede demostrar el flujo completo reclamación → predicción → revisión humana.

## Measurable outcomes

1. Un proceso HTTP responde a `POST /api/v1/predictions` con un `PredictionResponse` válido.
2. Un endpoint `GET /api/v1/health` devuelve el estado del servicio.
3. Cuando el artefacto de modelo está disponible localmente, la predicción es real (baseline evaluado).
4. Cuando el artefacto no está disponible, el servicio responde con un mock claramente identificado (`model_version: "mock-v0"`, `review_required: true`, `review_reasons: ["service_policy"]`).
5. Los tests de contrato del backend pasan contra `docs/api/openapi.json`.
6. Ninguna narrativa se loguea, persiste ni se incluye en la respuesta.

## Non-goals

- No implementar RAG ni procesamiento avanzado de texto (solo dejar una interfaz de extensión).
- No conectar directamente al CSV de la fuente CFPB.
- No crear base de datos ni persistencia de feedback.
- No desplegar en cloud ni dockerizar (será trabajo posterior: ADV-01, ADV-03).
- No implementar autenticación ni autorización (decisión pendiente según threat model).
- No modificar el contrato OpenAPI existente.
- No entrenar ni reentrenar el modelo.
- No inventar métricas, resultados ni decisiones de modelo.

## Affected delivery-level IDs

| ID | Impacto |
|---|---|
| `ESS-04` | Directamente: este cambio crea el servicio necesario para conectar la PWA a inferencia real |
| `ESS-01` | Parcialmente: el servicio carga y sirve el artefacto, pero el versionado formal del modelo es trabajo separado |
| `003/T-007` | Desbloquea: la tarea de integración frontend-backend podrá avanzar tras este cambio |

## Privacy and security impact

- Body logging prohibido: la narrativa del request no se registra en logs (threat model, security baseline).
- El servicio no persiste narrativas ni feedback por defecto.
- El artefacto se carga solo desde la ruta local controlada (`models/`), sin descarga externa.
- Las respuestas de error no exponen detalles internos (conforme a `ErrorResponse` del contrato).
- CORS, rate limiting y autenticación quedan fuera de alcance; se implementarán cuando se definan políticas.

## Capabilities

- `prediction-service`: servicio HTTP que recibe PredictionRequest y devuelve PredictionResponse.
- `health-endpoint`: endpoint de estado del servicio sin datos sensibles.
- `model-loading`: carga del artefacto baseline serializado (joblib) con fallback a mock.
- `predictor-interface`: puerto de extensión para alternar entre baseline real, mock y futura capa RAG.

## Tracking

- Jira: `PG-5`.
