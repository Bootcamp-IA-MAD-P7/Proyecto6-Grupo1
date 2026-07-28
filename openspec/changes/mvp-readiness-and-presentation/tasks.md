## 1. Inventario y decisión operativa

- [x] 1.1 [Arquitectura / seguridad] Inventariar rutas, configuración, logging, almacenamiento, dependencias y límites actuales de API y PWA; registrar evidencia sin narrativas ni datos locales. Evidencia: `reports/validation/mvp_readiness_inventory.md` revisa `app/api/`, `app/interface/`, `docs/security/` y pruebas existentes; no se ejecutaron inferencias ni se trataron datos CFPB.
- [x] 1.2 [Coordinación] Crear o enlazar el elemento Jira operativo de este cambio y el mapa único de criterios pendientes, con responsable, dependencia, OpenSpec y evidencia mínima; no modificar estados de criterios sin evidencia. Evidencia: `PG-9` agrupa el roadmap, `PG-10` rastrea este cambio y `PG-11` a `PG-17` conservan dependencias y evidencias mínimas en `docs/project_management/mvp_delivery_roadmap.md`.
- [x] 1.3 [Seguridad] Aprobar el límite de tamaño y frecuencia locales, y confirmar que observabilidad significa eventos técnicos sin identidad ni contenido. Decisión aprobada: narrativa de hasta 5.000 caracteres y 20 predicciones por minuto por cliente local temporal; eventos técnicos sin identidad ni contenido. Evidencia: `design.md`.

## 2. Controles locales y observabilidad segura

- [x] 2.1 [Backend] Implementar validación de tamaño y rate limiting en memoria configurable, con respuestas contractuales `429` y errores seguros. Evidencia: `app/api/config.py`, `app/api/security.py`, `app/api/routes/predictions.py`, contrato actualizado y `tests/unit/test_api_local_controls.py`.
- [x] 2.2 [Backend] Añadir cabeceras de seguridad apropiadas para API local y comprobar que CORS mantiene orígenes explícitos, sin comodines ni credenciales. Evidencia: `app/api/main.py` y `tests/contract/test_backend_cors.py`.
- [x] 2.3 [Backend] Implementar eventos técnicos estructurados sin narrativa, identidad, IP persistida, alternativas ni confianza individual. Evidencia: `app/api/observability.py` y prueba de campos permitidos y ausencias prohibidas en `tests/unit/test_api_local_controls.py`.
- [x] 2.4 [Frontend] Comunicar de forma accesible los estados de límite, indisponibilidad y privacidad sin persistir la narrativa. Evidencia: `ClassificationPage` muestra contador y límite de 5.000 caracteres, conserva alertas accesibles de límite, indisponibilidad y privacidad; pruebas de interfaz actualizadas.

## 3. Calidad estructural y rendimiento proporcional

- [x] 3.1 [Arquitectura] Revisar encapsulamiento de rutas, servicio, predictores, configuración y cliente HTTP; documentar los hallazgos y seleccionar solo refactors de bajo riesgo con beneficio demostrable. Evidencia: auditoría en `reports/validation/mvp_readiness_inventory.md`.
- [x] 3.2 [Backend / frontend] Aplicar los refactors aprobados sin cambiar OpenAPI, contrato de once clases, revisión humana ni modo mock seguro. Evidencia: controles aislados en `app/api/security.py` y `app/api/observability.py`; contrato, tests y build conservados.
- [x] 3.3 [QA] Ejecutar una prueba local de recorrido real con narrativa sintética, artefacto local y configuración explícita; registrar latencia agregada, modo de predictor y límites sin datos sensibles. Resultado: salud `200`/`ok`, predicción `200` real, revisión humana obligatoria, sin eco de entrada y recorrido agregado de `9 ms`; evidencia en `reports/validation/mvp_readiness_inventory.md`.

## 4. Documentación, presentación y release

- [x] 4.1 [Documentación] Reescribir `README.md` como guía principal de MVP: problema, demo local, arquitectura, evidencia, seguridad, escalabilidad, límites, repositorio y rutas de trabajo. Evidencia: `README.md` incorpora recorrido demostrable, límites, arquitectura actual/prevista y tabla de madurez.
- [x] 4.2 [Documentación] Revisar `AGENTS.md`, OpenSpec, changelog, niveles de entrega, seguridad, dailies y fuentes NotebookLM; actualizar únicamente los documentos cuyo significado cambie. Evidencia: contratos API, seguridad, blueprint, daily, changelog e inventario se reconcilian con el servicio local y sus controles.
- [x] 4.3 [Producto] Actualizar `business_narrative.md`, `project_facts.md`, `technical_status.md` y el catálogo NotebookLM con un guion de cliente: problema, valor, demostración, evidencia, arquitectura, seguridad, escalabilidad y límites. Evidencia: fuentes NotebookLM y `docs/presentations/claimvox_mvp_story.md` actualizados sin datos CFPB reales.
- [x] 4.4 [Coordinación] Regenerar el paquete NotebookLM y preparar una guía de presentación con referencias a figuras, métricas agregadas y demostración local; no incluir narrativas CFPB reales. Evidencia: `docs/presentations/claimvox_mvp_story.md` y `exports/notebooklm/2026-07-28-notebooklm-pack.md` generado; el paquete contiene el guion y no incorpora datos brutos.
- [ ] 4.5 [Release] Tras PR fusionada y revisión humana, crear y verificar el tag anotado `v0.1.0-essential-mvp` en `dev`; documentar que es un corte local, no una release desplegada.

## 5. Verificación y cierre

- [x] 5.1 [QA] Ejecutar las pruebas Python/contrato afectadas, pruebas y build de frontend, quality gate, `git diff --check` y OpenSpec estricto; registrar resultados reales. Evidencia: 40 pruebas Python dirigidas, 16 pruebas Vitest, lint y build PWA superados; `python scripts/quality/check_repository.py`, `git diff --check` y `npm exec -- openspec validate --all --strict` superados el 28 de julio de 2026.
- [ ] 5.2 [Coordinación] Actualizar tareas, decisiones, evidencias y Jira con enlaces reales; abrir la Pull Request hacia `dev` con riesgos y reversión. No hacer merge ni tag sin revisión humana.
