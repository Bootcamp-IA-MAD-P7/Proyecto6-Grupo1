## 1. Inventario y recorrido canónico

- [x] 1.1 [Arquitectura / documentación] Contrastar los comandos, rutas, puertos, variables y artefacto por defecto con la configuración y el código actuales. Evidencia: `reports/validation/claimvox_local_runbook_review.md` enlaza `app/api/config.py`, cliente HTTP y manuales afectados.
- [x] 1.2 [Documentación] Redactar en `docs/project_management/essential_delivery_guide.md` un recorrido Git Bash de dos terminales para mock e inferencia local, con health, resultado esperado y recuperación sencilla de PWA.

## 2. Alineación de fuentes

- [x] 2.1 [Documentación] Actualizar README y manuales de frontend/backend para enlazar al recorrido canónico, retirar contradicciones de shell y no duplicar instrucciones.
- [x] 2.2 [Documentación] Revisar `AGENTS.md`, changelog, daily y fuentes de NotebookLM; modificar solo las fuentes cuyo significado cambie y registrar los límites locales reales. Evidencia: `AGENTS.md`, `project_facts.md` y `business_narrative.md` permanecen válidos y no se modifican; changelog, daily, estado técnico y catálogo se actualizan.

## 3. Verificación y cierre

- [x] 3.1 [Verificación] Comprobar enlaces y consistencia documental sin ejecutar entrenamiento ni incorporar datos locales. Verificación superada: `python scripts/quality/check_repository.py`, `git diff --check` y `npm exec -- openspec validate improve-local-claimvox-runbook --type change --strict`.
- [x] 3.2 [Documentación] Registrar el resultado de la revisión en una evidencia versionada y preparar el cambio para revisión humana, sin commit, push, PR ni archive. Evidencia: `reports/validation/claimvox_local_runbook_review.md`; paquete local de NotebookLM regenerado el 28 de julio de 2026.
