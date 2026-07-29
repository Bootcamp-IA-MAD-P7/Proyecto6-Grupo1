## Why

ClaimVox dispone de un baseline evaluado y de pruebas parciales, pero las
comprobaciones de datos, artefacto y métricas todavía no forman puertas de
calidad reproducibles. Esta carencia impide verificar de forma consistente los
criterios avanzados `ADV-04`, `ADV-05` y `ADV-06` antes de ampliar la operación
del producto.

## What Changes

- Añadir puertas de calidad locales y reproducibles para los contratos de datos
  de entrenamiento: esquema permitido, once clases canónicas, valores nulos,
  duplicados y ausencia de fuga entre grupos y particiones.
- Añadir puertas de calidad para el modelo local: carga segura, preprocesamiento,
  forma de salida, clases permitidas, probabilidades e inferencia controlada.
- Añadir puertas de métricas que consuman evidencia agregada versionada y
  verifiquen umbrales aprobados, rendimiento por clase y gap train-validación
  sin volver a entrenar modelos.
- Usar exclusivamente fixtures sintéticos en las pruebas y mantener fuera de
  Git los corpus, narrativas CFPB, artefactos de modelo y resultados locales.
- Registrar evidencia proporcionada para `ADV-04`, `ADV-05` y `ADV-06` sin
  alterar las métricas existentes ni declarar un modelo Champion.

## Capabilities

### New Capabilities

- `claimvox-quality-gates`: puertas de calidad versionadas para integridad de
  datos, comportamiento del modelo y métricas mínimas antes de promover cambios
  locales de ClaimVox.

### Modified Capabilities

- Ninguna.

## Impact

- Jira: `PG-12`.
- Afecta a contratos existentes de dataset y baseline, pruebas unitarias,
  scripts locales de verificación y evidencia agregada.
- No modifica datos reales, modelos entrenados, inferencia de producto,
  frontend, backend, dependencias, infraestructura ni despliegue.
- La seguridad y privacidad se refuerzan al impedir que los checks requieran
  narrativas CFPB o artefactos locales no versionables.

## Tracking

- Jira: `PG-12`.
- Criterios de entrega: `ADV-04`, `ADV-05` y `ADV-06`.
