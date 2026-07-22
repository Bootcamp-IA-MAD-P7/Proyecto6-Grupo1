# Tareas: Flujo de trabajo del equipo con IA

- Spec: [`spec.md`](spec.md)
- Plan: [`plan.md`](plan.md)

## T-001 Alinear el contexto vigente

- Estado: `[x]`
- Responsable: `Documentación / QA`
- Requisitos cubiertos: `R-001, R-002, R-009, AC-006`
- Trabajo: actualizar instrucciones, intent y arquitectura con decisiones confirmadas y abiertas.
- Evidencia obtenida: `AGENTS.md`, `.specify/intent.md` y el blueprint distinguen decisiones confirmadas y abiertas.

## T-002 Documentar el flujo operativo

- Estado: `[x]`
- Responsable: `Equipo / QA`
- Dependencias: `T-001`
- Requisitos cubiertos: `R-008, AC-004, AC-005`
- Trabajo: explicar inicio, prompts, responsabilidades, verificación y cierre.
- Evidencia obtenida: `docs/project_management/workflow.md` contiene los dos modos de uso, prompts, responsabilidades y cierre.

## T-003 Implementar el generador de handoff

- Estado: `[x]`
- Responsable: `Plataforma / documentación`
- Dependencias: `T-001`
- Requisitos cubiertos: `R-003 a R-007, AC-001 a AC-003`
- Trabajo: construir el paquete desde fuentes versionadas y rechazar entradas inseguras.
- Evidencia obtenida: `scripts/documentation/build_ai_handoff.py` valida spec, tarea, seguimiento Git, ruta, extensión y tamaño.

## T-004 Verificar el arnés

- Estado: `[x]`
- Responsable: `QA`
- Dependencias: `T-002, T-003`
- Requisitos cubiertos: `todos`
- Trabajo: ejecutar tests, generar un paquete real y pasar los checks del repositorio.
- Evidencia obtenida: 19 tests superados; paquete `001-cfpb-target-contract-T-004.md` generado correctamente y `repository-quality` superado.

## T-005 Sincronizar la documentación viva

- Estado: `[x]`
- Responsable: `Documentación / QA`
- Dependencias: `T-004`
- Requisitos cubiertos: `R-002, R-008, R-009`
- Trabajo: actualizar README, scripts, NotebookLM, daily, changelog y catálogo de specs.
- Evidencia obtenida: README, scripts, NotebookLM, daily, changelog, equipo y catálogo de specs sincronizados.

## Checklist de cierre

- [x] Las cinco tareas están verificadas.
- [x] El paquete de ejemplo se genera fuera de Git.
- [x] No se incluye información sensible.
- [x] El flujo puede utilizarse con cualquier IA.
- [x] La documentación coincide con el estado real.
