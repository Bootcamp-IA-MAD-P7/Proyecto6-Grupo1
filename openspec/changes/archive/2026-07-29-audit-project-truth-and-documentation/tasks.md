## 1. Auditoría y verdad integrada

- [x] 1.1 [Arquitectura / QA] Inventariar rama, cambios OpenSpec, contratos, aplicación, ML, pruebas, CI y evidencias sin leer datasets ni incorporar ramas no fusionadas. Evidencia: `reports/validation/project_truth_audit_2026-07-30.md` y rama `docs/PG-9-audit-project-truth`; no se abrieron datasets, narrativas ni artefactos.
- [x] 1.2 [QA] Contrastar los 25 criterios y las métricas publicadas contra `delivery_levels.md` y los informes JSON versionados. Evidencia: el informe de auditoría registra 15 verificados, 3 en curso y 7 no iniciados; métricas del baseline contrastadas con `cfpb_baseline_metrics.json`.

## 2. Correcciones reproducibles

- [x] 2.1 [QA / documentación] Extender `scripts/quality/check_repository.py` y sus pruebas para validar IDs, conteos y gráfico activo contra los niveles de entrega. Verificación: `python -m unittest tests.unit.test_repository_quality -v`, 6 pruebas superadas.
- [x] 2.2 [Documentación] Generar el gráfico accesible del corte vigente con 15 criterios verificados, 3 en curso y 7 no iniciados; actualizar el catálogo de activos. Evidencia: `docs/assets/charts/delivery-status-2026-07-30.svg`; validación SVG incluida en las 6 pruebas de repositorio.
- [x] 2.3 [Equipo] Corregir otras incoherencias claras halladas durante la auditoría mediante cambios mínimos y pruebas directamente afectadas. Evidencia: se corrigieron tres incompatibilidades TypeScript del flujo de feedback, un test dependiente de la configuración local y seis incumplimientos de Prettier; `typecheck`, lint, formato, 52 tests y build del frontend superados.

## 3. Documentación profesional

- [x] 3.1 [Documentación] Reestructurar README como entrada técnica profesional: problema, alcance, arquitectura, resultados, ejecución local, evidencia, estado y límites, sin lenguaje publicitario. Evidencia: `README.md` distingue los dos cortes de evaluación, documenta 25 criterios y enlaza fuentes reproducibles.
- [x] 3.2 [Arquitectura / seguridad] Reconciliar AGENTS, intención, contexto OpenSpec, arquitectura, API y seguridad con inferencia y feedback locales, manteniendo pendientes operación compartida, autenticación, Docker, base de datos, despliegue y MLOps. Evidencia: documentos canónicos y README de aplicación reconciliados con persistencia SQLite local minimizada.
- [x] 3.3 [Documentación] Actualizar niveles de entrega, roadmap, guion de presentación, fuentes NotebookLM y changelog sin alterar evidencias históricas. Evidencia: corte global corregido a 15 verificados, 3 en curso y 7 no iniciados; gráfico activo del 30 de julio y fuentes NotebookLM actualizadas.
- [x] 3.4 [Coordinación] Crear la daily factual del corte a partir de Git y verificaciones reales, separando áreas sin inventar autoría. Evidencia: `docs/project_management/dailies/2026-07-29.md` distingue actividad comprobable de ausencia de commits individuales atribuibles.

## 4. Verificación y cierre

- [x] 4.1 [QA] Ejecutar tests focalizados de backend, frontend, ML y documentación, además de `git diff --check`. Evidencia: suites Python unitarias, de contrato e integración superadas; frontend con 52 tests, typecheck, lint, formato y build superados.
- [x] 4.2 [QA] Ejecutar `python scripts/quality/check_repository.py`, `python scripts/harness.py doctor` y validación estricta del cambio. Evidencia: 579 archivos versionados y 639 locales comprobados; arnés correcto; 30 elementos OpenSpec válidos en modo estricto.
- [x] 4.3 [Coordinación] Revisar el diff final, registrar riesgos y proponer commit, Pull Request y una etiqueta no engañosa; no crear ni publicar nada sin revisión humana. Evidencia: riesgos y propuesta `v0.2.0-local-governed-workflow` registrados en el informe; la etiqueta queda bloqueada hasta reconciliar versiones `0.1.0`/`0.2.0` y obtener revisión humana.
