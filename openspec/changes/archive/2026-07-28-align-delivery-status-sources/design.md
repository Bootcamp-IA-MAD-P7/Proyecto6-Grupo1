## Context

`docs/project_management/delivery_levels.md` ya es el contrato canónico de los
25 criterios. El SVG mostrado desde el README contiene sus cifras vigentes,
pero su nombre de archivo y algunos enlaces activos no coinciden con la fecha
de corte declarada dentro del propio recurso. La coexistencia de OpenSpec
archivado, expedientes numerados, dailies e informes es deliberada y protege la
trazabilidad, pero requiere una frontera editorial visible.

Personas afectadas: equipo, evaluadores, clientes y NotebookLM. Ninguna de ellas
debe deducir el estado actual de un archivo histórico ni de una fecha de nombre
incoherente.

## Goals / Non-Goals

**Goals:**

- Mantener un único recurso visual activo, fechado con su corte real y enlazado
  desde todos los documentos activos que lo utilizan.
- Hacer explícita la jerarquía: `delivery_levels.md` es el estado vigente; el
  gráfico y README lo resumen; los expedientes archivados y dailies preservan
  contexto histórico.
- Validar el recuento contra la tabla canónica sin reabrir criterios ni alterar
  sus evidencias.

**Non-Goals:**

- Cambiar el estado de criterios, métricas, Jira, modelo, datos o aplicación.
- Renombrar, editar o eliminar documentación histórica.
- Añadir un segundo registro de estado, automatización de métricas o una nueva
  fuente de verdad.

## Decisions

### Un único gráfico activo y fechado

El recurso se moverá, no se copiará, a una ruta cuyo nombre incorpore la fecha
real del corte. README, catálogo NotebookLM, guía de recursos y guion de
presentación usarán esa ruta. Se evita conservar dos gráficos activos con
posibles lecturas distintas.

Se descarta mantener el nombre anterior por compatibilidad: las referencias se
pueden localizar de forma exhaustiva y el nombre fechado incorrectamente reduce
la confianza del evaluador.

### Jerarquía editorial en lugar de reescritura histórica

La norma se añade a la capacidad vigente de documentación de estado. Debe
identificar `delivery_levels.md` como fuente canónica y explicar que cambios
OpenSpec archivados, `specs/` de compatibilidad, informes puntuales y dailies
conservan la fotografía de su fecha. Solo las fuentes activas se actualizan.

Se descarta homogeneizar todos los documentos: alteraría evidencias de decisiones
y pruebas realizadas con un estado anterior.

### Verificación proporcional y reproducible

La revisión compara el gráfico con la tabla canónica, busca referencias al
nombre antiguo, comprueba formato y ejecuta los quality gates documentales. No
requiere entrenar, descargar datos ni ejecutar la aplicación.

## Risks / Trade-offs

- [Una referencia activa conserva el nombre antiguo] → búsqueda global antes de
  cerrar y comprobación de enlaces del quality gate.
- [Un lector interpreta un informe histórico como estado vigente] → nota breve
  de jerarquía en las fuentes activas, sin esconder el historial.
- [El conteo cambia mientras se revisa] → `delivery_levels.md` prevalece; se
  actualiza el gráfico en otro cambio si cambia la evidencia.

## Migration Plan

1. Mover el SVG al nombre fechado correcto y actualizar referencias activas.
2. Añadir la regla canónica/histórica en documentación y delta OpenSpec.
3. Ejecutar comprobaciones y regenerar el paquete NotebookLM local.
4. Revertir el commit si se detecta una referencia no migrada; no hay migración
   de datos ni de código.

## Open Questions

- Ninguna para esta corrección: el recuento canónico actual ya está en
  `delivery_levels.md`.
