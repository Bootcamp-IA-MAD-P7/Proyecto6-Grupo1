## Why

ClaimVox ya dispone de un recorrido local con mock seguro y otro con inferencia
local real, pero la documentación mezcla sintaxis de PowerShell y Git Bash,
duplica pasos y no ofrece una comprobación breve para distinguir ambos modos.
Esto dificulta la demo, la incorporación de una persona nueva y la revisión del
MVP, aunque no implica un fallo del modelo ni un despliegue pendiente.

## Tracking

- Jira: `PG-10`.

## What Changes

- Crear un runbook único y breve para arrancar ClaimVox en Windows con Git Bash:
  modo mock seguro, modo de inferencia local y comprobaciones de salud.
- Alinear README, guías de frontend/backend y guía esencial con las rutas,
  variables, puertos y nombre de artefacto que el código usa realmente.
- Explicar de forma proporcional cómo evitar una caché PWA anterior, sin
  convertir esa situación de desarrollo en una capacidad de producto.
- Revisar CHANGELOG, fuentes de NotebookLM y daily del 28 de julio únicamente
  si su significado cambia tras la revisión documental.
- Mantener explícito que el recorrido es local, no desplegado, sin autenticación,
  persistencia, datos CFPB reales en la interfaz ni decisión automática.

## Capabilities

### New Capabilities

- `local-claimvox-runbook`: recorrido documentado y verificable para ejecutar
  la demo mock o la inferencia local real de ClaimVox sin exponer datos sensibles.

### Modified Capabilities

- `mvp-presentation-documentation`: el README debe dirigir a una guía local
  inequívoca y distinguir el modo mock del servicio local real.

## Impact

- Documentación afectada: `README.md`, guías de proyecto, frontend y backend,
  fuentes de NotebookLM, CHANGELOG y daily si procede.
- No cambia React, FastAPI, el contrato API, el artefacto, dependencias,
  infraestructura, Jira ni los criterios de entrega.
- Seguimiento: `PG-10` conserva el cierre transversal; este cambio no altera
  estados de Jira ni el alcance de producto.
