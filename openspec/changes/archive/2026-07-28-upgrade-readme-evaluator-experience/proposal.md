## Why

El MVP esencial de ClaimVox está verificado y cuenta con evidencia técnica,
pero el README todavía exige recorrer varias secciones para encontrar el
recorrido demostrable, las métricas esenciales, los límites y la evolución
prevista. Una persona evaluadora o cliente debe poder comprender el valor y la
madurez del MVP en pocos minutos, sin convertir el documento en una presentación
ni exagerar el alcance local.

## What Changes

- Reorganizar el README como puerta de entrada ejecutiva y técnica: prueba local
  en cinco minutos, estado verificable, arquitectura actual y evolución, evidencia,
  seguridad, escalabilidad y rutas de consulta.
- Incorporar una tabla ejecutiva de criterios esenciales, métricas reales y sus
  fuentes, diferenciando MVP local de capacidades futuras.
- Mejorar enlaces internos hacia la demo, informes, Jira, OpenSpec, NotebookLM y
  documentación operativa sin duplicar su contenido.
- Revisar únicamente la documentación relacionada cuyo significado cambie y
  registrar la verificación editorial.

## Capabilities

### New Capabilities

- Ninguna.

### Modified Capabilities

- `mvp-presentation-documentation`: el README debe permitir a una audiencia nueva
  evaluar el MVP local desde una ruta breve, verificable y orientada a valor.

## Tracking

- Jira: `PG-10`.

## Impact

- Afecta `README.md`, la documentación de presentación y las fuentes de
  NotebookLM solo cuando requieran referencias nuevas.
- No afecta código de aplicación, APIs, contratos, modelo, métricas, dependencias,
  infraestructura, estados de Jira ni el trabajo de frontend, backend o datos.
- Tracking: refinamiento documental posterior al corte `PG-10`, vinculado al Epic
  `PG-9`; no altera el alcance ni el estado de las historias de entrega.
