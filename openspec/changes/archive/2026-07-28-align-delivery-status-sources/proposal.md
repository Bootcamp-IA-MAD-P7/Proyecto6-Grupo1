## Why

El gráfico de estado del briefing contiene el recuento vigente —incluido
`MED-01` como verificado—, pero conserva un nombre de archivo fechado el 23 de
julio mientras su contenido indica el 28 de julio. README, catálogo NotebookLM
y guion de presentación no apuntan de forma uniforme a esa fuente. Además, una
persona nueva puede confundir expedientes históricos con documentación de estado
actual.

La corrección debe hacer visible una sola fuente canónica de estado sin borrar
ni reescribir decisiones, informes, dailies o cambios archivados que conservan
trazabilidad histórica.

## What Changes

- Renombrar el recurso visual de estado con la fecha real de su corte y alinear
  todas sus referencias activas.
- Verificar que el gráfico, `delivery_levels.md` y el resumen del README
  representan el mismo recuento: 11 criterios verificados, 2 en curso y 12 no
  iniciados; nivel medio 1 de 5 verificado y 1 en curso.
- Declarar de forma breve y accesible qué documento es canónico para el estado
  vigente y qué rutas se conservan exclusivamente como historial.
- Actualizar solo las fuentes activas de NotebookLM y presentación afectadas,
  sin reproducir el estado en lugares nuevos.

## Capabilities

### New Capabilities

- Ninguna.

### Modified Capabilities

- `project-state-documentation`: la documentación debe diferenciar de forma
  explícita la fuente canónica de estado vigente de los expedientes históricos
  y mantener sincronizados sus resúmenes visuales activos.

## Tracking

- Jira: `PG-9`.

## Impact

- Afecta exclusivamente documentación y recursos visuales: el gráfico de
  entrega, README, catálogo de fuentes NotebookLM, guía de recursos y guion de
  presentación si aún enlaza el nombre anterior.
- Afecta el resumen del roadmap posterior al MVP, pero no modifica el estado,
  alcance ni asignación de ninguna historia Jira.
- No afecta código, React PWA, backend, datos, modelo, métricas, contratos,
  seguridad, dependencias, infraestructura o despliegue.
- No introduce narrativas CFPB, datos sensibles ni nuevas capacidades de
  producto.
