# Expedientes de compatibilidad

Estas carpetas documentan trabajo creado antes de implantar OpenSpec. Se mantienen para no romper las tareas ya asignadas ni perder decisiones históricas.

| ID | Expediente | Estado | Uso permitido |
|---|---|---|---|
| `000` | [`problem-discovery`](000-problem-discovery/spec.md) | En curso | Cerrar las puertas de descubrimiento heredadas |
| `001` | [`cfpb-target-contract`](001-cfpb-target-contract/spec.md) | En curso | Terminar el EDA asignado a Víctor y aplicar el contrato de target |
| `002` | [`team-ai-workflow`](002-team-ai-workflow/spec.md) | Cerrado | Referencia histórica del flujo independiente de proveedor |
| `003` | [`complaint-routing-experience`](003-complaint-routing-experience/spec.md) | En curso | Terminar la tarea frontend asignada a Abel |
| `004` | [`agentic-harness`](004-agentic-harness/spec.md) | Sustituido | Evidencia de la primera iteración; OpenSpec gobierna la implantación definitiva |

## Regla desde la adopción

- No crear nuevas carpetas `NNN-nombre`.
- Crear los cambios nuevos en `openspec/changes/`.
- Archivar los cambios completados para actualizar `openspec/specs/`.
- Adaptar mediante OpenSpec cualquier entrega heredada que cambie alcance, contratos o decisiones.

La configuración vigente está en [`openspec/config.yaml`](../openspec/config.yaml) y el manual en [`docs/project_management/harness_quickstart.md`](../docs/project_management/harness_quickstart.md).
