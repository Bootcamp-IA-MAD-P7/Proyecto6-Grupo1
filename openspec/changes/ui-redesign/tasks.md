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
  resumen del texto, botones "Clasificar reclamación" y "Volver". Step 3:
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
  mostrar "El servicio de predicción no está disponible" sin etiquetar
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

- [ ] 5.1 [Frontend/UX] Ejecutar batería completa:
  ```bash
  cd app/interface
  npm run typecheck && npm run lint && npm test -- --run && npm run build
  ```
  Evidencia: los tres comandos finalizan con código 0.
- [ ] 5.2 [Frontend/UX] Ejecutar comprobaciones del repositorio:
  ```bash
  cd raíz
  python scripts/quality/check_repository.py
  git diff --check
  npm exec -- openspec validate ui-redesign --type change --strict
  ```
  Evidencia: comandos finalizan con código 0.
- [ ] 5.3 [Frontend/UX] Sin hacer commit, presentar archivos modificados,
  evidencia de tests, riesgos y decisiones pendientes para revisión
  humana antes de proceder con PR.
