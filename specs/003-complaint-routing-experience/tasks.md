# Tareas: Experiencia de clasificación de reclamaciones

- Spec: [`spec.md`](spec.md)
- Plan: [`plan.md`](plan.md)

## Fase 0 — Contrato y diseño (completadas)

## T-001 Definir flujo y límites del producto

- Estado: `[x]`
- Responsable: `Producto / UX`
- Requisitos cubiertos: `R-001, R-002, R-006 a R-010, R-012`
- Evidencia obtenida: spec y arquitectura de información con estados y fuera de alcance explícitos.

## T-002 Versionar el contrato de inferencia simulado

- Estado: `[x]`
- Responsable: `Aplicación / plataforma`
- Dependencias: `T-001`
- Requisitos cubiertos: `R-003 a R-005, R-007, R-009, R-011, R-012`
- Evidencia obtenida: `docs/api/openapi.json` y tests contra las once clases.

## T-003 Completar límites iniciales de seguridad

- Estado: `[x]`
- Responsable: `Seguridad / aplicación`
- Dependencias: `T-001, T-002`
- Requisitos cubiertos: `R-002, R-006 a R-009, R-011`
- Evidencia obtenida: modelo de amenazas actualizado y extensiones de tratamiento en OpenAPI.

## T-004 Validar el contrato documental

- Estado: `[x]`
- Responsable: `QA`
- Dependencias: `T-002, T-003`
- Requisitos cubiertos: `AC-004, AC-005, AC-007`
- Evidencia obtenida: tests automatizados de esquema, clases, privacidad, revisión y rutas.

## T-005 Contrastar el flujo con negocio

- Estado: `[!]`
- Responsable: `Producto / equipo`
- Dependencias: `T-001`
- Requisitos cubiertos: `Q-001, Q-005, Q-006`
- Bloqueante: falta una persona usuaria o responsable de negocio con quien contrastar el flujo.
- Evidencia obtenida: pendiente.

## T-006 Implementar la React PWA con mock

- Estado: `[x]`
- Responsable: `Frontend / UX`
- Dependencias: `T-001 a T-004`
- Requisitos cubiertos: `AC-001 a AC-004, AC-006`
- Trabajo: crear shell PWA, formulario, cliente mock, resultado y estados accesibles.
- Evidencia obtenida: React PWA, cliente mock sustituible, 5 tests de interacción, lint accesible, build con service worker y [informe de validación](../../reports/validation/complaint_routing_pwa.md).

## T-007 Integrar el servicio real

- Estado: `[!]`
- Responsable: `José / Backend, con contrato de ML pendiente`
- Dependencias: `T-006`, `001/T-004 a T-006`
- Bloqueante: EDA, modelo aprobado, idioma, límites y política de revisión. La asignación de José permite revisar y preparar el diseño, pero no autoriza a conectar inferencia real antes de resolverlos.
- Evidencia obtenida: pendiente.

## T-008 Endurecer y revisar la entrega frontend

- Estado: `[~]`
- Responsable: `Abel / Frontend / UX`
- Dependencias: `T-006`
- Requisitos cubiertos: `R-010, R-013, R-014, AC-006, AC-008, AC-009`
- Trabajo:
  - revisar la implementación existente en `app/interface/` sin recrearla en `/frontend`;
  - comprobar teclado, foco y estados con tecnología asistiva disponible;
  - revisar móvil, tablet y escritorio y conservar capturas con contenido sintético;
  - completar iconos e instalabilidad PWA;
  - ejecutar Lighthouse registrando versión, entorno y resultados;
  - medir cobertura antes de proponer un umbral obligatorio;
  - activar Dependabot para npm y actualizar las evidencias afectadas.
- Verificación: `npm run typecheck`, `npm run lint`, `npm test`, `npm run build`, revisión manual y actualización del informe de validación.
- Evidencia obtenida: Dependabot npm incorporado durante la reconciliación; revisión manual, capturas, iconos, Lighthouse y cobertura pendientes.

## Fase 1 — Setup base

## T-009 Limpiar `app/interface/` preservando contratos

