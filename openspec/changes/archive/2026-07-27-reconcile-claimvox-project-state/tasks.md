## 1. Inventario y contexto operativo

- [x] 1.1 [Arquitectura / documentación] Confirmar el alcance integrado de la PR #28, el cambio archivado `integrate-frontend-foundation`, el estado Jira confirmado de `PG-2` y los límites vigentes de `PG-3`, `PG-4` y `PG-5`. Evidencia: `reports/validation/claimvox_state_reconciliation_inventory.md`; sin modificar Jira.
- [x] 1.2 [Arquitectura / documentación] Actualizar `AGENTS.md`, `docs/project_management/team.md` y `docs/project_management/jira_workflow.md` para eliminar referencias operativas obsoletas y reflejar responsables, hitos y bloqueos reales. Verificación: no atribuyen `PG-2/T-004` como trabajo activo ni presentan el baseline o backend como implementados.
- [x] 1.3 [Arquitectura / documentación] Revisar `docs/project_management/workflow.md`, `docs/project_management/harness_quickstart.md` y los expedientes heredados afectados; actualizar solo las referencias cuyo significado operativo haya cambiado. Evidencia: `harness_quickstart.md` y `specs/003-complaint-routing-experience/tasks.md` actualizados; los enlaces del workflow conservan validez.

## 2. Estado del producto e interfaz

- [x] 2.1 [Frontend / documentación] Actualizar `README.md` para identificar ClaimVox como el prototipo React PWA integrado, enlazar la PR #28 y conservar el límite explícito de que `ESS-04` no está verificado sin inferencia real. Verificación: no se introducen métricas ni capacidades no existentes.
- [x] 2.2 [Frontend / documentación] Revisar `app/interface/README.md`, `specs/003-complaint-routing-experience/` y `openspec/specs/complaint-routing-interface/`; actualizar únicamente la documentación que necesite reflejar identidad visible, tema y madurez del prototipo. Evidencia: el contrato y las rutas no se renombran ni se presentan como servicios operativos.
- [x] 2.3 [Arquitectura / documentación] Actualizar el changelog con una entrada concisa y trazable de la PR #28 y de esta reconciliación; registrar que no corresponde crear tag o release. Verificación: no se duplica historial ni se altera autoría de Abel.

## 3. Daily y fuentes de NotebookLM

- [x] 3.1 [Equipo / documentación] Completar `docs/project_management/dailies/2026-07-27.md` con apartados de Miguel, Víctor, Abel y José, separando contribución completada, coordinación, responsabilidad vigente, preparación y bloqueos. Verificación: no se inventan tareas, evidencias ni autorías.
- [x] 3.2 [NotebookLM / documentación] Actualizar `docs/notebooklm/project_facts.md`, `technical_status.md`, `business_narrative.md` y `source_catalog.md` solo donde la integración ClaimVox, el estado de datos o la trazabilidad cambien su significado. Verificación: la narrativa para cliente comienza por problema, valor, revisión humana y límites; no por proceso interno.
- [x] 3.3 [NotebookLM / documentación] Regenerar el paquete de NotebookLM para `2026-07-27` y revisar que no contiene narrativas CFPB reales, datos brutos, secretos ni afirmaciones de modelo, backend, despliegue o MLOps. Evidencia: `exports/notebooklm/2026-07-27-notebooklm-pack.md` generado desde fuentes versionadas; no se añade al control de versiones.

## 4. Validación y preparación de revisión

- [x] 4.1 [QA documental] Ejecutar `python scripts/quality/check_repository.py`, `git diff --check` y `npm exec -- openspec validate reconcile-claimvox-project-state --type change --strict`; registrar los resultados reales en las evidencias o tareas correspondientes. Resultado: quality gate superado para 329 archivos versionados y 362 locales; sin errores de whitespace; cambio OpenSpec válido.
- [x] 4.2 [QA documental] Revisar enlaces Markdown, referencias a Jira/OpenSpec/PR y coherencia de los estados de entrega. Evidencia: el README, la daily, el changelog, el arnés y NotebookLM usan el mismo estado integrado; búsqueda focalizada sin referencias operativas obsoletas a `PG-2` como trabajo activo o a `T-006` como pendiente.
- [x] 4.3 [Arquitectura / coordinación] Preparar la Pull Request hacia `dev` con la plantilla completada, referencia a `PG-4`, PR #28 y el cambio OpenSpec. Evidencia: `exports/pr-bodies/reconcile-claimvox-project-state.md`. No crear tag, archive, commit, push, Pull Request ni merge sin revisión humana.
