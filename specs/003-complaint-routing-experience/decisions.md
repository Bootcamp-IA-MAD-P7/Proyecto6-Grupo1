# Decisiones: Experiencia de clasificación de reclamaciones

## ADR-001 Desarrollar frontend contra contrato y mock

- Fecha: `2026-07-22`
- Estado: `accepted`
- Relacionada con: `R-003 a R-005, R-011, T-002, T-006`

### Decisión

La React PWA se desarrollará contra un OpenAPI estable y respuestas sintéticas. El servicio real adaptará posteriormente el modelo aprobado sin exponer detalles internos a la interfaz.

### Consecuencias

- Frontend puede avanzar sin esperar al entrenamiento.
- Contrato y taxonomía se prueban antes de integrar.
- La existencia del mock no puede presentarse como inferencia funcional.

## ADR-002 No persistir narrativas ni ofrecer routing automático en v1

- Fecha: `2026-07-22`
- Estado: `accepted`
- Relacionada con: `R-002, R-006 a R-009, R-012`

### Decisión

La primera versión envía una narrativa para una predicción puntual, no la registra por defecto, no la devuelve y no incluye feedback ni una cola recomendada. El usuario conserva la decisión operativa.

### Consecuencias

- Se reduce exposición de información personal y alcance prematuro.
- Feedback, historial y mapping a colas necesitarán specs y políticas propias.

## ADR-003 Tratar la confianza como dato opcional

- Fecha: `2026-07-22`
- Estado: `accepted`
- Relacionada con: `R-004, R-005, AC-002`

### Decisión

`confidence` puede ser nulo. Si el modelo no proporciona una probabilidad calibrada, la respuesta debe exigir revisión y la interfaz no mostrará porcentajes derivados o inventados.

### Consecuencias

- El contrato admite baselines sin falsa precisión.
- El umbral de revisión permanece pendiente de evaluación experimental.

## ADR-004 Utilizar React PWA para productivizar el modelo

- Fecha: `2026-07-23`
- Estado: `accepted`
- Relacionada con: `ESS-04, R-001 a R-012, T-006, T-007`

### Contexto

El briefing propone Streamlit, Gradio o Dash como ejemplos de aplicación. El equipo ha confirmado que el objetivo evaluable es productivizar el modelo, no utilizar obligatoriamente una de esas tecnologías.

### Decisión

La aplicación del proyecto será una React PWA. Esta elección cumple el criterio tecnológico cuando la interfaz consuma inferencia real y permita introducir datos válidos y obtener una predicción multiclase.

### Consecuencias

- No es necesario añadir una segunda interfaz en Streamlit, Gradio o Dash.
- El contrato y los mocks permiten avanzar en UX, pero no verifican `ESS-04`.
- `ESS-04` solo se cumple cuando frontend, servicio y modelo real están integrados y probados.
- Una evolución nativa permanece fuera de alcance mientras no exista una necesidad demostrada.