- Estado: `[ ]`
- Responsable: `Frontend / UX`
- Dependencias: `T-006`
- Requisitos cubiertos: `R-015`
- Trabajo: eliminar archivos obsoletos de `app/interface/` (CSS tokens, componentes viejos, tests viejos) preservando `src/contracts/prediction.ts`, `src/services/prediction-client.ts` y `src/services/mock-prediction-client.ts`.
- Verificación: la carpeta `app/interface/` contiene únicamente contratos y servicios preservados.

## T-010 Crear `package.json` con dependencias del stack completo

- Estado: `[ ]`
- Responsable: `Frontend / UX`
- Dependencias: `T-009`
- Requisitos cubiertos: `R-015 a R-020`
- Trabajo: definir React 19, Vite 8, TypeScript, Tailwind CSS, shadcn/ui, React Router v6, TanStack Query, @xenova/transformers, Vitest, Testing Library, ESLint, Prettier.
- Verificación: `package.json` contiene todas las dependencias declaradas.

## T-011 Instalar dependencias npm

- Estado: `[ ]`
- Responsable: `Frontend / UX`
- Dependencias: `T-010`
- Trabajo: ejecutar `npm install` y verificar que no hay conflictos de versiones.
- Verificación: `npm run dev` arranca sin errores.

## T-012 Configurar Vite con plugin PWA

- Estado: `[ ]`
- Responsable: `Frontend / UX`
- Dependencias: `T-011`
- Requisitos cubiertos: `R-008, AC-009`
- Trabajo: configurar `vite.config.ts` con `@vitejs/plugin-react` y `vite-plugin-pwa`.
- Verificación: `npm run build` genera service worker y manifest.

## T-013 Configurar TypeScript

- Estado: `[ ]`
- Responsable: `Frontend / UX`
- Dependencias: `T-011`
- Trabajo: crear `tsconfig.json`, `tsconfig.app.json`, `tsconfig.node.json` con estricto habilitado.
- Verificación: `npx tsc --noEmit` pasa sin errores.

## T-014 Configurar Tailwind CSS

- Estado: `[ ]`
- Responsable: `Frontend / UX`
- Dependencias: `T-011`
- Requisitos cubiertos: `R-015`
- Trabajo: instalar `tailwindcss`, `@tailwindcss/vite`, crear `tailwind.config.ts` con tokens de diseño del proyecto (forest, paper, sand, gold, rust).
- Verificación: `npm run dev` aplica estilos de Tailwind.

## T-015 Inicializar shadcn/ui

- Estado: `[ ]`
- Responsable: `Frontend / UX`
- Dependencias: `T-014`
- Requisitos cubiertos: `R-015`
- Trabajo: ejecutar `npx shadcn@latest init`, configurar `components.json`, instalar componentes base (Button, Card, Input, Label, Badge, Alert).
- Verificación: componentes se importan y renderizan correctamente.

## T-016 Configurar ESLint y Prettier

- Estado: `[ ]`
- Responsable: `Frontend / UX`
- Dependencias: `T-011`
- Trabajo: configurar `eslint.config.js` con React hooks, a11y, refresh y Prettier integration.
- Verificación: `npm run lint` pasa sin errores.

## T-017 Crear `index.html` y puntos de entrada

- Estado: `[ ]`
- Responsable: `Frontend / UX`
- Dependencias: `T-012, T-013`
- Trabajo: crear `index.html` con meta tags y `src/main.tsx` con StrictMode.
- Verificación: `npm run dev` muestra la aplicación en el navegador.

## Fase 2 — Estructura, layouts y routing

## T-018 Crear estructura de carpetas

- Estado: `[ ]`
- Responsable: `Frontend / UX`
- Dependencias: `T-017`
- Trabajo: crear `src/components/`, `src/components/ui/`, `src/layouts/`, `src/pages/`, `src/pages/user/`, `src/pages/admin/`, `src/pages/auth/`, `src/hooks/`, `src/lib/`, `src/contracts/`, `src/services/`.
- Verificación: estructura existe y es accesible desde el código.

## T-019 Implementar AuthLayout

- Estado: `[ ]`
- Responsable: `Frontend / UX`
- Dependencias: `T-018`
- Requisitos cubiertos: `R-018, R-019, AC-013`
- Trabajo: layout para página de login con logo, título y área de contenido central.
- Verificación: componente renderiza correctamente en diferentes viewports.

