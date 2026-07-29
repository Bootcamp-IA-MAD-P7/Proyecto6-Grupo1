## Why

ClaimVox ya dispone de una interfaz React PWA verificable, pero el equipo quiere
evaluar una evolución de UX/UI con mayor claridad de flujo sin arriesgar la
integración existente ni presentar una propuesta de diseño como producto
operativo. Esta exploración permite comparar una experiencia navegable, recoger
la decisión de frontend/UX y conservar evidencia antes de autorizar cualquier
integración futura.

## Tracking

- Jira: `PG-4`.
- Este cambio toma `PG-4` como antecedente de interfaz; es una exploración de
  diseño y no modifica su estado ni su alcance entregado.
- Niveles de entrega afectados: ninguno. No verifica ni modifica criterios
  `ESS`, `MED`, `ADV` o `EXP`.

## What Changes

- Crear una propuesta visual navegable y aislada para una futura evolución de
  ClaimVox bajo `docs/design/claimvox-ux-ui-prototype/`.
- Definir una jerarquía de navegación, progreso, narrativa, dictado opcional,
  orientación revisable y ayuda contextual inspirada solo en la estructura de
  la referencia aportada.
- Documentar límites visibles entre propuesta visual, mock, predicción local y
  capacidades futuras no implementadas.
- Registrar criterios de accesibilidad, comportamiento responsive, privacidad,
  evidencia visual y decisiones que debe validar la responsabilidad de
  frontend/UX antes de cualquier integración.

No se modifica `app/interface/`, el backend, los contratos, el modelo, la API,
la PWA, dependencias, configuración, Jira ni infraestructura. No se crea una
segunda aplicación de producción, autenticación, persistencia, analítica ni
ninguna funcionalidad operativa nueva.

## Capabilities

### New Capabilities

- `claimvox-ux-ui-prototype`: propuesta visual aislada, accesible y trazable
  para evaluar una futura evolución de la experiencia ClaimVox sin alterar la
  aplicación integrada.

### Modified Capabilities

- Ninguna. La experiencia React PWA vigente no cambia en este alcance.

## Impact

- Documentación y artefactos de diseño bajo `docs/design/`.
- Nueva capacidad OpenSpec y evidencia visual versionable de bajo peso.
- Ningún impacto en código de aplicación, API, contratos, datos, modelo,
  dependencias, CI/CD, seguridad operativa o criterios de entrega.
