## Why

La primera corrección evita el desbordamiento matemático, pero `ENTRADA` continúa demasiado próxima al borde derecho con la tipografía real de GitHub. La etiqueta necesita una holgura visual inequívoca y protegida frente a regresiones.

## What Changes

- Ampliar de forma notable los tres fondos de estado del diagrama principal.
- Mantener sus textos centrados con una regla automatizada más exigente.
- Renderizar y revisar el resultado antes de publicarlo.

No cambian el flujo, los textos, los colores ni el estado del producto.

## Capabilities

### New Capabilities

- Ninguna.

### Modified Capabilities

- `repository-presentation-quality`: aumentar el margen mínimo verificable de las etiquetas del diagrama principal.

## Impact

- Un SVG documental, su quality gate y sus tests existentes.
- Sin impacto en datos, privacidad, producto, API o criterios del briefing.
