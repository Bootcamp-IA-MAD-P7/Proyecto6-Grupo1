# Plan técnico: Experiencia de clasificación de reclamaciones

- Spec: [`spec.md`](spec.md)
- Estado: `mock_implemented`

## Solución propuesta

Separar el trabajo en dos etapas:

1. Contrato y mock: arquitectura de información, OpenAPI y estados verificables sin modelo.
2. Integración real: backend conectado a un artefacto aprobado posteriormente y consumido por el mismo cliente de inferencia.

```text
React PWA → cliente de inferencia → contrato OpenAPI → mock o servicio real
```

## Base técnica de la PWA

- React y TypeScript para componentes y contratos tipados.
- Vite para desarrollo, compilación y configuración de Vitest.
- `vite-plugin-pwa` para manifest, registro del service worker y shell instalable.
- Cliente de inferencia inyectable; esta tarea activa únicamente el adaptador mock.
- CSS propio basado en tokens para evitar acoplar la experiencia a una librería visual antes de validar el producto.

El service worker precacheará únicamente recursos estáticos. No se configurará caché de respuestas bajo `/api/` ni persistencia de narrativas.

La interfaz no conocerá scikit-learn ni detalles del modelo. El backend deberá adaptar el modelo al contrato estable.

## Responsabilidades y traspasos

| Área | Responsable | Estado y límite |
|---|---|---|
| Frontend y UX | Abel | Endurecer y validar la PWA mock mediante `T-008` y la PR `#14` |
| Arquitectura y coherencia transversal | Miguel | Mantener el contrato, decisiones, seguridad, documentación y límites de alcance |
| Backend | José | Preparar la futura integración de `T-007`; la implementación real sigue bloqueada por las decisiones de ML, privacidad y operación |
| Datos / EDA | Víctor | Aportar evidencia desde `001/T-004` para resolver idioma, longitud, desbalanceo y partición |

La asignación de José no autoriza a fabricar un modelo ni un endpoint de inferencia real. Puede revisar el OpenAPI, preparar adaptadores y detectar preguntas, pero la conexión real comienza únicamente cuando se levanten los bloqueos registrados.

## Reconciliación de la propuesta frontend del 21 de julio

La propuesta aportada por Abel se conserva como entrada de diseño y se adapta al estado alcanzado el 22 de julio. No se crea una segunda spec `001`, una carpeta `/frontend` ni otra rama con el mismo nombre.

| Tratamiento | Elementos |
|---|---|
| Incorporados | React, Vite, TypeScript, PWA, mocks sustituibles, responsive, accesibilidad, tests, documentación y Dependabot npm |
| Ya implementados | Base en `app/interface/`, contrato `/api/v1/predictions`, Vitest, Testing Library, ESLint, manifest, service worker y CSS basado en tokens |
| Pendientes de endurecimiento | Instalabilidad, iconos completos, capturas, revisión manual por viewport, evidencia de teclado, Lighthouse y medición de cobertura |
| Diferidos a nuevas decisiones o specs | Autenticación, roles, registro, dashboard, KPIs, historial, entrenamiento, voz, React Router, TanStack Query, Tailwind y shadcn/ui |

Las versiones instaladas y `app/interface/` son las fuentes de verdad técnicas. Cambiar de ubicación, librería visual o contrato requeriría justificar la migración antes de implementarla.

## Componentes implementados

- Formulario accesible de narrativa.
- Cliente de inferencia sustituible entre mock y servicio.
- Presentación de resultado y revisión.
- Gestión explícita de estados y errores.
- API `/api/v1/predictions` y health check mínimo.
- Fixtures sintéticos para desarrollo y tests.

El trabajo restante de frontend se limita a endurecer y revisar estos componentes; no autoriza nuevas áreas de producto.

## Estrategia de pruebas

- Contrato: OpenAPI válido como JSON y clases iguales al target CFPB.
- Unitarias y componentes: cinco pruebas verifican formulario, foco, mensajes, confianza nula, offline y errores; se medirá cobertura antes de acordar un umbral.
- Integración: mock OpenAPI antes del modelo real.
- End-to-end: envío, resultado, revisión, offline y servicio no disponible.
- Visual: viewport móvil, tablet y escritorio sin depender solo del color.
- PWA: build, manifest, service worker, iconos e instalación revisados con la versión de herramienta registrada.

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

El contrato y la React PWA ya están implementados contra mock en la misma rama. Su versión inicial puede evolucionar dentro de `v1` mientras no exista un consumidor publicado; una ruptura posterior exigirá una nueva versión. La reversión de la PR elimina la interfaz y sus checks sin migrar datos, porque no existe backend, persistencia ni modelo conectado.
