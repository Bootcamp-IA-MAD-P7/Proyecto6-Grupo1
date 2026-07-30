## 1. Layout unificado por roles

- [x] 1.1 [Frontend/UX] Rediseñar `UserLayout.tsx`: sidebar única que
  filtra ítems de navegación por `user.role` usando `hasRole()`. User:
  Home, Classify, Settings. Admin: Home, Classify, Dashboard, Training,
  Models, Settings. Cabecera con nombre, rol y botón de cierre de sesión.
  `ThemeToggle` en sección Settings al pie. Barra de progreso (`StepProgress`
  component) en la zona de contenido.
  Evidencia: `npm run typecheck` y revisión visual con ambos roles.
- [x] 1.2 [Frontend/UX] Eliminar `AdminLayout.tsx`. Ajustar `App.tsx` para
  que todas las rutas protegidas y públicas usen `UserLayout`.
  Evidencia: las rutas `/admin/*` siguen funcionando con el layout unificado.
- [x] 1.3 [Frontend/UX] Actualizar `UserLayout.test.tsx`: reemplazar
  asserción de "Local classification prototype" por verificación de ítems
  según rol. Verificar que admin ve Dashboard, Training, Models y user no.
  Evidencia: `npm test -- --run` pasa.

## 2. Flujo de clasificación en 4 pasos

- [x] 2.1 [Frontend/UX] Crear componente `StepProgress` que muestre 4
  pasos (Describe, Review, Guidance, Next step) con el paso actual
  resaltado. Responsive y accesible.
  Evidencia: `npm run typecheck`.
- [x] 2.2 [Frontend/UX] Rediseñar `ClassificationPage.tsx` con estado
  `step: 1 | 2 | 3 | 4`. Step 1: textarea ≤6 líneas visuales (clase CSS
  `max-h-[9rem]` o similar), dictado, botón "Revisar texto". Step 2:
  resumen del texto, botones "Classify complaint" y "Back". Step 3:
  resultado con `PredictionResult`. Step 4: opciones post-clasificación.
  La barra de progreso se integra en la parte superior.
  Evidencia: `npm run typecheck` y `npm test -- --run` pasa.
- [x] 2.3 [Frontend/UX] Actualizar `ClassificationPage.test.tsx`:
  reemplazar asserciones de "Mock response", "Interface demonstration
  only", "Classify complaint" por los nuevos textos en español y la nueva
  estructura de pasos. Mantener cobertura de estados (offline, error,
  rate-limit, voice dictation).
  Evidencia: `npm test -- --run` pasa con cobertura equivalente.

## 3. Etiquetas profesionales

- [x] 3.1 [Frontend/UX] Modificar `PredictionResult.tsx`: eliminar "Mock
  response", "Interface demonstration only". Cuando `clientMode === 'mock'`
  mostrar "The prediction service is unavailable" sin etiquetar
  como mock. Cuando `clientMode === 'local_api'` mostrar "Predicción
  local" con versión y confianza.
  Evidencia: `npm test -- --run` pasa.
- [x] 3.2 [Frontend/UX] Actualizar `PredictionResult.test.tsx`:
  reemplazar asserciones de "Interface demonstration only" y "Mock
  response" por los nuevos textos.
  Evidencia: `npm test -- --run` pasa.
- [x] 3.3 [Frontend/UX] Modificar `HomePage.tsx`: eliminar badges
  "Prototype", "Synthetic responses". Mostrar estado real del servicio
  cuando esté disponible.
  Evidencia: `npm run typecheck`.
- [x] 3.4 [Frontend/UX] Eliminar `ProposalNotice.tsx` y su importación en
  el layout. Eliminar badges "Proposal only", "Interface concept" de las
  páginas admin (Dashboard, Training, Models). Conservar indicadores
  factuales como "No connected" o "Not implemented".
  Evidencia: `npm run typecheck`.

## 4. Panel de revisión humana y tip contextual

- [x] 4.1 [Frontend/UX] Crear componente `HumanReviewPanel` como `aside`
  explicativo: "La sugerencia requiere revisión humana. La clasificación,
  derivación y decisión final pertenecen al equipo responsable." Con
  estructura semántica, visible en escritorio a la derecha y apilado en
  móvil.
  Evidencia: `npm run typecheck` y revisión responsive.
