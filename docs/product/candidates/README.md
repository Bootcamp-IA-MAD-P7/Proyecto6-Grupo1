# Candidatas de producto

Esta carpeta conserva las propuestas consideradas durante `000-problem-discovery`. Registrar una candidata no significa seleccionarla.

## Estados

- `incompleta`: faltan campos obligatorios;
- `en evaluación`: se están recopilando evidencias;
- `viable condicional`: no incumple una puerta, pero mantiene validaciones pendientes;
- `viable`: supera las puertas y dispone de evidencia mínima;
- `bloqueada`: no puede avanzar sin resolver una condición crítica;
- `descartada`: no cumple los mínimos o el equipo decide no continuar;
- `seleccionada`: existe una decisión del equipo registrada en la spec;
- `seleccionada con validaciones obligatorias`: el equipo ha elegido la dirección, pero la implementación espera a que se resuelvan sus puertas críticas;
- `no seleccionada`: la alternativa se conserva con sus evidencias y puede recuperarse si cambia la decisión.

## Candidatas registradas

| ID | Candidata | Estado |
|---|---|---|
| CAND-001 | [Clasificación y enrutamiento de reclamaciones financieras](CAND-001-cfpb-complaint-routing.md) | Seleccionada con validaciones obligatorias |
| CAND-002 | [Clasificación visual de residuos](CAND-002-realwaste-classification.md) | No seleccionada; alternativa conservada |

La [comparación de la ronda](comparison-2026-07-22.md) utiliza la versión vigente de [`idea_evaluation_template.md`](../idea_evaluation_template.md) y registra la decisión unánime del equipo.
