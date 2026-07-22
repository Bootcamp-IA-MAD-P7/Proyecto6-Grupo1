# Catálogo de fuentes para NotebookLM

Este catálogo indica qué documentos pueden alimentar una presentación y con qué frecuencia deben revisarse.

| Fuente | Propósito | Frecuencia | Responsable | Estado |
|---|---|---|---|---|
| `.specify/intent.md` | Propósito, restricciones y principios globales | Cuando cambie la intención | Miguel / equipo | Activa |
| `AGENTS.md` | Decisiones vigentes y límites para agentes y equipo | Cuando cambie el contexto operativo | Equipo | Activa |
| `specs/*/` | Specs, planes, tareas y decisiones | Por cambio de alcance | Equipo | Activa |
| `config/cfpb_target_contract.json` | Clases, mappings y límites aplicables al EDA CFPB | Cuando cambie el contrato de datos | Miguel / arquitectura; Víctor / evidencia | Activa |
| `README.md` | Visión general y acceso al proyecto | Cada hito | Equipo | Activa |
| `CHANGELOG.md` | Evolución por versiones | Cada cambio relevante | Miguel / equipo | Activa |
| `docs/architecture/repository_structure.md` | Arquitectura del repositorio | Cuando cambie la estructura | Miguel | Activa |
| `docs/project_management/delivery_levels.md` | Alcance y puertas de calidad | Cada cambio de alcance | Miguel / equipo | Activa |
| `docs/product/idea_evaluation_template.md` | Reglas y evidencias para comparar ideas | Durante descubrimiento | Equipo | Activa |
| `docs/product/candidates/` | Fichas y evidencias de alternativas consideradas | Durante descubrimiento | Equipo | Activa |
| `docs/project_management/dailies/YYYY-MM-DD.md` | Actividad y bloqueantes | Diaria | Equipo | Activa |
| `docs/project_management/workflow.md` | Método común desde Jira hasta Pull Request | Cuando cambie el proceso | Equipo | Activa |
| `docs/design/information_architecture.md` | Usuario, tareas, estados y accesibilidad del flujo | Cuando cambie la experiencia | Abel / equipo | Activa |
| `docs/api/openapi.json` | Contrato entre React PWA y futura inferencia | Cuando cambie la API | Miguel / arquitectura; José / backend | Activa contract-only |
| `app/interface/README.md` | Estado, ejecución y límites de la React PWA | Por cambio de interfaz | Abel | Activa con mock |
| `docs/security/threat_model.md` | Amenazas y controles del producto | Cuando cambien datos o arquitectura | Seguridad / equipo | Activa |
| `docs/notebooklm/project_facts.md` | Hechos verificados del producto | Diaria o por hito | Miguel / responsables de evidencia | Activa |
| `docs/notebooklm/business_narrative.md` | Historia para audiencia no técnica | Cuando cambie la hipótesis o su validación | Equipo | Activa con límites explícitos |
| `docs/notebooklm/technical_status.md` | Estado técnico consolidado | Diaria o por PR | Miguel / equipo | Activa |
| `docs/notebooklm/briefs/` | Narrativa, audiencia y límites de cada presentación | Por presentación | Miguel / equipo | Activa |
| `reports/metrics/` | Evidencia cuantitativa | Por experimento | ML/QA | Pendiente |
| `reports/validation/complaint_routing_pwa.md` | Evidencia de tests, build, accesibilidad y límites del mock | Por cambio de experiencia | Abel / frontend | Activa |
| `reports/figures/` | Gráficos finales | Por experimento | ML/Docs | Pendiente |
| `docs/assets/screenshots/` | Evidencia visual del producto | Por cambio de UI | UX/QA | Pendiente |

## Regla editorial

Una fuente marcada como pendiente o propuesta no puede utilizarse para afirmar que una capacidad ya existe.
