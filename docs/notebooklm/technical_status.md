# Estado técnico consolidado

## Estado general

- Fase: nivel esencial 10/10 verificado; nivel medio 2/5 y avanzado 3/6,
  con OpenSpec + Harness Engineering operativos.
- Idea de negocio: clasificación y enrutamiento de reclamaciones financieras, elegida por unanimidad con condiciones.
- Dataset: Consumer Complaint Database del CFPB viable con condiciones; target y reglas de EDA versionados.
- Producto demostrable: ClaimVox React PWA integrado mediante las PR #25, #28 y
  #66, con layout unificado, tema y clasificación guiada en cuatro pasos. Una
  URL local explícita habilita la respuesta contractual del servicio FastAPI
  contra un artefacto reproducible; sin API o con backend degradado no se
  muestra categoría. La evidencia conserva revisión humana y no hay servicio
  desplegado.
- Despliegue: no iniciado.
- Feedback: persistencia SQLite local gobernada y flujo explícito posterior a predicción, con creación minimizada y resumen agregado. No hay autenticación, permisos reales, base compartida, operación productiva, corpus ni reentrenamiento automático.
- Seguimiento: Jira `PG` operativo; `PG-11` está en curso, `PG-12` a `PG-14`
  están listos, `PG-16` dispone de rediseño local revisado y `PG-15`/`PG-17`
  permanecen por hacer. Jira no sustituye requisitos ni evidencia versionada.

## Capacidades verificadas

- Rama `dev` creada y configurada como rama predeterminada.
- Estructura inicial integrada en `dev` mediante Pull Request y squash merge.
- Intent global del proyecto integrado y vigente.
- Spec `000-problem-discovery` conservada como expediente histórico de
  descubrimiento; el estado vigente se gobierna con OpenSpec.
- Reglas de evaluación `1.0` aprobadas por mayoría absoluta del equipo activo, con puertas críticas, matriz y gobierno de la selección.
- Dos candidatas evaluadas con la matriz `1.0`: reclamaciones CFPB y clasificación visual de residuos con RealWaste.
- `CAND-001` elegida por José, Abel, Víctor y Miguel con cuatro votos favorables, cero contrarios y cero abstenciones.
- El spike está completado y la spec `001` autoriza el EDA bajo contrato. Las decisiones posteriores de preparación habilitaron y la PR #31 incorporó el baseline reproducible; no autorizan por sí solas inferencia integrada.
- Arnés CFPB reproducible implementado con configuración versionada, probe API, muestra temporal en memoria, informes agregados y siete tests unitarios.
- Probe verificado: 2.306.723 narrativas, catorce etiquetas observadas, licencia CC0 informada por la API y clase mayoritaria del 72,45 %.
- Las puertas de descubrimiento habilitaron el EDA. La privacidad se mantiene
  como control transversal y no como permiso para versionar narrativas.
- El expediente `001-cfpb-target-contract` conserva once clases canónicas, dos
  aliases, una exclusión ambigua y ocho tests de contrato.
- El EDA de Víctor está incorporado mediante la PR #24 con evidencia agregada sobre clases, tiempo, ausencias, duplicados, longitud e idioma. `T-006` aplica para el baseline inicial una política de inglés, grupos completos, split temporal y pesos balanceados; no autoriza conclusiones de modelo.
- El constructor contractual de `T-005` se ha ejecutado sobre una instantánea local actual del CFPB. La preparación posterior de `T-006` obtuvo 1.961.073 filas en inglés y particiones locales de 1.372.751/294.161/294.161 para train/validation/test, sin leakage de grupos y con 100 filas mínimas por clase en validation y test. El informe EDA previo usa otra instantánea; ambos resultados siguen trazados por huella y no se mezclan.
- React PWA confirmada como dirección frontend inicial; el prototipo de `PG-4`
  permite recorrer la captura, respuesta sintética y revisión humana. `PG-6`
  incorpora una ruta local configurada de PWA a API, con respuesta contractual,
  recuperación segura y revisión humana. La evolución nativa sigue pendiente.
- Spec `003-complaint-routing-experience` aporta la arquitectura de información
  y el OpenAPI `0.1.0` contract-only; el frontend implementa su lado del
  contrato mediante un cliente TypeScript y un mock explícito.
- La integración frontend conserva la autoría del trabajo de Abel. El cambio
  OpenSpec `integrate-frontend-foundation` está archivado, la capacidad
  `complaint-routing-interface` está vigente y la PR #25 está fusionada en
  `dev`.
