## 1. Auditoría editorial

- [x] 1.1 [Arquitectura / documentación] Inventariar las secciones actuales del README, sus enlaces y las fuentes canónicas de estado, métricas y demo. Evidencia: `README.md`, `docs/project_management/delivery_levels.md`, `docs/project_management/essential_delivery_guide.md`, `docs/project_management/mvp_delivery_roadmap.md`, `reports/validation/cfpb_essential_evaluation.md`, `reports/validation/cfpb_baseline_metrics.json`, `reports/validation/claimvox_local_inference_smoke.md`, `docs/architecture/system_blueprint.md` y el tag `v0.1.0-essential-mvp` revisados.
- [x] 1.2 [Documentación] Definir la secuencia de lectura para cliente, evaluador y persona técnica, conservando el alcance local y los límites explícitos. Evidencia: el README abre con prueba segura, continúa con resumen ejecutivo y evidencia, y enlaza después a arquitectura, operación y fuentes canónicas.

## 2. README de evaluación

- [x] 2.1 [Documentación] Añadir una ruta «Prueba ClaimVox en 5 minutos» basada exclusivamente en comandos y contenido sintético ya documentados. Evidencia: sección homónima de `README.md`; el modo sin API se identifica como mock y la inferencia local real remite a la guía canónica.
- [x] 2.2 [Documentación] Incorporar una tabla ejecutiva de estado del MVP y una tabla breve de evidencias esenciales con enlaces a informes canónicos. Evidencia: secciones «Evaluación ejecutiva» y «Evidencia esencial destacada» de `README.md`.
- [x] 2.3 [Documentación] Explicar arquitectura actual, seguridad, privacidad, revisión humana y evolución prevista mediante lectura progresiva y enlaces; no duplicar informes ni prometer despliegue. Evidencia: contraste «Construido ahora / Evolución gobernada» y enlaces al blueprint, seguridad y guía de entrega.
- [x] 2.4 [Documentación] Reordenar enlaces de producto, evaluación, Jira, OpenSpec y NotebookLM para que cada audiencia pueda profundizar sin perder la fuente de verdad. Evidencia: accesos progresivos en las secciones de demostración, evaluación ejecutiva, arquitectura, NotebookLM y próximos hitos.

## 3. Coherencia y verificación

- [x] 3.1 [Documentación] Revisar si `CHANGELOG.md`, fuentes de NotebookLM, catálogo de fuentes y guía de presentación requieren ajustes de significado; modificar solo los afectados. Evidencia: `CHANGELOG.md` recoge el reajuste editorial; el catálogo y las fuentes NotebookLM ya apuntaban al README y a las evidencias canónicas, por lo que no se duplican ni reescriben.
- [x] 3.2 [QA] Ejecutar `git diff --check`, `python scripts/quality/check_repository.py` y `npm exec -- openspec validate --all --strict`; comprobar enlaces Markdown modificados. Evidencia: las tres comprobaciones superadas el 28 de julio de 2026; el paquete NotebookLM se regeneró con `python scripts/documentation/build_notebooklm_pack.py --date 2026-07-28`.
- [ ] 3.3 [Coordinación] Actualizar tareas y evidencias, preparar una PR documental hacia `dev` y mantener el cambio activo hasta revisión humana, archivo y cierre.
