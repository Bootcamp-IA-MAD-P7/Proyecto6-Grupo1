# Estado técnico consolidado

## Estado general

- Fase: descubrimiento y EDA con OpenSpec + Harness Engineering operativos.
- Idea de negocio: clasificación y enrutamiento de reclamaciones financieras, elegida por unanimidad con condiciones.
- Dataset: Consumer Complaint Database del CFPB viable con condiciones; target y reglas de EDA versionados.
- Producto demostrable: prototipo React PWA validado en la rama de `PG-4` con
  respuestas sintéticas, pendiente de revisión y merge; todavía no existe una
  predicción real ni un servicio operativo.
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
- El spike está completado y la spec `001` autoriza el EDA bajo contrato; todavía no autoriza entrenamiento o implementación funcional.
- Arnés CFPB reproducible implementado con configuración versionada, probe API, muestra temporal en memoria, informes agregados y siete tests unitarios.
- Probe verificado: 2.306.723 narrativas, catorce etiquetas observadas, licencia CC0 informada por la API y clase mayoritaria del 72,45 %.
- G-02, G-03, G-04 y G-06 superadas para EDA; G-05 continúa condicionada por la revisión de privacidad.
- Spec `001-cfpb-target-contract` activa con once clases canónicas, dos aliases, una exclusión ambigua y ocho tests unitarios de contrato de target.
- El EDA continúa en paralelo y debe aportar evidencia agregada sobre clases, tiempo, ausencias, duplicados, longitud e idioma.
- React PWA confirmada como dirección frontend inicial; el prototipo de `PG-4`
  ya permite recorrer la captura, respuesta sintética y revisión humana, pero
  backend, inferencia real y evolución nativa siguen pendientes.
- Spec `003-complaint-routing-experience` aporta la arquitectura de información
  y el OpenAPI `0.1.0` contract-only; el frontend implementa su lado del
  contrato mediante un cliente TypeScript y un mock explícito.
- La rama de integración frontend conserva la autoría del trabajo de Abel y
  está gobernada por el cambio OpenSpec `integrate-frontend-foundation`; todavía
  no se ha publicado su Pull Request ni fusionado en `dev`.
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
- El trabajo activo comprende la evidencia del EDA en `001/T-004` y la revisión
  humana y preparación de PR de la React PWA mediante `PG-4` y
  `integrate-frontend-foundation`.
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

- Pipeline de datos y entrenamiento.
- Conexión de la React PWA con backend e inferencia multiclase reales.
- Persistencia y feedback.
- Docker y despliegue.
- CI/CD completo.
- Red neuronal, A/B testing, drift y promoción.

## Riesgos actuales

- Tratar la viabilidad condicionada como si idioma, privacidad y partición ya estuvieran cerrados.
- Confundir estructura preparada con funcionalidad implementada.
- Confundir la respuesta sintética del prototipo, el login mock o las pantallas
  administrativas propuestas con capacidades operativas.
- Integrar entregas heredadas de frontend o EDA sin adaptar mediante OpenSpec cualquier decisión que cambie contratos o alcance.
- Los roles de respaldo y la cobertura estable de producto, MLOps y QA siguen sin asignar.
- La normalización de target está versionada; idioma, deduplicación final, partición, desbalanceo y privacidad siguen pendientes de la evidencia del EDA.
- El fuerte crecimiento de reclamaciones de informes de crédito puede producir desbalanceo extremo y cambios de procedencia que limiten la representatividad.
- La muestra temporal detecta drift de etiquetas y duplicación: el extremo de 2023 concentra la etiqueta histórica y muchos más duplicados que el extremo de 2026.
- La publicación reciente de narrativas presenta retraso y la API tiene comportamiento dependiente del cliente y paginación no trivial.