- [x] 4.2 [Frontend/UX] Integrar `HumanReviewPanel` en `UserLayout` (no
  dentro de `ClassificationPage`) para que sea persistente durante el
  flujo.
  Evidencia: el panel aparece en los pasos 1-4 de clasificación.
- [x] 4.3 [Frontend/UX] Añadir aviso "Helpful tip" al pie de
  `ClassificationPage` con consejo sobre redacción de narrativa.
  Colapsable con control accesible.
  Evidencia: `npm run typecheck`.

## 5. Verificación y cierre

- [x] 5.1 [Frontend/UX] Ejecutar batería completa:
  ```bash
  cd app/interface
  npm run typecheck && npm run lint && npm test -- --run && npm run build
  ```
  Evidencia posterior a la PR `#66`: `typecheck`, `lint`, `format:check`,
  58 pruebas Vitest y el build PWA finalizan con código 0 después de corregir
  el manejo de indisponibilidad.
- [x] 5.2 [Frontend/UX] Ejecutar comprobaciones del repositorio:
  ```bash
  cd raíz
  python scripts/quality/check_repository.py
  git diff --check
  npm exec -- openspec validate ui-redesign --type change --strict
  ```
  Evidencia: comandos finalizan con código 0.
- [x] 5.3 [Frontend/UX] Sin hacer commit, presentar archivos modificados,
  evidencia de tests, riesgos y decisiones pendientes para revisión
  humana antes de proceder con PR.
- [x] 5.4 [Frontend/UX] Verificar después de integrar que los errores de
  transporte, el modo sin API y el backend degradado no fabrican una
  clasificación. Evidencia: pruebas directas de `ClassificationPage`, smoke
  local con frontend `200`, health `ok` y respuesta real del modelo
  `baseline-lr-C0.1-f8000`; informe agregado
  `reports/validation/claimvox_ui_redesign_review_2026-07-30.md`.
- [x] 5.5 [Frontend/UX] Mantener todos los textos visibles en inglés y
  restaurar `Sign in` cuando no existe sesión para revisar las identidades
  demo user/admin. Evidencia: tests directos de `UserLayout` y búsqueda de
  literales visibles; no añade autenticación ni permisos reales.

## 6. Dashboard local factual

- [x] 6.1 [Frontend] Consumir health y el resumen agregado de feedback con
  la misma base local configurada, contratos estrictos y errores seguros.
  Evidencia: contratos TypeScript y clientes locales compilan sin modificar API.
- [x] 6.2 [Frontend/UX] Sustituir los estados estáticos del Dashboard por
  estados accesibles de configuración, carga, salud, actividad agregada,
  vacío y error, sin cambiar los límites operativos. Evidencia:
  `DashboardPage.tsx` separa health, modelo, feedback local, datos compartidos
  y revisión humana.
- [x] 6.3 [Tests/QA] Cubrir API no configurada, health ok/degraded, error de
  red y resumen vacío/con actividad; comprobar la ausencia de datos o
  afirmaciones prohibidas. Evidencia: 5 pruebas directas y 63 pruebas frontend
  completas superadas.
- [x] 6.4 [Verificación] Ejecutar type-check, lint, format check, pruebas
  afectadas, build, validación OpenSpec, quality gate y `git diff --check`;
  registrar evidencia agregada de PG-16. Evidencia del 30 de julio de 2026:
  type-check, lint, formato, 5 pruebas directas, 63 pruebas frontend y build
  superados; OpenSpec válido, quality gate superado y diff correcto.
- [x] 6.5 [Frontend/UX] Mostrar debajo de las tarjetas una tabla accesible
  con el desglose agregado en el orden recibido y solo los cuatro campos
  aprobados, incluyendo carga, vacío y error recuperable. Evidencia:
  `DashboardPage.tsx` usa una tabla nativa con caption y encabezados.
- [x] 6.6 [Tests/QA] Verificar varias filas, total coherente, estados seguros
  y ausencia de campos prohibidos; repetir la batería frontend y transversal.
  Evidencia: 5 pruebas directas y 63 pruebas frontend superadas; type-check,
  lint, formato, build, OpenSpec, quality gate y diff correctos.
