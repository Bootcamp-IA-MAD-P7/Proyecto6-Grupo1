# Expedientes de compatibilidad

<<<<<<< HEAD
Cada funcionalidad, hito o cambio relevante que necesite un contrato compartido dispone de una carpeta numerada.
=======
Estas carpetas documentan trabajo creado antes de implantar OpenSpec. Se mantienen para no romper las tareas ya asignadas ni perder decisiones históricas.
>>>>>>> 5558ae2204151767a53be0e45102bd04a3b6da83

| ID | Expediente | Estado | Uso permitido |
|---|---|---|---|
<<<<<<< HEAD
| `000` | [`problem-discovery`](000-problem-discovery/spec.md) | Active | Validar las puertas de datos y cerrar la selección condicionada |
| `001` | [`cfpb-target-contract`](001-cfpb-target-contract/spec.md) | In progress | Fijar clases, elegibilidad y límites comunes para EDA y modelado |
| `002` | [`team-ai-workflow`](002-team-ai-workflow/spec.md) | Closed | Unificar el trabajo humano-IA sin imponer una herramienta |
| `003` | [`complaint-routing-experience`](003-complaint-routing-experience/spec.md) | In progress | Validar la React PWA mock y preparar futura inferencia |

La spec `001` permite que el EDA avance en paralelo con un contrato común. La spec `002`, ya cerrada, convierte el método en un flujo reutilizable. La spec `003` ya dispone de frontend contra mock y permanece abierta por la validación de negocio y la integración real. La spec `000` continúa activa hasta cerrar privacidad, evidencia de usuario y ratificación de la evaluación; todavía no existe capacidad predictiva real.

## Trabajo activo y responsables

| Trabajo | Responsable principal | Estado |
|---|---|---|
| Arquitectura, coherencia documental y gobierno SDD | Miguel | En curso transversal |
| `001/T-004`: análisis del CSV y EDA | Víctor | En curso |
| `003/T-008`: endurecimiento y validación de la PWA mock | Abel | En curso en la PR `#14` |
| `003/T-007`: futura integración backend | José | Asignada, con implementación real bloqueada |

Josué ya no forma parte del equipo. Las personas de respaldo por área siguen pendientes de acordar. Jira comenzará a utilizarse el 23 de julio de 2026 para seguimiento operativo; estas specs y sus decisiones continúan siendo la fuente de verdad del alcance.
=======
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
>>>>>>> 5558ae2204151767a53be0e45102bd04a3b6da83
