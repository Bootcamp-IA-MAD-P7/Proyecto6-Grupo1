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
- React PWA de `PG-4` incorporada selectivamente a su rama de integración desde
  el trabajo de Abel, con formulario público, dictado, respuesta sintética
  revisable, contrato TypeScript, instalación y shell offline.
- Evidencia reproducible del frontend con typecheck, lint, formato, 31 tests,
  build PWA, auditoría sin vulnerabilidades y revisión manual de accesibilidad,
  responsive, dictado, privacidad, instalación y actualización.
- Manual operativo del frontend y capturas sintéticas verificadas en móvil,
  tablet y escritorio.
- EDA reproducible de Víctor incorporado mediante la PR `#24`, con conversión
  segura a Parquet, notebook Jupytext, cuatro figuras agregadas e informe de
  clases, temporalidad, duplicados, longitud e idioma.
- Integración frontend de Abel fusionada mediante la PR `#25`; la PWA sigue
  usando respuestas sintéticas y no acredita inferencia real.
- Constructor local contractual para `T-005` / `PG-2`, con rutas explícitas,
  soporte seguro de ZIP, filtros, aliases, exclusiones, huella de narrativa,
  exclusión de conflictos y manifiesto agregado sin textos CFPB.
- Seis pruebas sintéticas del constructor y evidencia agregada de una ejecución
  local de 1.998.570 filas, conservando las decisiones de `T-006` abiertas.
- Política versionada de preparación para `PG-2` / `T-006`: huellas de fuente y contrato, inglés para el baseline inicial, grupos de duplicados aislados, split temporal 70/15/15, mínimo de 100 filas por clase en validation y test, macro F1 y pesos balanceados.
- Particiones locales reproducibles para 1.961.073 filas en inglés, con manifiesto agregado, evidencia de soporte de las once clases y pruebas sintéticas de idioma, huellas, grupos y orden temporal.

### Changed

- El prototipo React PWA integrado adopta la identidad visible ClaimVox mediante la PR #28, con preferencias de tema claro, oscuro y sistema, además de mejoras visuales y de accesibilidad. Sigue siendo una demostración sin modelo, backend ni inferencia real.
- El contexto de equipo y del arnés deja de presentar `PG-2` como trabajo activo: la preparación de datos está en `Listo`, `PG-3` queda disponible para el baseline y `PG-5` depende de su evaluación. Esta reconciliación documental no crea tag ni release.
- Las dailies se consolidan en un único documento canónico por fecha dentro de gestión de proyecto; NotebookLM consume esa fuente sin duplicarla.
- El equipo activo pasa a estar formado por José, Abel, Víctor y Miguel tras la baja comunicada de Josué.
- React PWA se confirma como dirección frontend inicial; la evolución nativa queda sujeta a requisitos futuros.
- Las instrucciones de agentes y el workflow reflejan las decisiones actuales y un método OpenSpec independiente del proveedor de IA.
- La estructura adopta creación incremental: conserva contratos en los README y elimina subcarpetas vacías para capacidades todavía no implementadas.
- El estado activo comprende la revisión de la evidencia EDA de Víctor y las
  decisiones de datos posteriores; la React PWA de Abel ya está fusionada.
- `PG-2` deja de estar bloqueada por decisiones de datos y habilita el baseline reproducible de `PG-3`; no existe todavía un modelo entrenado ni métricas de evaluación.
- OpenSpec gobierna los cambios nuevos; `specs/` conserva únicamente los expedientes anteriores y las tareas ya asignadas.
- El piloto con Víctor deja de ser una condición de implantación y pasa a ser una oportunidad de feedback durante su trabajo real.
- La propuesta frontend experimental de la PR `#14` se cierra sin mergear para que Abel defina e implemente el frontend desde una base limpia.
- Jira pasa a conservar responsable, estado y bloqueos; OpenSpec conserva
  requisitos y decisiones, y GitHub conserva implementación y evidencia.
- El estado de aplicación pasa de “prevista” a “prototipo validado pendiente de
  PR y merge”; `ESS-04` continúa sin verificar hasta conectar una inferencia
  real.

### Fixed

- Responsables, estados de specs y tareas, recuentos de tests y documentación de aplicación, producto y scripts sincronizados con el estado real.
- README y niveles de entrega describen el nivel esencial como `En curso` por el EDA activo.
- La primera iteración del arnés deja de presentarse como la solución definitiva; el expediente `004` queda sustituido por la capacidad OpenSpec versionada.
- La normalización de rutas OpenSpec distingue correctamente rutas Windows y POSIX sin permitir fuentes externas al repositorio.
- Las etiquetas del diagrama principal utilizan fondos de 120 unidades, margen interior amplio y centrado consistente después de su validación visual.
- Los veinticinco IDs del briefing permanecen completos en tablas estrechas y se contrastan automáticamente con su estado canónico.
- La PWA bloquea la clasificación sin conexión, excluye narrativas y API de la
  caché y diferencia de forma persistente mocks, sesiones de demostración y
  conceptos administrativos de capacidades reales.
