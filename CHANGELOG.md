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
- React PWA con TypeScript y Vite, cliente de inferencia sustituible, mock visible, estados accesibles y shell offline sin caché de API.
- Cinco tests de interacción frontend, lint de accesibilidad, build PWA y ejecución de los 30 tests Python incorporados a CI.

### Changed

- Las dailies se consolidan en un único documento canónico por fecha dentro de gestión de proyecto; NotebookLM consume esa fuente sin duplicarla.
- El equipo activo pasa a estar formado por José, Abel, Víctor y Miguel tras la baja comunicada de Josué.
- React PWA se confirma como dirección frontend inicial; la evolución nativa queda sujeta a requisitos futuros.
- Las instrucciones de agentes y el workflow reflejan las decisiones actuales y un método independiente de proveedor.
- La spec `003` pasa a implementación: `T-006` queda verificada contra mock mientras negocio, backend y modelo continúan bloqueados.
- La propuesta frontend de Abel se reconcilia con la spec `003`: el endurecimiento PWA queda en `T-008` y las ampliaciones de producto pasan a Jira y futuras specs.
- Dependabot incorpora el ecosistema npm de `app/interface/` y la documentación reconoce la base visual y CI frontend ya implementadas.
- Se formalizan las responsabilidades principales: Miguel en arquitectura, José en backend, Abel en frontend/UX y Víctor en datos/EDA; Josué permanece fuera del equipo activo.
- `001/T-004` pasa a estar en curso bajo la responsabilidad de Víctor y `003/T-007` queda asignada a José sin levantar sus bloqueantes.
- README, intent, AGENTS, specs, tareas, arquitectura, daily y fuentes de NotebookLM se sincronizan para el cierre del 22 de julio.
- La narrativa de presentación adopta un enfoque orientado a cliente: problema, experiencia, valor y confianza antes de la explicación técnica.
- El comprobador del repositorio deja de recorrer dependencias y artefactos generados, manteniendo el arnés rápido al incorporar Node.

### Fixed
