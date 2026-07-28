## Why

ClaimVox ha verificado el nivel esencial en ejecución local, pero la evidencia,
la experiencia de evaluación y el repositorio aún no comunican esa madurez con
la claridad, seguridad y trazabilidad necesarias para una demo profesional. El
proyecto necesita consolidar su README, preparar una presentación orientada a
cliente, endurecer los límites operativos locales y convertir el trabajo
pendiente en un backlog Jira único y gobernado, sin presentar el MVP como un
servicio desplegado.

## What Changes

- Elevar el README a guía principal de producto, demo, arquitectura, evidencia,
  seguridad, escalabilidad y límites reales del MVP; comprobar el resto de
  documentación y actualizar solo aquello cuyo significado haya cambiado.
- Definir e implementar observabilidad técnica mínima y segura: sin narrativas,
  audio, identidades, direcciones IP persistidas ni credenciales; los eventos
  deben limitarse a salud del servicio, latencia agregada, resultado técnico,
  versión de modelo y revisión humana.
- Endurecer la superficie local de predicción con límites de entrada,
  cabeceras de seguridad y rate limiting configurable, acompañados de pruebas
  y mensajes de error seguros. No se expondrá el servicio a Internet.
- Auditar encapsulamiento, dependencias y puntos de rendimiento de la PWA, API
  y capa de modelo; aplicar solo mejoras pequeñas, comprobables y compatibles
  con los contratos existentes.
- Establecer una política de versionado y crear el primer tag de entrega cuando
  la evidencia y la revisión humana confirmen el corte `v0.1.0-essential-mvp`.
- Preparar un único mapa Jira para los criterios no verificados de los niveles
  medio, avanzado y experto, con dependencias y evidencias mínimas, sin
  fragmentar el trabajo por el nombre de cada nivel.
- Actualizar las fuentes y el guion de NotebookLM para una presentación que
  empiece por el problema y el valor para la persona usuaria, y que explique
  después evidencia, arquitectura, seguridad, escalabilidad y límites.

## Capabilities

### New Capabilities

- `privacy-safe-operational-observability`: eventos técnicos mínimos, sin
  contenido de reclamaciones ni identidad de usuario, con reglas de retención y
  consulta local explícitas.
- `mvp-release-governance`: corte versionado, checklist de release y backlog
  Jira trazable para el trabajo posterior al nivel esencial.
- `mvp-presentation-documentation`: documentación principal y fuentes de
  presentación que comuniquen valor, evidencia y límites sin lenguaje técnico
  prematuro ni afirmaciones de producción.

### Modified Capabilities

- `prediction-service`: endurecer los requisitos de protección de entrada,
  cabeceras, frecuencia y observabilidad segura del servicio local.
- `complaint-routing-interface`: comunicar de forma accesible la disponibilidad
  local, la privacidad y los fallos del servicio sin conservar la narrativa.
- `project-state-documentation`: exigir una fuente canónica de estado de
  entrega, release y criterios pendientes que no contradiga README, Jira ni
  NotebookLM.

## Impact

- Afecta a `README.md`, documentación de seguridad, fuentes NotebookLM,
  artefactos OpenSpec, evidencias y dailies.
- Puede afectar a `app/api/`, `app/interface/`, pruebas Python/TypeScript,
  configuración local y workflows de calidad, sin introducir base de datos,
  autenticación, despliegue, datos pesados ni servicios externos.
- Contribuye directamente a `MED-04`, `ADV-04`, `ADV-05` y `ADV-06`, y prepara
  el resto del briefing sin declararlo cumplido antes de tener evidencia.

## Tracking

- Jira: `PG-10`.

`PG-10` pertenece al Epic `PG-9` y coordina este cambio transversal. Las
historias posteriores `PG-11` a `PG-17` se documentan en
`docs/project_management/mvp_delivery_roadmap.md`; ninguna cambia por sí misma
el estado de un criterio de entrega.
