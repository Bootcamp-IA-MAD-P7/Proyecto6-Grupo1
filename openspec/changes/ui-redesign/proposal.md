## Why

ClaimVox ya dispone de una React PWA integrada y verificable con flujo de
clasificación funcional. Sin embargo, la interfaz actual:

- mantiene etiquetas de "prototype", "mock" y "concept" incluso cuando el
  servicio local está disponible;
- separa `UserLayout` y `AdminLayout` con navegación distinta, lo que obliga
  a la persona administradora a cambiar de layout para acceder a funciones
  de revisión;
- no ofrece una guía visual de progreso durante el flujo de clasificación.

Este cambio evoluciona la PWA hacia una experiencia unificada, profesional y
orientada al rol, eliminando la distancia entre la apariencia de prototipo y
el funcionamiento real del servicio local. La propuesta visual explorada en
`claimvox-ux-ui-prototype` sirve de inspiración estructural; este cambio la
convierte en modificaciones reales de la PWA.

## Tracking

- Jira: `PG-16`.
- (Propuesto; no cerrado en Jira.)
- Implementación inicial fusionada en la PR `#66`; la verificación posterior
  detectó y corrigió una regresión de error seguro antes del archivo del cambio.
- Este cambio modifica la PWA integrada; no altera backend, API, modelo,
  contratos, SQLite, servicios, CI/CD ni niveles de entrega.
- Niveles de entrega afectados: ninguno. No verifica ni modifica criterios
  `ESS`, `MED`, `ADV` o `EXP`.

## What Changes

### Unified layout

`UserLayout` y `AdminLayout` se fusionan en un solo layout responsivo. La
barra lateral izquierda filtra los ítems de navegación según el rol:

- **Rol `user`**: Home, Classify, Settings (ThemeToggle).
- **Rol `admin`**: Home, Classify, Dashboard, Training, Models, Settings
  (ThemeToggle).

La cabecera muestra el nombre, rol y botón de cierre de sesión para ambos
roles. Sin sesión, conserva un enlace `Sign in` a la autenticación de
demostración para poder revisar los roles user/admin sin presentarla como
seguridad real.

### 4-step progress flow

`ClassificationPage` se rediseña como un flujo guiado de cuatro pasos con
barra de progreso visible:

1. **Describe** — textarea de narrativa (≤6 líneas), aviso de privacidad,
   dictado opcional.
2. **Review** — resumen del texto ingresado y confirmación antes de clasificar.
3. **Guidance** — resultado de la clasificación con panel derecho explicativo
   de revisión humana.
4. **Next step** — opciones posteriores (nueva clasificación, acciones según
   el rol).

Internamente sigue siendo una sola página con estados; no se crean rutas
separadas.

### Professional labels

Se eliminan las etiquetas "mock response", "interface demonstration only",
"prototype", "concept" y "proposal only" del flujo principal. La UI
distingue:

- **Servicio local disponible**: muestra `Local prediction` con versión,
  confianza y revisión humana.
- **Servicio no disponible**: muestra `Service unavailable` sin fabricar
  un resultado ni llamarlo "mock".

Las páginas de administración (Dashboard, Training, Models) siguen siendo
conceptuales en cuanto a datos operativos, pero se presentan sin la etiqueta
"Proposal only".

### Right guidance panel

Un panel lateral (o sección apilada en móvil) explica de forma persistente
que la sugerencia requiere revisión humana, con iconografía funcional y
diseño profesional.

### Helpful tip

Un aviso contextual al pie con información útil sobre la revisión, sin
iconografía de IA ni recursos externos.

### Settings al pie del sidebar

El `ThemeToggle` se mueve a una sección "Settings" al final de la barra
lateral, accesible para ambos roles.

## Capabilities

### New Capabilities

- `claimvox-ui-redesign`: se añade el comportamiento visual y de interacción
  del nuevo
  layout unificado, flujo de 4 pasos, etiquetas profesionales, panel de
  revisión humana y tip contextual, apoyado sobre la capacidad vigente
  `complaint-routing-interface`.

## Impact

- `app/interface/src/layouts/UserLayout.tsx` — rediseño completo.
- `app/interface/src/layouts/AdminLayout.tsx` — eliminado (absorbido por
  UserLayout).
- `app/interface/src/pages/user/ClassificationPage.tsx` — rediseño a flujo
  4 pasos.
- `app/interface/src/pages/user/HomePage.tsx` — limpieza de etiquetas mock.
- `app/interface/src/components/PredictionResult.tsx` — limpieza de
  etiquetas mock.
- `app/interface/src/components/ProposalNotice.tsx` — eliminado.
- `app/interface/src/layouts/UserLayout.test.tsx` — actualizado.
- `app/interface/src/pages/user/ClassificationPage.test.tsx` — actualizado.
- `app/interface/src/components/PredictionResult.test.tsx` — actualizado.

No se modifican: backend, API, contratos, modelo, SQLite, servicios de
transporte, hooks, providers, PWA service worker, configuración de Vite,
CI/CD, tests de backend o scripts. La revisión posterior actualiza únicamente
la documentación que cambia de significado y su evidencia agregada.

### Dashboard local factual

El Dashboard administrativo sustituye sus estados estáticos por consultas
locales a `GET /api/v1/health` y `GET /api/v1/feedback/summary`, usando la
misma base URL configurada para predicción. Muestra salud del servicio,
disponibilidad factual del baseline y actividad local agregada. Debajo de las
tarjetas presenta el desglose agregado recibido: versión de modelo, clase
sugerida, decisión y conteo.

Los datos operativos compartidos permanecen como `Not connected` y la
revisión humana como `Required`. Esta revisión no incorpora evaluación
conectada, Champion, métricas de modelo, registros individuales,
autenticación, base compartida ni despliegue.
