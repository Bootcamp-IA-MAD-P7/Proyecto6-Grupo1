## Context

ClaimVox tiene una React PWA integrada con dos layouts separados
(`UserLayout`, `AdminLayout`), etiquetas de prototipo en toda la interfaz y
un flujo de clasificación de una sola vista sin indicación de progreso. La
propuesta visual explorada en `docs/design/claimvox-ux-ui-prototype/`
validó una composición alternativa con navegación lateral, pasos y panel de
revisión. Este cambio implementa esa evolución directamente sobre la PWA
real.

El servicio local de predicción y feedback ya existe y funciona. La
autenticación sigue siendo mock; no existe despliegue, base compartida ni
MLOps.

## Goals / Non-Goals

**Goals:**

- Layout único que muestre navegación distinta según `user.role`.
- Flujo de clasificación con barra de progreso de 4 pasos (Describe,
  Review, Guidance, Next step).
- Eliminación de etiquetas "mock", "prototype", "concept", "proposal only"
  del flujo principal.
- Panel lateral de revisión humana persistente.
- Aviso contextual "Helpful tip" al pie.
- `ThemeToggle` movido a sección Settings al pie del sidebar.
- Cabecera unificada con nombre, rol y botón de cierre de sesión.

**Non-Goals:**

- Modificar backend, API, contratos TypeScript, modelo, SQLite, servicios
  de transporte o predicción.
- Implementar autenticación real, persistencia de usuarios, despliegue
  cloud, MLOps, Champion/Challenger.
- Añadir iconografía de IA, recursos externos, librerías de UI nuevas o
  dependencias adicionales.
- Cambiar el nombre de rutas, el contrato de predicción o el
  funcionamiento del service worker PWA.

## Decisions

### 1. Layout único con filtrado por rol

Se elimina `AdminLayout.tsx`. `UserLayout.tsx` se convierte en el único
layout. Los ítems de navegación se definen en un array que incluye
`requiredRole`, y se filtran con `hasRole()`.

```tsx
const navItems = [
  { to: '/', label: 'Home', icon: Home },
  { to: '/classify', label: 'Classify', icon: FileText },
  { to: '/admin', label: 'Dashboard', icon: LayoutDashboard, requiredRole: 'admin' },
  { to: '/admin/training', label: 'Training', icon: Cpu, requiredRole: 'admin' },
  { to: '/admin/models', label: 'Models', icon: Box, requiredRole: 'admin' },
]
```

**Alternativa considerada:** mantener layouts separados y alternar con un
layout wrapper. Se descarta porque la cabecera unificada, el Settings en
sidebar y la barra de progreso serían difíciles de compartir entre dos
layouts sin duplicación.

### 2. Flujo 4 pasos como una sola página con estados

`ClassificationPage` mantiene su estructura de un solo componente pero
organiza el contenido en 4 secciones que se muestran según un estado
`step: 1 | 2 | 3 | 4`. La barra de progreso es un componente puramente
visual que refleja `step`.

```tsx
const [step, setStep] = useState<1 | 2 | 3 | 4>(1)
```

- **Step 1 (Describe)**: textarea, dictado, botón "Revisar texto".
- **Step 2 (Review)**: resumen del texto, botones "Clasificar reclamación"
  y "Volver".
- **Step 3 (Guidance)**: `PredictionResult` adaptado, panel de revisión.
- **Step 4 (Next step)**: opciones "Nueva clasificación", "Ir al inicio".

**Alternativa considerada:** rutas independientes (`/classify/describe`,
etc.). Se descarta porque añade complejidad de enrutamiento, posible
pérdida de estado narrativa al navegar y fragmentación de tests.

### 3. Eliminación progresiva de etiquetas mock

No se elimina el modo mock del cliente de predicción; ese es un mecanismo
de fallback interno. Lo que cambia es la presentación al usuario:

- El cliente mock sigue existiendo como `MockPredictionClient`.
- El `PredictionResult` deja de etiquetar como "Mock response" cuando el
  origen es mock. En su lugar muestra "Servicio no disponible" con texto
  claro.
- El `Badge` de "Mock responses" debajo del formulario se elimina.
- El `Badge` de "Public prototype" en `UserLayout` se elimina.
- `ProposalNotice.tsx` se elimina del layout.
- Las páginas admin pierden `Badge variant="mock"` pero conservan
  indicadores factuales ("No connected", "No data", "Not implemented").

**Riesgo:** sin etiqueta "mock", una persona sin backend configurado
podría pensar que la app no funciona. Se mitiga con mensajes explícitos
de indisponibilidad.

### 4. Panel de revisión humana como `aside` en el layout

El panel de revisión humana se implementa como un componente
`HumanReviewPanel` que se renderiza en el layout (no dentro de
`ClassificationPage`) para que sea persistente durante el flujo. En
escritorio aparece a la derecha; en móvil debajo del contenido.

### 5. Sin nuevas dependencias

Todos los cambios usan componentes ya existentes en
`src/components/ui/` y `lucide-react`. No se añaden librerías de
progreso, paneles laterales ni tooltips externos.

## Risks / Trade-offs

- [Eliminar etiquetas mock puede confundir cuando no hay backend] → Se
  muestra "Servicio no disponible" con texto claro, no se finge una
  respuesta ni se oculta el error.
- [Unificar layouts puede romper las rutas admin protegidas] → El
  `ProtectedRoute` en `App.tsx` se mantiene; el layout solo oculta ítems
  de navegación, no es el guardia de seguridad.
- [El flujo de 4 pasos alarga la interacción] → Se mantiene la opción de
  "Nueva clasificación" directa desde el paso 4 y se evita fricción
  innecesaria.
- [Los tests existentes asumen etiquetas "mock"] → Las tareas incluyen
  actualizar tests antes de marcar como completadas.
- [Textarea de 6 líneas puede ser poco para narrativas largas] → El
  textarea tiene desplazamiento interno; el límite es visual, no de
  caracteres.

## Migration Plan

1. Rediseñar `UserLayout.tsx`: sidebar unificada, cabecera con rol,
   Settings al pie, barra de progreso.
2. Eliminar `AdminLayout.tsx` y `ProposalNotice.tsx`.
3. Rediseñar `ClassificationPage.tsx`: flujo 4 pasos, textarea 6 líneas,
   panel derecho, tip inferior.
4. Actualizar `PredictionResult.tsx` y `HomePage.tsx`: eliminar etiquetas
   mock/prototype.
5. Actualizar `App.tsx` para usar solo `UserLayout`.
6. Actualizar tests y verificar typecheck/lint/build.

Para revertir: restaurar los archivos originales desde `git checkout` y
revertir el cambio OpenSpec.

## Open Questions

- ¿Debe la barra de progreso ser un componente extraído o va inline en
  `UserLayout`? → Decisión: componente `StepProgress` separado.
- ¿"Revisar texto" en step 1 o se fusiona con guidance? → Decisión: step 1
  (Describe) con botón "Revisar texto", step 2 (Review) muestra el texto
  y permite clasificar.
- Textos definitivos en español para todos los labels: deben validarse con
  Abel antes del PR.
