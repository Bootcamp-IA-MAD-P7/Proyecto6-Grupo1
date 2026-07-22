# Specs

Cada funcionalidad, hito o cambio relevante que necesite un contrato compartido dispone de una carpeta numerada.

## Specs actuales

| ID | Spec | Estado | Propósito |
|---|---|---|---|
| `000` | [`problem-discovery`](000-problem-discovery/spec.md) | Active | Validar las puertas de datos y cerrar la selección condicionada |
| `001` | [`cfpb-target-contract`](001-cfpb-target-contract/spec.md) | In progress | Fijar clases, elegibilidad y límites comunes para EDA y modelado |
| `002` | [`team-ai-workflow`](002-team-ai-workflow/spec.md) | Closed | Unificar el trabajo humano-IA sin imponer una herramienta |
| `003` | [`complaint-routing-experience`](003-complaint-routing-experience/spec.md) | In progress | Validar la React PWA mock y preparar futura inferencia |

La spec `001` permite que el EDA avance en paralelo con un contrato común. La spec `002`, ya cerrada, convierte el método en un flujo reutilizable. La spec `003` ya dispone de frontend contra mock y permanece abierta por la validación de negocio y la integración real. La spec `000` continúa activa hasta cerrar privacidad, evidencia de usuario y ratificación de la evaluación; todavía no existe capacidad predictiva real.
