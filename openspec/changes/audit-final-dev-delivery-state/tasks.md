## 1. Inventario integrado

- [x] 1.1 [Arquitectura] Fijar el SHA de `origin/dev` e inventariar ramas y Pull Requests fusionadas, abiertas, cerradas y no contenidas. Evidencia: SHA `1366ef202cbabe45a1c53a96d57e6284e690993a`, consultas Git/GitHub y clasificación agregada en `reports/validation/claimvox_final_dev_audit_2026-07-31.md`.
- [x] 1.2 [Seguridad] Auditar archivos pesados, artefactos, secretos y cambios OpenSpec activos/archivados sin imprimir valores ni modificar archivos locales excluidos. Evidencia: quality gate superado para 628 archivos versionados/684 locales, inventario OpenSpec y comprobación de que los tres archivos excluidos continúan sin seguimiento.

## 2. Auditoría funcional y de plataforma

- [x] 2.1 [Backend / ML] Verificar carga del baseline, health, predicción de once clases, errores seguros, CORS y límites con pruebas existentes y payloads sintéticos. Evidencia: 141 tests unitarios y 40 de contrato superados; el modelo local ignorado existe y conserva once clases, sin entrenamiento nuevo.
- [x] 2.2 [Frontend / UX] Verificar clasificación, resultado, revisión humana, feedback, Dashboard, estados accesibles y textos visibles en inglés. Evidencia: type-check, lint, Prettier, 63 tests y build PWA superados.
- [x] 2.3 [Plataforma] Verificar estática y dinámicamente, cuando el entorno lo permita, Docker/Compose y PostgreSQL: imágenes, healthcheck, configuración, esquema, persistencia, mínimo privilegio y reversión. No acreditar cloud. Evidencia: `docker compose config --quiet` y pruebas estáticas superadas; daemon Docker no disponible, por lo que build, PostgreSQL, rollback y cloud quedan explícitamente sin verificar.
- [x] 2.4 [Seguridad] Corregir credenciales o secretos de demostración embebidos, DDL runtime incompatible con mínimo privilegio y smoke de despliegue no bloqueante; añadir pruebas o validaciones directas sin contactar cloud. Evidencia: secretos externos, JWT efímero, Bearer en predicción/feedback, CORS acotado, DDL administrativo, smoke bloqueante y auditorías npm con cero vulnerabilidades.

## 3. Reconciliación de entrega

- [x] 3.1 [Arquitectura] Revisar los 25 criterios `ESS`, `MED`, `ADV` y `EXP` contra evidencia mínima, manteniendo selección, Champion, corpus, cloud y MLOps pendientes salvo prueba suficiente. Resultado: 15 verificados, 6 en curso y 4 no iniciados.
- [x] 3.2 [Documentación] Actualizar `docs/project_management/delivery_levels.md` y fuentes activas que contradigan el estado verificado, enlazando evidencia exacta. Resultado: `ADV-01` a `ADV-03` se reconcilian como “En curso”, sin elevar ningún criterio.

## 4. Documentación y presentación

- [x] 4.1 [Documentación] Reconciliar README, AGENTS, intent, changelog, guías técnicas y de presentación cuyo significado cambie, sin reescribir fuentes históricas. Evidencia: fuentes activas actualizadas y daily factual del 31 de julio.
- [x] 4.2 [NotebookLM] Actualizar hechos, estado técnico y catálogo de fuentes para separar capacidades locales, contenerizadas, compartidas, desplegadas y pendientes. Evidencia: `project_facts.md`, `technical_status.md`, `business_narrative.md` y `source_catalog.md`.
- [x] 4.3 [Documentación] Generar el gráfico activo fechado `2026-07-31` desde los criterios canónicos, conservar gráficos anteriores como históricos y validar SVG/accesibilidad. Evidencia: SVG sincronizado y parseado; revisión visual automatizada no disponible y registrada como límite.
- [x] 4.4 [Arquitectura] Crear `reports/validation/claimvox_final_dev_audit_2026-07-31.md` con SHA, inventarios, comprobaciones, estados, límites y recomendaciones para `PG-11`, `PG-15` y `PG-17`.

## 5. Verificación y cierre para revisión

- [x] 5.1 [QA] Ejecutar harness doctor, compilación y suites Python, quality gates, comprobaciones frontend completas, validación OpenSpec estricta y `git diff --check`; registrar solo resultados reales. Evidencia: doctor/32 OpenSpec, 141 unitarios, 40 contratos, 63 frontend, build, auditorías npm, quality gate, Compose estático y whitespace superados.
- [x] 5.2 [Arquitectura] Revisar que los tres archivos locales excluidos no estén staged ni modificados y entregar comandos mínimos para revisión humana, commit y PR hacia `dev`, sin publicar, archivar ni tocar `main`. Evidencia: `Generated`, `Never` y `reports/validation/cfpb_fast_linear_search.json` continúan sin seguimiento; no se ejecutó publicación.
