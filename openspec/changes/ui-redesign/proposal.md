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
roles.

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

- **Servicio local disponible**: muestra predicción real con versión,
  confianza y revisión humana.
- **Servicio no disponible**: mensaje claro de indisponibilidad sin fabricar
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

### Modified Capabilities

- `complaint-routing-interface`: se modifica la PWA existente con nuevo
  layout unificado, flujo de 4 pasos, etiquetas profesionales, panel de
  revisión humana y tip contextual. La capacidad sigue siendo la misma; su
  especificación se actualiza con los nuevos requisitos.

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
CI/CD, tests de backend, scripts, documentación fuera de `app/interface/`.
