## Why

El equipo necesita un lugar único para saber quién hace cada trabajo, en qué estado está y qué lo bloquea, sin convertir Jira en una segunda fuente de requisitos ni depender de que Miguel prepare contexto manualmente. La integración debe enlazar Jira, OpenSpec, ramas y Pull Requests mediante identificadores estables y reglas comprensibles.

## Tracking

- Jira exception: `bootstrap`.
- Motivo: este cambio crea el mecanismo que hará obligatoria y verificable la referencia Jira en los cambios posteriores.

## What Changes

- Definir Jira `PG` como sistema de seguimiento operativo del proyecto.
- Mantener OpenSpec y los contratos versionados como fuente de requisitos, decisiones y aceptación.
- Establecer una jerarquía mínima Epic → Historia/Tarea sin duplicar cada checkbox de OpenSpec.
- Incorporar la clave Jira al inicio del arnés, nombres de rama y plantilla de Pull Request.
- Validar localmente el formato y la coherencia de la referencia Jira sin almacenar credenciales.
- Crear un primer Epic del nivel esencial y un backlog reducido solo después de aprobación humana.
- Documentar el flujo en lenguaje corriente para que cada integrante trabaje desde su propio clon.

No se sincronizarán automáticamente estados, comentarios o datos mediante secretos en el repositorio. Jira no sustituirá specs, ADR, evidencias, dailies ni GitHub.

## Capabilities

### New Capabilities

- `jira-work-tracking`: seguimiento operativo enlazado con OpenSpec, el arnés y GitHub mediante claves Jira verificables.

### Modified Capabilities

- `openspec-governance`: exigir que todo cambio nuevo con trabajo planificado identifique su elemento Jira o documente explícitamente una excepción.

## Impact

- `scripts/harness.py`, tests, plantilla de Pull Request y documentación de trabajo.
- OpenSpec, convenciones de rama y futuros tickets del proyecto `PG`.
- Jira Cloud `miguel-redondo.atlassian.net`, proyecto `PG`.
- Sin impacto en API de producto, datos CFPB, modelo o estados del briefing.
- Seguridad: ninguna credencial, token, narrativa ni contenido sensible en Git o paquetes para IA.
