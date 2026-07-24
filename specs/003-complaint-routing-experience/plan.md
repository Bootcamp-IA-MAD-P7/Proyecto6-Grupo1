# Plan técnico: Experiencia de clasificación de reclamaciones

- Spec: [`spec.md`](spec.md)
<<<<<<< HEAD
- Estado: `mock_implemented`
=======
- Estado: `approved`
>>>>>>> 5558ae2204151767a53be0e45102bd04a3b6da83

## Solución propuesta

Separar el trabajo en dos etapas:

1. Contrato y mock: arquitectura de información, OpenAPI y estados verificables sin modelo.
2. Integración real: backend conectado a un artefacto aprobado posteriormente y consumido por el mismo cliente de inferencia.

```text
React PWA → cliente de inferencia → contrato OpenAPI → mock o servicio real
```

## Base técnica de la PWA

- React 19 y TypeScript para componentes y contratos tipados.
- Vite 8 para desarrollo, compilación y configuración de Vitest.
- `vite-plugin-pwa` para manifest, registro del service worker y shell instalable.
- Tailwind CSS para utility-first styling con tokens de diseño del proyecto.
- shadcn/ui para componentes accesibles y reutilizables construidos sobre Tailwind.
- React Router v6 para navegación entre vistas con rutas protegidas por rol.
- TanStack Query para gestión de estado del servidor, caché y datos mock.
- @xenova/transformers (Whisper Tiny) para dictado por voz local sin servicios externos.
- Cliente de inferencia inyectable; esta fase activa únicamente el adaptador mock.
- Auth mock con localStorage y roles (user/admin) para demostración.
- Vitest + Testing Library para tests unitarios y de componente.

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

La propuesta aportada por Abel se conserva como entrada de diseño y se adapta al estado alcanzado. No se crea una segunda spec `001`, una carpeta `/frontend` ni otra rama con el mismo nombre.

| Tratamiento | Elementos |
|---|---|
| Incorporados | React 19, Vite 8, TypeScript, PWA, mocks sustituibles, responsive, accesibilidad, tests, documentación y Dependabot npm |
| Incorporados (expansión actual) | Tailwind CSS, shadcn/ui, React Router v6, TanStack Query, @xenova/transformers, auth mock, layouts, admin views |
| Ya implementados | Base en `app/interface/`, contrato `/api/v1/predictions`, Vitest, Testing Library, ESLint, manifest, service worker, prediction client y prediction result |
| Pendientes de endurecimiento | Instalabilidad, iconos completos, capturas, revisión manual por viewport, evidencia de teclado, Lighthouse y medición de cobertura |
| Diferidos a nuevas specs | Backend, servicio de inferencia real, entrenamiento de modelos, despliegue cloud |

Las versiones instaladas y `app/interface/` son las fuentes de verdad técnicas. La ubicación fue confirmada en ADR-008.

## Estructura de ramas y commits

El trabajo se distribuye en 30 commits sobre la rama `feature/complaint-routing-pwa` (PR #14). Cada commit corresponde a una tarea y sigue conventional commits.

### Fase 1 — Setup base (T-001 a T-009)

| Commit | Tarea |
|---|---|
| `feat: remove obsolete files preserving contracts` | T-001 |
| `feat: create package.json with full stack dependencies` | T-002 |
| `chore: install npm dependencies` | T-003 |
| `feat: configure Vite with PWA plugin` | T-004 |
| `chore: configure TypeScript` | T-005 |
| `feat: add Tailwind CSS configuration` | T-006 |
| `feat: initialize shadcn/ui` | T-007 |
| `chore: configure ESLint and Prettier` | T-008 |
| `feat: create index.html and entry points` | T-009 |

### Fase 2 — Estructura y layouts (T-010 a T-014, T-022, T-023)

| Commit | Tarea |
|---|---|
| `feat: create project folder structure` | T-010 |
| `feat: implement AuthLayout` | T-011 |
| `feat: implement UserLayout` | T-012 |
| `feat: implement AdminLayout` | T-013 |
| `feat: configure React Router` | T-014 |
| `feat: implement mock auth with localStorage` | T-022 |
| `feat: create AuthProvider and useAuth hook` | T-023 |

### Fase 3 — Vistas de usuario (T-015 a T-018)

| Commit | Tarea |
|---|---|
| `feat: create HomePage with KPIs mock` | T-015 |
| `feat: create ClassificationPage` | T-016 |
| `feat: integrate PredictionResult` | T-017 |
| `feat: add voice dictation with Whisper Tiny` | T-018 |

### Fase 4 — Vistas de admin (T-019 a T-021, T-024)

| Commit | Tarea |
|---|---|
| `feat: create DashboardPage` | T-019 |
| `feat: create TrainingPage` | T-020 |
| `feat: create ModelsPage` | T-021 |
| `feat: configure TanStack Query` | T-024 |

### Fase 5 — PWA, tests y documentación (T-025 a T-030)

| Commit | Tarea |
|---|---|
| `feat: complete PWA configuration` | T-025 |
| `test: add main flow tests` | T-026 |
| `test: verify responsive and accessibility` | T-027 |
| `docs: update ADR for app/interface location` | T-028 |
| `docs: update AGENTS.md` | T-029 |
| `chore: final dependency audit` | T-030 |

## Componentes implementados

- Formulario accesible de narrativa.
- Cliente de inferencia sustituible entre mock y servicio.
- Presentación de resultado y revisión.
- Gestión explícita de estados y errores.
- Contrato `/api/v1/predictions` y health check mínimo.
- Fixtures sintéticos para desarrollo y tests.

## Componentes a implementar (expansión actual)

- Tailwind CSS + shadcn/ui como sistema visual.
- React Router v6 con rutas protegidas por rol.
- AuthProvider con mock localStorage (user/admin).
- AuthLayout, UserLayout, AdminLayout.
- HomePage con KPIs mock.
- ClassificationPage con formulario y dictado por voz.
- DashboardPage, TrainingPage, ModelsPage para admin.
- TanStack Query para datos mock.
- @xenova/transformers (Whisper Tiny) para dictado local.

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
| Migración a Tailwind rompe estilos existentes | Reescribir estilos con tokens de Tailwind; tests de visual |
| Auth mock confunde con auth real | Etiqueta visible "Mock auth" en interfaz |
| Whisper Tiny no carga en todos los browsers | Fallback a input de texto; detección de soporte WebGPU |

## Entrega y reversión

El contrato y la React PWA están implementados contra mock en la rama `feature/complaint-routing-pwa` (PR #14). La expansión agrega Tailwind, shadcn/ui, React Router, TanStack Query, auth mock, layouts, vistas de admin y dictado por voz en 30 commits sobre la misma rama. Su versión inicial puede evolucionar dentro de `v1` mientras no exista un consumidor publicado; una ruptura posterior exigirá una nueva versión. La reversión de la PR elimina la interfaz y sus checks sin migrar datos, porque no existe backend, persistencia ni modelo conectado.
