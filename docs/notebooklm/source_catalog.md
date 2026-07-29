# Catálogo de fuentes para NotebookLM

Este catálogo indica qué documentos pueden alimentar una presentación y con qué frecuencia deben revisarse.

| Fuente | Propósito | Frecuencia | Responsable | Estado |
|---|---|---|---|---|
| `.specify/intent.md` | Propósito, restricciones y principios globales | Cuando cambie la intención | Equipo | Activa |
| `AGENTS.md` | Decisiones vigentes y límites para agentes y equipo | Cuando cambie el contexto operativo | Equipo | Activa |
| `openspec/specs/` | Capacidades vigentes después de archivar cambios | Por cambio de alcance | Equipo | Activa principal |
| `openspec/changes/` | Propuestas, requisitos, diseño y tareas activos | Durante cada cambio | Equipo | Activa técnica |
| `specs/*/` | Expedientes anteriores a OpenSpec | Solo para trabajo heredado | Equipo | Compatibilidad |
| `config/cfpb_target_contract.json` | Clases, mappings y límites aplicables al EDA CFPB | Cuando cambie el contrato de datos | Datos / ML | Activa |
| `README.md` | Visión general y acceso al proyecto | Cada hito | Equipo | Activa |
| `CHANGELOG.md` | Evolución por versiones | Cada cambio relevante | Miguel / equipo | Activa |
| `docs/architecture/repository_structure.md` | Arquitectura del repositorio | Cuando cambie la estructura | Miguel | Activa |
| `docs/project_management/delivery_levels.md` | Alcance y puertas de calidad | Cada cambio de alcance | Miguel / equipo | Activa |
| `docs/product/idea_evaluation_template.md` | Reglas y evidencias para comparar ideas | Durante descubrimiento | Equipo | Activa |
| `docs/product/candidates/` | Fichas y evidencias de alternativas consideradas | Durante descubrimiento | Equipo | Activa |
| `docs/project_management/dailies/YYYY-MM-DD.md` | Actividad y bloqueantes | Diaria | Equipo | Activa |
| `docs/project_management/workflow.md` | Método común desde Jira hasta Pull Request | Cuando cambie el proceso | Equipo | Activa |
| `docs/project_management/jira_workflow.md` | Frontera, backlog y manual operativo de Jira | Cuando cambie el seguimiento | Miguel / equipo | Activa técnica |
| `docs/project_management/harness_quickstart.md` | Guía autoservicio del arnés | Cuando cambie el proceso | Miguel / equipo | Activa técnica |
| `ai-specs/` | Roles y procedimientos reutilizables para IA | Cuando cambie el arnés | Miguel / equipo | Activa técnica |
| `openspec/config.yaml` | Contexto y reglas obligatorias de los cambios | Cuando cambie el gobierno | Miguel / equipo | Activa técnica |
| `docs/design/information_architecture.md` | Usuario, tareas, estados y accesibilidad del flujo | Cuando cambie la experiencia | Producto / UX | Activa |
| `docs/api/openapi.json` | Contrato vigente entre React PWA y servicio de inferencia local; el mock sigue como valor seguro por defecto | Cuando cambie la API | Aplicación / plataforma | Activa técnica |
| `app/interface/README.md` | Uso reproducible y límites del prototipo React PWA ClaimVox | Por cambio de frontend | Abel / frontend | Activa técnica |
| `app/api/README.md` | Ejecución local, límites y contrato del servicio FastAPI | Por cambio de backend | José / backend | Activa técnica |
| `docs/security/threat_model.md` | Amenazas y controles del producto | Cuando cambien datos o arquitectura | Seguridad / equipo | Activa |
| `reports/validation/frontend_foundation_integration.md` | Evidencia automática y manual de la React PWA prototipo | Por hito frontend | Abel / Miguel | Activa técnica |
| `reports/validation/claimvox_state_reconciliation_inventory.md` | Trazabilidad documental de PR #28, estado Jira y límites del prototipo ClaimVox | Por reconciliación de estado | Arquitectura / documentación | Activa técnica |
| `reports/validation/repository_harness_audit_2026-07-23.md` | Evidencia puntual de coherencia documental y estructural | Cierre del arnés | Miguel / arquitectura | Activa técnica |
| `reports/validation/openspec-harness-validation-2026-07-23.md` | Evidencia de implantación real de OpenSpec y el arnés | Cierre de la adopción | Miguel / arquitectura | Activa técnica |
| `reports/validation/repository-final-review-2026-07-23.md` | Evidencia final de presentación, estructura, estados y quality gates | Cierre documental | Miguel / arquitectura | Activa técnica |
| `reports/validation/jira-harness-integration-2026-07-23.md` | Evidencia de backlog, dependencias y arnés Jira | Cierre de la integración | Miguel / arquitectura | Activa técnica |
| `docs/notebooklm/project_facts.md` | Hechos verificados del producto | Diaria o por hito | Miguel / responsables de evidencia | Activa |
| `docs/notebooklm/business_narrative.md` | Historia para audiencia no técnica | Cuando se defina el negocio | Equipo | Activa con límites explícitos |
| `docs/notebooklm/technical_status.md` | Estado técnico consolidado | Diaria o por PR | Miguel / equipo | Activa |
| `docs/assets/diagrams/readme-project-overview.svg` | Flujo de valor y límites del producto | Cuando cambie el flujo | Arquitectura / producto | Activa visual |
| `docs/assets/charts/delivery-status-2026-07-28.svg` | Resumen visual de las 25 puertas; su estado canónico está en `delivery_levels.md` | Cuando cambie un criterio | Miguel / QA | Activa visual |
| `reports/metrics/` | Evidencia cuantitativa | Por experimento | ML/QA | Pendiente |
| `reports/figures/` | Gráficos finales | Por experimento | ML/Docs | Activa técnica |
| `notebooks/01_eda.py` | EDA reproducible del CFPB | Por cambio de datos | Víctor / Datos | Activa técnica |
| `scripts/data/convert_cfpb_to_parquet.py` | Conversión reproducible y filtrado seguro | Por cambio de datos | Víctor / Datos | Activa técnica |
| `reports/validation/cfpb_eda.md` | Evidencia agregada verificable del EDA, visualizaciones pertinentes y continuidad con la política posterior | Por hito de datos o cambio de política | Víctor / Datos | Activa |
| `reports/validation/cfpb_training_dataset.md` | Evidencia agregada del constructor local y diferencia de instantáneas | Por construcción del corpus | Datos / ML | Activa técnica |
| `reports/validation/cfpb_training_dataset_manifest.json` | Recuentos agregados y huellas de fuente/contrato del constructor | Por construcción del corpus | Datos / ML | Activa técnica |
| `config/cfpb_training_policy.json` | Política aprobada de idioma, grupos, split, soporte y evaluación del baseline | Por cambio de preparación | Datos / ML | Activa técnica |
| `reports/validation/cfpb_training_preparation.md` | Evidencia agregada de filtrado de idioma y particiones locales | Por preparación del baseline | Datos / ML | Activa técnica |
| `reports/validation/cfpb_training_preparation_manifest.json` | Huellas, recuentos por clase y límites temporales de la preparación | Por preparación del baseline | Datos / ML | Activa técnica |
| `reports/validation/cfpb_baseline.md` | Configuración y métricas agregadas del baseline, incluyendo validation y test protegido | Tras cambio de baseline | Datos / ML | Activa técnica |
| `reports/validation/cfpb_baseline_metrics.json` | Métricas agregadas y por clase del baseline, sin narrativas | Tras cambio de baseline | Datos / ML | Activa técnica |
| `reports/validation/cfpb_essential_evaluation.md` | Evaluación final agregada sobre validation: matriz de confusión, importancia, errores, límites y artefacto local | Tras evaluación esencial | Datos / ML | Activa técnica |
| `docs/project_management/essential_delivery_guide.md` | Guía canónica Git Bash para mock seguro e inferencia local PWA → FastAPI, con health y límites | Tras cambio del flujo esencial | Equipo | Activa técnica |
| `reports/validation/claimvox_local_runbook_review.md` | Inventario de consistencia entre guía, configuración, cliente HTTP y límites de la demo local | Tras cambio del recorrido local | Arquitectura / documentación | Activa técnica |
| `docs/project_management/mvp_delivery_roadmap.md` | Secuencia propuesta de criterios posteriores, dependencias y evidencias mínimas antes de crear Jira | Al planificar el siguiente ciclo | Equipo | Propuesta de gestión |
| `reports/validation/backend_foundation_real_smoke.md` | Evidencia agregada de entrenamiento local reproducible y smoke del servicio FastAPI; no acredita despliegue ni integración PWA | Por cambio de backend o artefacto | Backend / ML | Activa técnica |
| `reports/validation/claimvox_local_inference_smoke.md` | Evidencia agregada de la integración local PWA→API con entrada sintética, contrato, CORS y revisión humana; no acredita despliegue | Por cambio de integración | Frontend / backend | Activa técnica |
| `reports/validation/mvp_readiness_inventory.md` | Inventario de controles locales, límites de privacidad, prueba sintética y auditoría estructural del MVP | Por cambio transversal de MVP | Arquitectura / seguridad | Activa técnica |
| `docs/presentations/claimvox_mvp_story.md` | Guion breve para explicar problema, demostración, evidencia, límites y evolución a cliente o evaluador | Antes de una presentación | Equipo | Activa de presentación |
| `reports/validation/med_01_comparison.md` | Comparación agregada del baseline con RF, XGBoost y LightGBM; no selecciona un modelo definitivo | Tras comparación ensemble | Víctor / Datos | Activa técnica |
| `reports/validation/med_01_metrics.json` | Métricas agregadas reproducibles de la comparación ensemble, sin narrativas | Tras comparación ensemble | Víctor / Datos | Activa técnica |
| `reports/validation/screenshots/PG-4/` | Evidencia visual sintética del prototipo | Por cambio de UI | UX/QA | Activa técnica |
| `reports/validation/cfpb_quality_gates.md` | Evidencia agregada de puertas locales de datos, modelo y métricas con límites explícitos | Tras cambio de quality gates | QA / arquitectura | Activa técnica |
| `reports/validation/claimvox_feedback_persistence.md` | Evidencia agregada de persistencia local gobernada: contrato minimizado, retención, privacidad y pruebas sintéticas; no acredita endpoint, base compartida ni MLOps | Tras cambio de feedback local | Backend / arquitectura | Activa técnica |
| `reports/validation/claimvox_feedback_operational_flow.md` | Evidencia agregada del registro local explícito y resumen de feedback por versión, clase y decisión; no acredita autenticación, operación compartida, corpus ni reentrenamiento | Tras cambio del flujo local de feedback | Backend / frontend | Activa técnica |
| `reports/validation/claimvox_local_feedback_e2e.md` | Evidencia agregada de predicción local real, registro de feedback minimizado y resumen agregado; no acredita operación compartida, autenticación, despliegue ni reentrenamiento | Tras verificación local extremo a extremo | Backend / QA | Activa técnica |
| `reports/validation/claimvox_local_classification_usability.md` | Evidencia agregada de la revisión del flujo local: fuente API/mock, resultado, revisión humana, límites de alternativas y navegación pública | Tras cambio de UX local | Frontend / UX | Activa técnica |
| `docs/assets/screenshots/` | Evidencia visual general del producto | Por cambio de UI | UX/QA | Pendiente |

## Regla editorial

Una fuente marcada como pendiente o propuesta no puede utilizarse para afirmar que una capacidad ya existe.

Para el estado vigente de entrega prevalece
`docs/project_management/delivery_levels.md`. Las dailies, informes puntuales,
expedientes numerados y cambios OpenSpec archivados se conservan como evidencia
histórica de su fecha y no deben reinterpretarse como estado actual.

## Selección según audiencia

- Cliente o negocio: comenzar por `business_narrative.md`, `project_facts.md`, el brief concreto y evidencia visual o cuantitativa revisada.
- Presentación técnica: añadir `technical_status.md`, contratos, specs relevantes, informes y niveles de entrega.
- Trabajo interno con IA: utilizar `AGENTS.md`, OpenSpec, `ai-specs/`, tareas y decisiones; estas fuentes no deben ordenar la narrativa de una presentación para cliente.

El paquete generado reúne fuentes para revisión interna. Antes de subirlo a un notebook orientado a cliente se debe comprobar el brief y excluir fuentes que introduzcan proceso técnico antes del problema, usuario, valor y evidencia.