## T-020 Implementar UserLayout

- Estado: `[ ]`
- Responsable: `Frontend / UX`
- Dependencias: `T-018`
- Requisitos cubiertos: `R-019`
- Trabajo: layout con sidebar de navegación (HomePage, ClassificationPage) y header con información de usuario y botón de logout.
- Verificación: navegación entre vistas funciona sin recarga.

## T-021 Implementar AdminLayout

- Estado: `[ ]`
- Responsable: `Frontend / UX`
- Dependencias: `T-018`
- Requisitos cubiertos: `R-019, AC-011`
- Trabajo: layout con sidebar de navegación (DashboardPage, TrainingPage, ModelsPage) y header con badge de admin.
- Verificación: admin accede a todas las vistas.

## T-022 Implementar mock auth con localStorage

- Estado: `[ ]`
- Responsable: `Frontend / UX`
- Dependencias: `T-018`
- Requisitos cubiertos: `R-018, AC-010, AC-011, AC-013`
- Trabajo: crear `src/services/auth-client.ts` con login mock que persiste rol en localStorage.
- Verificación: login/logout funcionan; roles se persisten.

## T-023 Configurar React Router con rutas base

- Estado: `[ ]`
- Responsable: `Frontend / UX`
- Dependencias: `T-019 a T-022`
- Requisitos cubiertos: `R-016, AC-010, AC-011, AC-013`
- Trabajo: crear `src/App.tsx` con `BrowserRouter`, rutas protegidas por rol, redirección a login si no autenticado.
- Verificación: navegación funciona; rutas protegidas redirigen correctamente.

## T-024 Crear AuthProvider y hook useAuth

- Estado: `[ ]`
- Responsable: `Frontend / UX`
- Dependencias: `T-022`
- Requisitos cubiertos: `R-018`
- Trabajo: crear `src/providers/AuthProvider.tsx` con React Context y `src/hooks/use-auth.ts`.
- Verificación: `useAuth()` devuelve user, role, login, logout.

## Fase 3 — Vistas de usuario

## T-025 Crear HomePage con KPIs mock

- Estado: `[ ]`
- Responsable: `Frontend / UX`
- Dependencias: `T-020, T-024`
- Requisitos cubiertos: `R-017`
- Trabajo: página con tarjetas de KPIs mock (total reclamaciones, precisión del modelo, tiempo promedio) y acceso rápido a ClassificationPage.
- Verificación: KPIs se muestran correctamente.

## T-026 Crear ClassificationPage

- Estado: `[ ]`
- Responsable: `Frontend / UX`
- Dependencias: `T-020, T-015`
- Requisitos cubiertos: `R-001 a R-007, AC-001 a AC-004`
- Trabajo: formulario de narrativa con validación, botón de clasificar, integración con prediction client y presentación de resultado.
- Verificación: flujo completo de envío y resultado funciona con mock.

## T-027 Integrar PredictionResult con nuevo diseño

- Estado: `[ ]`
- Responsable: `Frontend / UX`
- Dependencias: `T-026, T-015`
- Requisitos cubiertos: `R-004 a R-006, AC-002`
- Trabajo: adaptar componente `PredictionResult` a Tailwind + shadcn/ui.
- Verificación: resultado se muestra correctamente con todos los estados.

## T-028 Agregar dictado por voz con Whisper Tiny

- Estado: `[ ]`
- Responsable: `Frontend / UX`
- Dependencias: `T-026`
- Requisitos cubiertos: `R-020, AC-012`
- Trabajo: instalar `@xenova/transformers`, crear `src/hooks/use-voice-dictation.ts`, integrar botón de grabación en ClassificationPage.
- Verificación: dictado convierte voz a texto en el campo de narrativa.

## Fase 4 — Vistas de admin

## T-029 Crear DashboardPage

- Estado: `[ ]`
- Responsable: `Frontend / UX`
- Dependencias: `T-021`
- Requisitos cubiertos: `R-017, AC-011`
- Trabajo: dashboard con métricas mock (distribución de clases, volumen diario, tasa de revisión).
- Verificación: dashboard se muestra correctamente.

## T-030 Crear TrainingPage

