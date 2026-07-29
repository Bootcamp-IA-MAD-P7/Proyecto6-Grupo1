# Changelog

## Unreleased

### Added

- `PG-12`: tres quality gates locales y configurables para integridad de datos,
  contrato de modelo y métricas agregadas. Las 16 pruebas usan exclusivamente
  fixtures y artefactos sintéticos; no acreditan entrenamiento, datos CFPB
  reales, Champion, persistencia, despliegue ni MLOps.

- Guía canónica para ejecutar ClaimVox localmente con Git Bash: diferencia mock
  seguro e inferencia local real, comprueba `GET /api/v1/health`, declara CORS
  local y explica una recuperación proporcional ante caché PWA anterior. No
  añade despliegue, datos, autenticación, persistencia ni cambios de aplicación.
- README reorganizado para evaluación: recorrido seguro de ClaimVox en cinco
  minutos, resumen ejecutivo, evidencias esenciales enlazadas, arquitectura
  actual frente a evolución prevista y hoja de ruta verificable. No modifica
  la aplicación ni amplía capacidades del MVP.
- Preparación de MVP local ClaimVox: máximo de 5.000 caracteres, 20
  predicciones/minuto por cliente temporal en memoria, cabeceras de respuesta
  seguras y eventos técnicos sin identidad ni contenido. No añade cuentas,
  persistencia de narrativas, analítica de usuarios ni despliegue.
- Inventario verificable de preparación del MVP y guion de presentación para
  cliente/evaluador, con evidencia y límites explícitos.

- `PG-7`: evaluación esencial reconstruible del baseline sobre las particiones locales actuales, sin cargar test protegido: macro F1 validation `0.6390`, accuracy `0.8684` y gap train-validation `0.0078`. Añade matriz de confusión, importancia TF-IDF, análisis agregado de errores, manifiesto local e informe/guía de entrega.
- `PG-6`: integración local explícita entre ClaimVox y `POST /api/v1/predictions`, con transporte TypeScript validado, CORS local de mínimo privilegio, estados de recuperación seguros y smoke end-to-end con entrada sintética. El mock sigue siendo el valor por defecto.

- MED-01: Módulo reutilizable `src/ml/` con vectorizador, evaluación, modelos (RF, XGBoost), tuning con Optuna y visualización.
- MED-01: `scripts/ml/train_ensemble.py` para entrenar, evaluar y comparar Random Forest y XGBoost, con figuras (confusión, importancia, comparativa) y reporte Markdown+JSON.
- MED-01: `scripts/ml/train_baseline.py` refactorizado para consumir `src/ml/vectorizer` y `src/ml/evaluation`.
- MED-01: Tests unitarios (9) e integración (5) para modelos ensemble.
- MED-01: Primeros resultados RF (val macro F1 0.4704) y XGBoost (val macro F1 0.6331) sobre muestra de 50K filas.
- MED-01: LightGBM (GPU) añadido como extensión; XGBoost obtiene el mejor macro F1 de validación (`0.6332`) sobre muestra de 50K, sin selección definitiva por su gap superior al 5 %.

### Changed

- `PG-6` y la PR #40 verifican `ESS-04`: la React PWA consume inferencia local real con respuesta contractual y revisión humana. No acredita autenticación, persistencia, despliegue ni una operación productiva.

- `pyproject.toml` incluye `xgboost>=2.1.0`, `optuna>=4.0.0`, `joblib>=1.5.0`.
- README actualizado: MED-01/MED-03 pasan a `En curso`; ESS-07/ESS-08 pasan a `En curso`.
- `delivery_levels.md` sincronizado con el estado actual de los criterios.
- Gráfico de estado actualizado a 2026-07-27 (5 verificados, 4 en curso, 16 no iniciados); la PR #36 se fusionó posteriormente.
- README, delivery_levels.md y chart actualizados: MED-01 pasa a `Verificado` (5/25 criterios); XGBoost obtiene el mejor macro F1 de validación (`0.6332`) sin selección definitiva.

### Fixed

- El gráfico de entrega fechado el 27 de julio vuelve a reflejar el estado
  canónico: 11 criterios verificados, 2 en curso y 12 no iniciados; el nivel
  esencial permanece completo con 10 de 10.

- `repository-quality.yml` usa `pip install -e .` para mantener dependencias sincronizadas con `pyproject.toml`.
- `scripts/ml/train_ensemble.py` escribe reporte con `encoding="utf-8"` para compatibilidad Windows.
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
- Integración frontend de Abel fusionada mediante la PR `#25`; en esa entrega la
  PWA usaba respuestas sintéticas. La integración local posterior se registra
  separadamente en `PG-6`.
