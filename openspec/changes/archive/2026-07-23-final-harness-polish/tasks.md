## 1. Presentación documental

- [x] 1.1 Miguel / arquitectura: centrar las etiquetas del diagrama principal, igualar sus fondos y conservar título, descripción y `viewBox`. Evidencia: render visual y parser XML correctos.
- [x] 1.2 Miguel / arquitectura: hacer no separables los veinticinco IDs visibles del briefing sin cambiar su nomenclatura ni estado. Evidencia: comprobación automatizada del README.

## 2. Quality gates

- [x] 2.1 Miguel / arquitectura: validar SVG accesibles y placeholders permitidos desde `scripts/quality/check_repository.py`. Evidencia: `python scripts/quality/check_repository.py`.
- [x] 2.2 Miguel / QA: añadir tests de regresión para IDs, SVG y `.gitkeep`. Evidencia: `python -m unittest tests.unit.test_repository_quality -v`.

## 3. Auditoría y documentación

- [x] 3.1 Miguel / arquitectura: revisar estructura, enlaces, documentación viva, OpenSpec, Git y estados del briefing sin acceder a narrativas CFPB. Evidencia: `reports/validation/repository-final-review-2026-07-23.md`.
- [x] 3.2 Miguel / documentación: actualizar changelog, daily y fuentes NotebookLM afectadas sin duplicar información. Evidencia: diff revisado.

## 4. Verificación y cierre

- [x] 4.1 Miguel / QA: ejecutar `npm audit --audit-level=high`, `python scripts/harness.py doctor`, `npm run openspec:validate`, suites unitarias y de contrato, compilación Python, quality check y `git diff --check`.
- [x] 4.2 Miguel / arquitectura: obtener aprobación humana después de revisar el diff para autorizar el archivo OpenSpec, el commit, la publicación y la preparación de la Pull Request. Evidencia: aprobación explícita del 23 de julio de 2026.
