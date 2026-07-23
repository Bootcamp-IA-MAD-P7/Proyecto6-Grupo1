## Context

El fondo actual mide 96 unidades. Aunque el texto está centrado, ciertas métricas tipográficas dejan un margen visual insuficiente.

## Goals / Non-Goals

**Goals:**

- ofrecer una separación claramente visible entre texto y borde;
- aplicar el mismo ancho a las tres etiquetas;
- mantener el diagrama equilibrado dentro de cada panel.

**Non-Goals:**

- rediseñar el diagrama o su tipografía;
- cambiar contenido o estado del proyecto.

## Decisions

- Los fondos pasan a 120 unidades y continúan centrados respecto al texto.
- El quality gate exige ese mínimo para evitar una regresión a 96 unidades.
- Se conserva la fuente de 13 px para no alterar el resto de textos `small`.

## Risks / Trade-offs

- Un fondo mayor ocupa más espacio horizontal. → Cada panel dispone de anchura suficiente y conserva 78 unidades libres.
- Las fuentes varían entre sistemas. → La holgura aumenta de forma deliberada y el resultado se revisa mediante render real.

## Migration Plan

Actualizar SVG, test y quality gate; renderizar; validar; revertir el cambio si altera el equilibrio del panel.

## Open Questions

Ninguna.
