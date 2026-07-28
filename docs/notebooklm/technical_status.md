# Estado técnico consolidado

## Estado general

- Fase: preparación de datos cerrada y baseline reproducible evaluado, con OpenSpec + Harness Engineering operativos.
- Idea de negocio: clasificación y enrutamiento de reclamaciones financieras, elegida por unanimidad con condiciones.
- Dataset: Consumer Complaint Database del CFPB viable con condiciones; target y reglas de EDA versionados.
- Producto demostrable: ClaimVox React PWA integrado mediante las PR #25 y #28,
  con tema configurable y mock seguro por defecto. Una URL local explícita
  habilita la respuesta contractual del servicio FastAPI contra un artefacto
  reproducible; la evidencia conserva revisión humana y no hay servicio
  desplegado.
- Despliegue: no iniciado.
- Seguimiento: Jira `PG` operativo para responsables, estados y bloqueos; `PG-1`
  agrupa el nivel esencial sin sustituir requisitos ni evidencias versionadas.

## Capacidades verificadas

- Rama `dev` creada y configurada como rama predeterminada.
- Estructura inicial integrada en `dev` mediante Pull Request y squash merge.
- Intent global del proyecto integrado y vigente.
- Spec `000-problem-discovery` activa para gobernar la evaluación y el cierre de las puertas de datos.
- Reglas de evaluación `1.0` aprobadas por mayoría absoluta del equipo activo, con puertas críticas, matriz y gobierno de la selección.
- Dos candidatas evaluadas con la matriz `1.0`: reclamaciones CFPB y clasificación visual de residuos con RealWaste.
- `CAND-001` elegida por José, Abel, Víctor y Miguel con cuatro votos favorables, cero contrarios y cero abstenciones.
- El spike está completado y la spec `001` autoriza el EDA bajo contrato. Las decisiones posteriores de preparación habilitaron y la PR #31 incorporó el baseline reproducible; no autorizan por sí solas inferencia integrada.
- Arnés CFPB reproducible implementado con configuración versionada, probe API, muestra temporal en memoria, informes agregados y siete tests unitarios.
- Probe verificado: 2.306.723 narrativas, catorce etiquetas observadas, licencia CC0 informada por la API y clase mayoritaria del 72,45 %.
- G-02, G-03, G-04 y G-06 superadas para EDA; G-05 continúa condicionada por la revisión de privacidad.
- Spec `001-cfpb-target-contract` activa con once clases canónicas, dos aliases, una exclusión ambigua y ocho tests unitarios de contrato de target.
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
- La batería frontend aprueba typecheck, lint, formato, 31 tests, build PWA y
  auditoría npm con cero vulnerabilidades.
- Chrome 150 en Windows verificó instalación, actualización, dictado con permiso
  real, responsive, accesibilidad y recarga del shell sin conexión. Edge queda
  pendiente de la misma comprobación manual.
- La clasificación se bloquea sin conexión y la política de caché excluye API,
  narrativas y peticiones de datos; el prototipo no fabrica una predicción.
- Login, administración, entrenamiento y registro de modelos permanecen como
  conceptos señalizados: no aportan identidad, permisos, datos, jobs ni modelos.
- Flujo humano-IA independiente de proveedor implementado y verificado, con generación acotada de contexto por spec y tarea.
- Primera versión operativa del arnés integrada en `dev` con cuatro roles, cuatro procedimientos y una entrada única probada localmente.
- OpenSpec `1.6.0` fijado como dependencia local, inicializado con configuración propia y adaptadores oficiales para cinco herramientas de IA.
- El arnés consulta validación, estado, instrucciones y tareas de OpenSpec; conserva el modo numerado solo para el EDA y frontend ya asignados.
- El quality gate incorpora instalación reproducible, auditoría npm, diagnóstico y validación estricta de OpenSpec.
- Responsabilidades principales confirmadas: Miguel en arquitectura y arnés, José en backend, Abel en frontend/UX y Víctor en datos y EDA.
- `PG-2` / `001/T-004` a `T-006` tienen evidencia documental y de preparación completada. El cierre documental del EDA confirma `ESS-02`: script reproducible, informe agregado, cuatro figuras y justificación de visualizaciones para texto, sin narrativas. La PR #31 completa la primera evaluación del baseline de `PG-3`: macro F1 validation `0.5973`, gap train/validation `0.0482`, accuracy validation `0.8484` y una evaluación de test protegido. `ESS-02`, `ESS-03`, `ESS-04`, `ESS-05` y `ESS-06` tienen evidencia mínima; `ESS-04` se verifica mediante el smoke local de `PG-6` fusionado en la PR #40, no como despliegue.
- `PG-5` dispone de FastAPI, validación contractual, predictor real con fallback mock y una comprobación local contra un artefacto reproducido con las particiones aprobadas. `PG-6` conecta ClaimVox bajo una URL local explícita, valida la respuesta, aplica CORS local restringido y mantiene revisión humana. Ninguna de estas evidencias acredita autenticación, persistencia, despliegue ni producto operativo.
- La comparación ensemble de `MED-01` incorpora Random Forest, XGBoost y LightGBM sobre una muestra de 50K con las mismas métricas que el baseline. XGBoost obtiene el mejor macro F1 de validation (`0.6332`), pero sus gaps superiores al 5 % impiden elegirlo como modelo definitivo; la selección y optimización posterior pertenecen a `MED-03`.
- `PG-7` reconstruye el baseline sobre las particiones locales actuales y genera diagnósticos únicamente sobre validation: matriz de confusión, importancia TF-IDF y análisis agregado de errores. El informe registra macro F1 `0.6390`, accuracy `0.8684` y gap `0.0078`; completa la evidencia de `ESS-01` y `ESS-07` a `ESS-10`, sin acreditar despliegue ni Champion.
- Workflow `repository-quality` ejecutado correctamente y asociado automáticamente a las Pull Requests `#14` y `#15`.
- La PR `#17` se integró en `dev` y verificó en Linux las suites Python, convenciones, whitespace, auditoría npm, diagnóstico y validación estricta de OpenSpec; la ejecución `30000072621` finalizó correctamente.
- El piloto con Víctor ya no bloquea la implantación; su tarea real servirá para recoger feedback del uso heredado y adaptar decisiones nuevas mediante OpenSpec.
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

## Capacidades previstas, no implementadas

- Selección y gobierno de un Champion. Existe un baseline reproducible y un
  servicio local capaz de cargarlo, pero no un modelo aprobado para producción.
- Persistencia y feedback.
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
