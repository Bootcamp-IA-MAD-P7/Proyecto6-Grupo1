## Context

El README usa tablas Markdown nativas y SVG versionados. GitHub calcula el ancho de cada columna según el espacio disponible y puede partir un identificador por el guion, aunque el contenido sea correcto. El diagrama principal también contenía una etiqueta alineada mediante coordenadas manuales y ajustada exactamente al borde de su fondo.

La revisión debe conservar la compatibilidad con GitHub, VS Code y navegadores, sin JavaScript, HTML complejo, estilos que GitHub pueda eliminar ni nuevas dependencias.

## Goals / Non-Goals

**Goals:**

- mantener juntos los identificadores de los niveles de entrega;
- centrar las etiquetas del diagrama dentro de fondos con dimensiones consistentes;
- convertir las convenciones visuales y estructurales comprobables en quality gates;
- cerrar con una evidencia reproducible de la revisión completa;
- conservar como fuente canónica el estado real del briefing.

**Non-Goals:**

- rediseñar la identidad visual;
- sustituir las tablas Markdown por componentes HTML;
- cambiar requisitos, estados o evidencias del briefing;
- implementar producto, ML, backend, frontend, despliegue o MLOps;
- añadir un renderizador gráfico al proyecto.

## Decisions

### Identificadores con guion no separable

Los IDs visibles usarán el carácter Unicode `U+2011` en el README. Mantiene el aspecto `ESS‑01`, evita el salto de línea y funciona en Markdown sin depender de estilos.

Alternativas descartadas:

- ancho HTML o CSS: GitHub filtra o ignora estilos y empeora la portabilidad;
- tabla HTML completa: añade ruido y dificulta el mantenimiento;
- eliminar el guion: rompe la nomenclatura canónica;
- espacios no separables alrededor del guion: altera visualmente el ID.

Los documentos contractuales conservan el guion ASCII dentro de código, enlaces y referencias técnicas.

### SVG accesible y verificable sin dependencia nueva

Los SVG documentales se analizarán con `xml.etree.ElementTree`, incluido en Python. Cada activo debe ser XML válido, declarar `role="img"`, `viewBox`, `<title>` y `<desc>`. El diagrama principal mantendrá las etiquetas de estado centradas y con fondos consistentes.

La comprobación automatizada cubre estructura y accesibilidad básica. El render visual seguirá siendo una evidencia humana proporcional cuando cambie la geometría.

### Placeholders limitados a datos

Los únicos `.gitkeep` permitidos son las cuatro etapas documentadas en `data/`: `raw`, `interim`, `processed` y `external`. Las capacidades futuras no se representan mediante árboles vacíos.

### Auditoría sin cambiar estados

La revisión comparará README, niveles de entrega, OpenSpec, dailies, changelog, estructura, tests y estado Git. Un hallazgo pendiente se documentará; no se convertirá en capacidad implementada ni en criterio verificado.

## Risks / Trade-offs

- El guion no separable puede pasar desapercibido al copiar un ID. → Las referencias técnicas y comandos conservan ASCII; el quality gate solo lo exige en las tablas visuales del README.
- Un parser XML no detecta todos los desbordamientos visuales. → Se conserva una revisión renderizada del activo cuando cambia su geometría.
- Las reglas visuales específicas pueden volverse rígidas. → Se comprueban propiedades funcionales mínimas, no colores ni coordenadas completas.
- La auditoría puede confundir pendientes legítimos con errores. → Los estados `No iniciado`, `En curso` y las decisiones abiertas se consideran información válida.

## Migration Plan

1. Actualizar los IDs visibles y el SVG principal.
2. Añadir comprobaciones y tests.
3. Ejecutar suites, validación OpenSpec, auditoría npm y revisión de Git.
4. Registrar evidencia, changelog y daily.
5. Validar y archivar el cambio antes de preparar la Pull Request.

Rollback: revertir este cambio restaura el render anterior sin afectar contratos, datos ni producto.

## Security, Testing and Documentation

- No se leen ni incorporan narrativas CFPB.
- No se añaden secretos, datos ni dependencias.
- La revisión incluye `npm audit`, tests unitarios y de contrato, OpenSpec estricto, compilación Python, enlaces y whitespace.
- Se actualizan únicamente README, changelog, daily, evidencia y fuentes NotebookLM cuyo estado cambia por esta auditoría.

## Open Questions

Ninguna bloqueante.
