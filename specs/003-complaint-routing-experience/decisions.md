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

## ADR-004 Utilizar una base PWA mínima y sustituible

- Fecha: `2026-07-22`
- Estado: `accepted`
- Relacionada con: `R-008, R-010, T-006`

### Decisión

La primera interfaz utiliza React, TypeScript, Vite y `vite-plugin-pwa`, con CSS basado en tokens y sin una librería visual. El cliente de inferencia se inyecta para sustituir el mock por el servicio real sin acoplar componentes al modelo.

El service worker solo precachea el shell estático. No existe caché runtime para `/api/` ni fallback que fabrique predicciones offline.

### Consecuencias

- El equipo puede probar la experiencia, accesibilidad y PWA antes del backend.
- La base visual puede evolucionar después de validar producto sin migrar un sistema de componentes prematuro.
- La instalación PWA no implica inferencia offline.

## ADR-005 Mantener visible el carácter provisional

- Fecha: `2026-07-22`
- Estado: `accepted`
- Relacionada con: `Q-001, Q-002, T-005, T-006`

### Decisión

La interfaz identifica el prototipo, las respuestas simuladas y la ausencia de un modelo entrenado. La copia en inglés sirve únicamente para probar el flujo y no cierra la política de idioma.

### Consecuencias

- Una demo no se confunde con capacidad predictiva real.
- El idioma y el flujo B2B continúan bloqueados hasta disponer de evidencia de usuario y EDA.

## ADR-006 Reconciliar la propuesta frontend previa con la spec vigente

- Fecha: `2026-07-22`
- Estado: `accepted`
- Relacionada con: `R-010, R-013, R-014, T-008`

### Contexto

Abel aportó una propuesta frontend fechada el 21 de julio, anterior a la creación de la spec `003`, la ubicación `app/interface/`, el OpenAPI `0.1.0` y la implementación de la PWA mock. La propuesta contiene requisitos de calidad aprovechables y una ampliación de producto todavía no aprobada.

### Decisión

Integrar en `003/T-008` los requisitos de instalabilidad, responsive, accesibilidad, pruebas, evidencias, documentación y Dependabot npm. Mantener la implementación existente, sus versiones y `/api/v1/predictions` como fuentes de verdad.

Autenticación, roles, registro, dashboard, KPIs, historial, entrenamiento y voz se conservan como propuestas para Jira. React Router, TanStack Query, Tailwind y shadcn/ui solo se adoptarán si una funcionalidad aprobada demuestra su necesidad.

### Consecuencias

- Se aprovecha el trabajo de Abel sin duplicar specs, carpetas, ramas ni contratos.
- La PR #14 mantiene un alcance verificable y puede pasar a su revisión frontend.
- Las ampliaciones de producto no se confunden con capacidades existentes.
- Cualquier propuesta diferida requerirá historia de Jira, spec y decisión propias antes de implementarse.
