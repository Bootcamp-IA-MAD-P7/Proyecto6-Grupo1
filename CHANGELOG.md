# Changelog

## Unreleased

### Added

- Estructura inicial del repositorio preparada para una evolución incremental hasta nivel experto.
- Flujo SPEC-first, plantillas de Pull Request e Issues y estrategia de tags/releases.
- Daily por fecha con un apartado para cada integrante activo del equipo.
- Fuentes curadas y generador de paquetes diarios para NotebookLM.
- Blueprint por capas, baseline de seguridad, disciplina UX y estrategia de pruebas.
- Workflows iniciales de calidad del repositorio y validación de tags.
- Dependabot y configuración de notas de release.
- Ruleset activo para proteger `dev` mediante Pull Requests, CI obligatorio e historial lineal.
- Intent global del proyecto con propósito, restricciones, decisiones abiertas y principios de entrega.
- Spec `000-problem-discovery` con plan, tareas y decisiones para evaluar ideas de forma trazable.
- Propuesta versionada de puertas críticas, matriz y gobierno para comparar ideas y datasets.
- Evaluación comparable de las candidatas CFPB y RealWaste, con evidencias, riesgos, puntuaciones y análisis cualitativo.
- Selección unánime y condicionada de la clasificación de reclamaciones CFPB como dirección del proyecto.
- Arnés acotado de viabilidad CFPB con contrato versionado, probe API, inspección temporal sin persistir narrativas, informes agregados y tests unitarios.
- Evidencia preliminar de 2.306.723 narrativas, catorce etiquetas observadas, desbalanceo, drift de taxonomía y duplicados.
- Spec `001-cfpb-target-contract`, contrato ejecutable de once clases y tests para coordinar EDA y modelado sin leakage.
- Spec `002-team-ai-workflow` y generador seguro de contexto por spec y tarea para herramientas de IA externas.
- Spec `003-complaint-routing-experience`, arquitectura de información y OpenAPI contract-only para desarrollar la React PWA mediante mocks.
<<<<<<< HEAD
- React PWA con TypeScript y Vite, cliente de inferencia sustituible, mock visible, estados accesibles y shell offline sin caché de API.
- Cinco tests de interacción frontend, lint de accesibilidad, build PWA y ejecución de los 30 tests Python incorporados a CI.
=======
- Spec `004-agentic-harness`, cuatro roles, cuatro procedimientos reutilizables y una entrada única para generar contexto seguro por tarea.
- Contrato verificable de niveles de entrega con criterios `ESS`, `MED`, `ADV` y `EXP`.
- Guía autoservicio para que cada integrante utilice el arnés desde su propio clon y con cualquier IA compatible con Markdown.
- Suites unitarias y de contrato del arnés integradas en `repository-quality`.
- OpenSpec `1.6.0` instalado localmente con configuración de proyecto, lockfile y adaptadores oficiales para Codex, GitHub Copilot, Claude Code, Cursor y Gemini CLI.
- Flujo reproducible para propuesta, requisitos, diseño, tareas, validación y archivo de cambios.
- Integración del arnés con el estado e instrucciones reales de OpenSpec, diagnóstico local y compatibilidad temporal con las tareas numeradas ya asignadas.
- Validación estricta de OpenSpec, auditoría npm y diagnóstico del arnés incorporados al quality gate.
- Comprobaciones de regresión para tablas de entrega, SVG documentales accesibles, sincronización de estados y placeholders permitidos.
- Capacidad OpenSpec `repository-presentation-quality` y auditoría final de presentación y estructura.
- Proyecto Jira `PG` integrado con un Epic del nivel esencial, seis elementos de
  entrega y ocho relaciones de bloqueo verificadas.
- Manual operativo de Jira y referencias `PG-N` en OpenSpec, arnés, ramas y
  Pull Requests, sin credenciales en el repositorio.
>>>>>>> 5558ae2204151767a53be0e45102bd04a3b6da83

### Changed

- Las dailies se consolidan en un único documento canónico por fecha dentro de gestión de proyecto; NotebookLM consume esa fuente sin duplicarla.
- El equipo activo pasa a estar formado por José, Abel, Víctor y Miguel tras la baja comunicada de Josué.
- React PWA se confirma como dirección frontend inicial; la evolución nativa queda sujeta a requisitos futuros.
<<<<<<< HEAD
- Las instrucciones de agentes y el workflow reflejan las decisiones actuales y un método independiente de proveedor.
- La spec `003` pasa a implementación: `T-006` queda verificada contra mock mientras negocio, backend y modelo continúan bloqueados.
- La propuesta frontend de Abel se reconcilia con la spec `003`: el endurecimiento PWA queda en `T-008` y las ampliaciones de producto pasan a Jira y futuras specs.
- Dependabot incorpora el ecosistema npm de `app/interface/` y la documentación reconoce la base visual y CI frontend ya implementadas.
- Se formalizan las responsabilidades principales: Miguel en arquitectura, José en backend, Abel en frontend/UX y Víctor en datos/EDA; Josué permanece fuera del equipo activo.
- `001/T-004` pasa a estar en curso bajo la responsabilidad de Víctor y `003/T-007` queda asignada a José sin levantar sus bloqueantes.
- README, intent, AGENTS, specs, tareas, arquitectura, daily y fuentes de NotebookLM se sincronizan para el cierre del 22 de julio.
- La narrativa de presentación adopta un enfoque orientado a cliente: problema, experiencia, valor y confianza antes de la explicación técnica.
- El comprobador del repositorio deja de recorrer dependencias y artefactos generados, manteniendo el arnés rápido al incorporar Node.
=======
- Las instrucciones de agentes y el workflow reflejan las decisiones actuales y un método OpenSpec independiente del proveedor de IA.
- La estructura adopta creación incremental: conserva contratos en los README y elimina subcarpetas vacías para capacidades todavía no implementadas.
- El estado activo comprende el EDA de Víctor, el uso operativo de OpenSpec y el inicio desde cero de la React PWA por Abel mediante `003/T-006`.
- OpenSpec gobierna los cambios nuevos; `specs/` conserva únicamente los expedientes anteriores y las tareas ya asignadas.
- El piloto con Víctor deja de ser una condición de implantación y pasa a ser una oportunidad de feedback durante su trabajo real.
- La propuesta frontend experimental de la PR `#14` se cierra sin mergear para que Abel defina e implemente el frontend desde una base limpia.
- Jira pasa a conservar responsable, estado y bloqueos; OpenSpec conserva
  requisitos y decisiones, y GitHub conserva implementación y evidencia.
>>>>>>> 5558ae2204151767a53be0e45102bd04a3b6da83

### Fixed

- Responsables, estados de specs y tareas, recuentos de tests y documentación de aplicación, producto y scripts sincronizados con el estado real.
- README y niveles de entrega describen el nivel esencial como `En curso` por el EDA activo.
- La primera iteración del arnés deja de presentarse como la solución definitiva; el expediente `004` queda sustituido por la capacidad OpenSpec versionada.
- La normalización de rutas OpenSpec distingue correctamente rutas Windows y POSIX sin permitir fuentes externas al repositorio.
- Las etiquetas del diagrama principal utilizan fondos de 120 unidades, margen interior amplio y centrado consistente después de su validación visual.
- Los veinticinco IDs del briefing permanecen completos en tablas estrechas y se contrastan automáticamente con su estado canónico.