- La PR #28 actualiza la identidad visible a ClaimVox y añade preferencias de
  tema claro, oscuro y sistema, junto a ajustes visuales y de accesibilidad.
  No altera el contrato de predicción ni añade capacidades operativas.
- La batería frontend posterior al rediseño aprueba typecheck, lint, formato,
  63 tests y build PWA. El Dashboard consulta health y el resumen agregado
  local; no expone registros ni convierte Admin en operación compartida. La
  auditoría npm sigue gobernada por el quality gate del repositorio.
- Chrome 150 en Windows verificó instalación, actualización, dictado con permiso
  real, responsive, accesibilidad y recarga del shell sin conexión. Edge queda
  pendiente de la misma comprobación manual.
- La clasificación se bloquea sin conexión, sin URL local y ante un backend
  degradado. La política de caché excluye API, narrativas y peticiones de datos;
  la PWA no fabrica una predicción.
- Login, entrenamiento y registro de modelos permanecen como conceptos
  señalizados. El Dashboard aporta health y feedback agregado locales, pero no
  identidad, permisos, datos compartidos, jobs, evaluación conectada ni modelos
  registrados.
- Flujo humano-IA independiente de proveedor implementado y verificado, con generación acotada de contexto por spec y tarea.
- Primera versión operativa del arnés integrada en `dev` con cuatro roles, cuatro procedimientos y una entrada única probada localmente.
- OpenSpec `1.6.0` fijado como dependencia local, inicializado con configuración propia y adaptadores oficiales para cinco herramientas de IA.
- El arnés consulta validación, estado, instrucciones y tareas de OpenSpec; conserva el modo numerado solo para el EDA y frontend ya asignados.
- El quality gate incorpora instalación reproducible, auditoría npm, diagnóstico y validación estricta de OpenSpec.
- `PG-12` añade puertas locales versionadas para integridad de datos, contrato de modelo y métricas; 16 pruebas sintéticas cubren los criterios `ADV-04` a `ADV-06`. No ejecuta particiones CFPB, no entrena, no persiste artefactos ni opera en producción.
- Responsabilidades principales confirmadas: Miguel en arquitectura y arnés, José en backend, Abel en frontend/UX y Víctor en datos y EDA.
- `PG-2` / `001/T-004` a `T-006` tienen evidencia documental y de preparación completada. El cierre documental del EDA confirma `ESS-02`: script reproducible, informe agregado, cuatro figuras y justificación de visualizaciones para texto, sin narrativas. La PR #31 completa la primera evaluación del baseline de `PG-3`: macro F1 validation `0.5973`, gap train/validation `0.0482`, accuracy validation `0.8484` y una evaluación de test protegido. `ESS-02`, `ESS-03`, `ESS-04`, `ESS-05` y `ESS-06` tienen evidencia mínima; `ESS-04` se verifica mediante el smoke local de `PG-6` fusionado en la PR #40, no como despliegue.
- `PG-5` dispone de FastAPI, validación contractual, predictor real con fallback
  mock y una comprobación local contra un artefacto reproducido. `PG-6` conecta
  ClaimVox bajo una URL local explícita, valida la respuesta, aplica CORS local
  restringido y mantiene revisión humana. `PG-13`/`PG-14` añaden feedback y
  persistencia SQLite locales. Nada de ello acredita autenticación, base
  compartida, despliegue ni producto operativo.
- La comparación ensemble de `MED-01` incorpora Random Forest, XGBoost y LightGBM sobre una muestra de 50K con las mismas métricas que el baseline. XGBoost obtiene el mejor macro F1 de validation (`0.6332`), pero sus gaps superiores al 5 % impiden elegirlo como modelo definitivo; la selección y optimización posterior pertenecen a `MED-03`.
- `PG-7` reconstruye el baseline sobre las particiones locales actuales y genera diagnósticos únicamente sobre validation: matriz de confusión, importancia TF-IDF y análisis agregado de errores. El informe registra macro F1 `0.6390`, accuracy `0.8684` y gap `0.0078`; completa la evidencia de `ESS-01` y `ESS-07` a `ESS-10`, sin acreditar despliegue ni Champion.
- Workflow `repository-quality` ejecutado correctamente y asociado automáticamente a las Pull Requests `#14` y `#15`.
- La PR `#17` se integró en `dev` y verificó en Linux las suites Python, convenciones, whitespace, auditoría npm, diagnóstico y validación estricta de OpenSpec; la ejecución `30000072621` finalizó correctamente.
- `PG-11` continúa bloqueado por falta de CV completa convergida; ningún piloto
  ni rama no fusionada acredita `MED-02`, `MED-03` o un Champion.