- Constructor local contractual para `T-005` / `PG-2`, con rutas explícitas,
  soporte seguro de ZIP, filtros, aliases, exclusiones, huella de narrativa,
  exclusión de conflictos y manifiesto agregado sin textos CFPB.
- Seis pruebas sintéticas del constructor y evidencia agregada de una ejecución
  local de 1.998.570 filas, conservando las decisiones de `T-006` abiertas.
- Política versionada de preparación para `PG-2` / `T-006`: huellas de fuente y contrato, inglés para el baseline inicial, grupos de duplicados aislados, split temporal 70/15/15, mínimo de 100 filas por clase en validation y test, macro F1 y pesos balanceados.
- Particiones locales reproducibles para 1.961.073 filas en inglés, con manifiesto agregado, evidencia de soporte de las once clases y pruebas sintéticas de idioma, huellas, grupos y orden temporal.
- Baseline `PG-3` entrenado y optimizado con TF‑IDF (unigramas+bigramas, sublinear_tf, 8K features) + LogisticRegression (C=0.1, balanced). Val macro F1 **0.5973**, gap **0.0482** ✅, accuracy **0.8484**. Clases débiles documentadas. Hiperparámetros explorados en 4 configuraciones.
- Evidencia protegida del baseline: macro F1 de test **0.6625**, accuracy **0.8230** y métricas por las once clases en JSON versionados. El artefacto local permanece fuera de Git.
- Cierre verificable de `ESS-02`: el informe EDA enlaza el script reproducible, cuatro figuras agregadas, visualizaciones pertinentes para texto multiclase y las decisiones posteriores de preparación, sin exponer narrativas ni mezclar instantáneas.

- Backend foundation (`PG-5`): servicio FastAPI en `app/api/` con endpoint de predicción (`POST /api/v1/predictions`) y health (`GET /api/v1/health`), conforme al contrato `docs/api/openapi.json`. Carga el baseline real (`models/cfpb_baseline.pkl`) cuando está disponible; opera en modo mock claramente identificado cuando no. Interfaz de predictor extensible para futuro RAG sin modificar rutas. 22 tests de contrato pasando. No incluye autenticación, CORS, rate limiting, persistencia ni Docker.
- `PG-5`: verificación local del servicio con un artefacto baseline reproducido a partir de las particiones aprobadas, sin incorporar datos ni artefactos pesados a Git. Health devuelve `ok` y la predicción usa clases canónicas, confianza numérica y no repite la narrativa. La evidencia agregada está en `reports/validation/backend_foundation_real_smoke.md`.

### Changed

- El prototipo React PWA integrado adopta la identidad visible ClaimVox mediante la PR #28, con preferencias de tema claro, oscuro y sistema, además de mejoras visuales y de accesibilidad. En esa PR permanecía desacoplado del backend; la integración local posterior se registra separadamente en `PG-6`.
- `PG-2` queda en `Listo` y la PR #31 incorpora el baseline de `PG-3`. La evidencia del baseline habilita el trabajo de contrato/backend, pero no acredita inferencia integrada ni un producto operativo.
- Las dailies se consolidan en un único documento canónico por fecha dentro de gestión de proyecto; NotebookLM consume esa fuente sin duplicarla.
- El equipo activo pasa a estar formado por José, Abel, Víctor y Miguel tras la baja comunicada de Josué.
- React PWA se confirma como dirección frontend inicial; la evolución nativa queda sujeta a requisitos futuros.
- Las instrucciones de agentes y el workflow reflejan las decisiones actuales y un método OpenSpec independiente del proveedor de IA.
- La estructura adopta creación incremental: conserva contratos en los README y elimina subcarpetas vacías para capacidades todavía no implementadas.
- El estado activo comprende la revisión de la evidencia EDA de Víctor y las
  decisiones de datos posteriores; la React PWA de Abel ya está fusionada.
- `PG-2` deja de estar bloqueada por decisiones de datos y habilita el baseline reproducible de `PG-3`; en ese momento aún no existía un modelo entrenado ni métricas de evaluación.
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
- README, gráfico y niveles de entrega reflejan `ESS-02` como verificado y mantienen el nivel esencial global en curso.
- La primera iteración del arnés deja de presentarse como la solución definitiva; el expediente `004` queda sustituido por la capacidad OpenSpec versionada.
- La normalización de rutas OpenSpec distingue correctamente rutas Windows y POSIX sin permitir fuentes externas al repositorio.
- Las etiquetas del diagrama principal utilizan fondos de 120 unidades, margen interior amplio y centrado consistente después de su validación visual.
- Los veinticinco IDs del briefing permanecen completos en tablas estrechas y se contrastan automáticamente con su estado canónico.
- La PWA bloquea la clasificación sin conexión, excluye narrativas y API de la
  caché y diferencia de forma persistente mocks, sesiones de demostración y
  conceptos administrativos de capacidades reales.