- Estado: `[ ]`
- Responsable: `Frontend / UX`
- Dependencias: `T-021`
- Requisitos cubiertos: `R-017, AC-011`
- Trabajo: página de simulación de entrenamiento con progreso mock y métricas de modelo.
- Verificación: simulación de entrenamiento funciona.

## T-031 Crear ModelsPage

- Estado: `[ ]`
- Responsable: `Frontend / UX`
- Dependencias: `T-021`
- Requisitos cubiertos: `R-017, AC-011`
- Trabajo: tabla de modelos con versiones, métricas y estado mock.
- Verificación: tabla se muestra correctamente con datos mock.

## T-032 Configurar TanStack Query

- Estado: `[ ]`
- Responsable: `Frontend / UX`
- Dependencias: `T-017`
- Requisitos cubiertos: `R-017`
- Trabajo: instalar `@tanstack/react-query`, crear `QueryClientProvider`, hooks con mock data preparados para sustitución por API REST.
- Verificación: `useQuery` y `useMutation` funcionan con datos mock.

## Fase 5 — PWA, tests y documentación

## T-033 Completar configuración PWA

- Estado: `[ ]`
- Responsable: `Frontend / UX`
- Dependencias: `T-012`
- Requisitos cubiertos: `R-008, AC-009`
- Trabajo: verificar manifest, service worker, iconos y test de instalabilidad.
- Verificación: Lighthouse PWA score >= 90.

## T-034 Escribir tests para flujos principales

- Estado: `[ ]`
- Responsable: `Frontend / UX`
- Dependencias: `T-026, T-023`
- Requisitos cubiertos: `AC-001 a AC-006, AC-010 a AC-013`
- Trabajo: tests para formulario, resultado, offline, error, auth, routing y dictado.
- Verificación: `npm test` pasa con cobertura >= 70%.

## T-035 Verificar responsive y accesibilidad

- Estado: `[ ]`
- Responsable: `Frontend / UX`
- Dependencias: `T-026, T-029`
- Requisitos cubiertos: `R-010, AC-006, AC-008`
- Trabajo: revisar viewports móvil, tablet y escritorio; verificar foco visible, ARIA labels, contraste de colores.
- Verificación: capturas sintéticas de cada viewport y reporte de accesibilidad.

## T-036 Actualizar ADR de ubicación

- Estado: `[ ]`
- Responsable: `Frontend / UX`
- Dependencias: `T-009`
- Requisitos cubiertos: `R-015`
- Trabajo: registrar ADR-008 confirmando `app/interface/` como ubicación del frontend.
- Verificación: `decisions.md` contiene ADR-008.

## T-037 Actualizar AGENTS.md

- Estado: `[ ]`
- Responsable: `Frontend / UX`
- Dependencias: `T-036`
- Trabajo: actualizar instrucciones de agentes para reflejar stack actual (Tailwind, shadcn, router, auth mock).
- Verificación: `AGENTS.md` refleja el stack correcto.

## T-038 Auditoría final de dependencias

- Estado: `[ ]`
- Responsable: `Frontend / UX`
- Dependencias: `T-034, T-035`
- Trabajo: ejecutar `npm audit`, `npm outdated`, actualizar dependencias obsoletas.
- Verificación: `npm audit` no tiene vulnerabilidades críticas; `npm run build` funciona.

## Checklist de cierre

- [x] Contrato y estados iniciales están definidos.
- [x] Las clases y límites de privacidad están verificados.
- [ ] El flujo ha sido validado con negocio.
- [x] La PWA consume el contrato mediante mock.
- [ ] Tailwind CSS y shadcn/ui están integrados y funcionando.
- [ ] React Router con rutas protegidas funciona correctamente.
- [ ] Auth mock con roles user/admin funciona.
- [ ] Vistas de usuario (HomePage, ClassificationPage) implementadas.
- [ ] Vistas de admin (DashboardPage, TrainingPage, ModelsPage) implementadas.
- [ ] Dictado por voz con Whisper Tiny funciona.
- [ ] La integración real cumple las decisiones de datos y modelo.
- [ ] Existen evidencias de accesibilidad y responsive.
- [ ] Tests con cobertura >= 70%.
- [ ] PWA instalable con Lighthouse score >= 90.
- [ ] `T-008` dispone de evidencias de instalabilidad, dependencias, capturas y calidad frontend.
