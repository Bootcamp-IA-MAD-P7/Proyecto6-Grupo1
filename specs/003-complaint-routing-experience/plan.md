# Plan técnico: Experiencia de clasificación de reclamaciones

- Spec: [`spec.md`](spec.md)
- Estado: `approved`

## Solución propuesta

Separar el trabajo en dos etapas:

1. Contrato y mock: arquitectura de información, OpenAPI y estados verificables sin modelo.
2. Integración real: React PWA y backend conectados a un artefacto aprobado posteriormente.

```text
React PWA → cliente de inferencia → contrato OpenAPI → mock o servicio real
```

La interfaz no conocerá scikit-learn ni detalles del modelo. El backend deberá adaptar el modelo al contrato estable.

## Componentes previstos

- Formulario accesible de narrativa.
- Cliente de inferencia sustituible entre mock y servicio.
- Presentación de resultado y revisión.
- Gestión explícita de estados y errores.
- API `/api/v1/predictions` y health check mínimo.
- Fixtures sintéticos para desarrollo y tests.

## Estrategia de pruebas

- Contrato: OpenAPI válido como JSON y clases iguales al target CFPB.
- Unitarias: validación de estados y transformación de respuesta cuando exista frontend.
- Componentes: teclado, foco, mensajes, confianza nula y errores.
- Integración: mock OpenAPI antes del modelo real.
- End-to-end: envío, resultado, revisión, offline y servicio no disponible.
- Visual: viewport móvil, tablet y escritorio sin depender solo del color.

## Riesgos

| Riesgo | Mitigación |
|---|---|
| La UI se acopla a un modelo concreto | OpenAPI y cliente sustituible |
| Confianza no calibrada | Campo nulo y revisión obligatoria |
| PII en texto o logs | Aviso, no persistencia y body logging prohibido |
| Flujo B2B incorrecto | Validación de usuario antes de cerrar la spec |
| PWA promete inferencia offline | Offline solo para shell y explicación |
| Contrato y clases divergen | Test automático contra target versionado |

## Entrega y reversión

El contrato se integra antes de React para permitir mocks. Su versión inicial puede evolucionar dentro de `v1` mientras no exista consumidor publicado; una ruptura posterior exigirá una nueva versión. Revertir esta definición no requiere migración porque todavía no hay implementación.
