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

### Changed

- Las dailies se consolidan en un único documento canónico por fecha dentro de gestión de proyecto; NotebookLM consume esa fuente sin duplicarla.
- El equipo activo pasa a estar formado por José, Abel, Víctor y Miguel tras la baja comunicada de Josué.
- React PWA se confirma como dirección frontend inicial; la evolución nativa queda sujeta a requisitos futuros.
- Las instrucciones de agentes y el workflow reflejan las decisiones actuales y un método independiente de proveedor.

### Fixed
