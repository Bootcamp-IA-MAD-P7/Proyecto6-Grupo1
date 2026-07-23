# Catálogo de fuentes para NotebookLM

Este catálogo indica qué documentos pueden alimentar una presentación y con qué frecuencia deben revisarse.

| Fuente | Propósito | Frecuencia | Responsable | Estado |
|---|---|---|---|---|
| `.specify/intent.md` | Propósito, restricciones y principios globales | Cuando cambie la intención | Equipo | Activa |
| `AGENTS.md` | Decisiones vigentes y límites para agentes y equipo | Cuando cambie el contexto operativo | Equipo | Activa |
| `specs/*/` | Specs, planes, tareas y decisiones | Por cambio de alcance | Equipo | Activa |
| `config/cfpb_target_contract.json` | Clases, mappings y límites aplicables al EDA CFPB | Cuando cambie el contrato de datos | Datos / ML | Activa |
| `README.md` | Visión general y acceso al proyecto | Cada hito | Equipo | Activa |
| `CHANGELOG.md` | Evolución por versiones | Cada cambio relevante | Miguel / equipo | Activa |
| `docs/architecture/repository_structure.md` | Arquitectura del repositorio | Cuando cambie la estructura | Miguel | Activa |
| `docs/project_management/delivery_levels.md` | Alcance y puertas de calidad | Cada cambio de alcance | Miguel / equipo | Activa |
| `docs/product/idea_evaluation_template.md` | Reglas y evidencias para comparar ideas | Durante descubrimiento | Equipo | Activa |
| `docs/product/candidates/` | Fichas y evidencias de alternativas consideradas | Durante descubrimiento | Equipo | Activa |
| `docs/project_management/dailies/YYYY-MM-DD.md` | Actividad y bloqueantes | Diaria | Equipo | Activa |
| `docs/project_management/workflow.md` | Método común desde Jira hasta Pull Request | Cuando cambie el proceso | Equipo | Activa |
| `docs/project_management/harness_quickstart.md` | Guía autoservicio del arnés | Cuando cambie el proceso | Miguel / equipo | Activa técnica |
| `ai-specs/` | Roles y procedimientos reutilizables para IA | Cuando cambie el arnés | Miguel / equipo | Activa técnica |
| `docs/design/information_architecture.md` | Usuario, tareas, estados y accesibilidad del flujo | Cuando cambie la experiencia | Producto / UX | Activa |
| `docs/api/openapi.json` | Contrato entre React PWA y futura inferencia | Cuando cambie la API | Aplicación / plataforma | Activa contract-only |
| `docs/security/threat_model.md` | Amenazas y controles del producto | Cuando cambien datos o arquitectura | Seguridad / equipo | Activa |
| `reports/validation/repository_harness_audit_2026-07-23.md` | Evidencia puntual de coherencia documental y estructural | Cierre del arnés | Miguel / arquitectura | Activa técnica |
| `docs/notebooklm/project_facts.md` | Hechos verificados del producto | Diaria o por hito | Miguel / responsables de evidencia | Activa |
| `docs/notebooklm/business_narrative.md` | Historia para audiencia no técnica | Cuando se defina el negocio | Equipo | Activa con límites explícitos |
| `docs/notebooklm/technical_status.md` | Estado técnico consolidado | Diaria o por PR | Miguel / equipo | Activa |
| `reports/metrics/` | Evidencia cuantitativa | Por experimento | ML/QA | Pendiente |
| `reports/figures/` | Gráficos finales | Por experimento | ML/Docs | Pendiente |
| `docs/assets/screenshots/` | Evidencia visual del producto | Por cambio de UI | UX/QA | Pendiente |

## Regla editorial

Una fuente marcada como pendiente o propuesta no puede utilizarse para afirmar que una capacidad ya existe.

## Selección según audiencia

- Cliente o negocio: comenzar por `business_narrative.md`, `project_facts.md`, el brief concreto y evidencia visual o cuantitativa revisada.
- Presentación técnica: añadir `technical_status.md`, contratos, specs relevantes, informes y niveles de entrega.
- Trabajo interno con IA: utilizar `AGENTS.md`, `ai-specs/`, tareas y decisiones; estas fuentes no deben ordenar la narrativa de una presentación para cliente.

El paquete generado reúne fuentes para revisión interna. Antes de subirlo a un notebook orientado a cliente se debe comprobar el brief y excluir fuentes que introduzcan proceso técnico antes del problema, usuario, valor y evidencia.