- Ruleset `Protect dev` activo con PR y check de calidad obligatorios, historial lineal y bloqueo de force push y borrado.
- Aprobaciones humanas no requeridas temporalmente.
- Estructura simplificada para crear subcarpetas de aplicación, ML, MLOps, infraestructura y evidencias únicamente cuando contengan una capacidad real.
- Backlog esencial creado después de aprobación humana: `PG-1` y seis elementos
  `PG-2` a `PG-7`; `PG-2` está asignada a Víctor y `PG-4` a Abel.
- El arnés valida referencias `PG-N`, admite excepciones controladas de bootstrap,
  emergencia o automatización y transporta el seguimiento sin credenciales.
- Jira conserva ocho relaciones de bloqueo verificadas entre `PG-2` y `PG-7`;
  la jerarquía y las dependencias coinciden con el orden de entrega esencial.
- La capacidad OpenSpec `jira-work-tracking` está vigente después del archivo
  revisado de `integrate-jira-workflow`.

## Controles locales recientes

- La guía canónica de ClaimVox separa la demostración mock de la inferencia
  local real y fija los comandos Git Bash, ruta de health y límites de caché
  PWA para revisión local. No cambia el modelo, el servicio ni el estado de
  entrega; la evidencia está en
  `reports/validation/claimvox_local_runbook_review.md`.
- `PG-18` mejora el resultado de clasificación local sin alterar API ni modelo:
  distingue API local de mock, limita alternativas, preserva revisión humana y
  retira la sesión mock del recorrido público. La administración continúa
  sin operación compartida; el Dashboard de `PG-16` sí refleja health y
  conteo/desglose agregado del feedback local sin inventar métricas. Evidencia en
  `reports/validation/claimvox_local_classification_usability.md`.
- El cierre de `PG-16` supera 63 pruebas frontend, 134 unitarias Python y 35
  pruebas de contrato, además de build PWA, OpenSpec estricto, diagnóstico del
  arnés y quality gate. Estos controles no equivalen a despliegue.
- El cambio `mvp-readiness-and-presentation` añade límites proporcionados para
  la API local: máximo de narrativa, frecuencia efímera en memoria, cabeceras
  de respuesta y un evento técnico sin identidad ni contenido. La evidencia
  está en `reports/validation/mvp_readiness_inventory.md`. No crea cuentas,
  almacenamiento, analítica de usuarios ni observabilidad productiva.

## Capacidades previstas, no implementadas

- Selección y gobierno de un Champion. Existe un baseline reproducible y un
  servicio local capaz de cargarlo, pero no un modelo aprobado para producción.
- Operación compartida de feedback, métricas operativas de producción y recolección validada para reentrenamiento; el flujo local minimizado sí está verificado extremo a extremo, pero sigue sin corpus ni incorporación automática.
- Docker y despliegue.
- CI/CD completo.
- Red neuronal, A/B testing, drift y promoción.

## Riesgos actuales

- Tratar el baseline evaluado como un Champion, una inferencia integrada o una capacidad de producto operativa.
- Confundir estructura preparada con funcionalidad implementada.
- Confundir la respuesta sintética del prototipo, el login mock o las pantallas
  administrativas propuestas con capacidades operativas.
- Integrar entregas heredadas de frontend o EDA sin adaptar mediante OpenSpec cualquier decisión que cambie contratos o alcance.
- Los roles de respaldo y la cobertura estable de producto, MLOps y QA siguen sin asignar.
- La política inicial está versionada; siguen pendientes la evaluación de cobertura multilingüe, la política de retención operativa y toda decisión posterior basada en resultados de modelo.
- El fuerte crecimiento de reclamaciones de informes de crédito puede producir desbalanceo extremo y cambios de procedencia que limiten la representatividad.
- La muestra temporal detecta drift de etiquetas y duplicación: el extremo de 2023 concentra la etiqueta histórica y muchos más duplicados que el extremo de 2026.
- La publicación reciente de narrativas presenta retraso y la API tiene comportamiento dependiente del cliente y paginación no trivial.
