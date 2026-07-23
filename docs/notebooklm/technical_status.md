# Estado técnico consolidado

## Estado general

- Fase: descubrimiento y EDA con OpenSpec + Harness Engineering operativos.
- Idea de negocio: clasificación y enrutamiento de reclamaciones financieras, elegida por unanimidad con condiciones.
- Dataset: Consumer Complaint Database del CFPB viable con condiciones; target y reglas de EDA versionados.
- Código de producto funcional: no iniciado; existen scripts de validación y automatización del trabajo.
- Despliegue: no iniciado.

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
- React PWA confirmada como dirección frontend inicial; backend, implementación de inferencia y evolución nativa siguen pendientes.
- Spec `003-complaint-routing-experience` preparada con arquitectura de información, OpenAPI contract-only y siete tests; no existe aún frontend ni servicio.
- Flujo humano-IA independiente de proveedor implementado y verificado, con generación acotada de contexto por spec y tarea.
- Primera versión operativa del arnés integrada en `dev` con cuatro roles, cuatro procedimientos y una entrada única probada localmente.
- OpenSpec `1.6.0` fijado como dependencia local, inicializado con configuración propia y adaptadores oficiales para cinco herramientas de IA.
- El arnés consulta validación, estado, instrucciones y tareas de OpenSpec; conserva el modo numerado solo para el EDA y frontend ya asignados.
- El quality gate incorpora instalación reproducible, auditoría npm, diagnóstico y validación estricta de OpenSpec.
- Responsabilidades principales confirmadas: Miguel en arquitectura y arnés, José en backend, Abel en frontend/UX y Víctor en datos y EDA.
- El trabajo de producto activo desde `dev` comprende la incorporación de evidencia del EDA en `001/T-004` y el inicio desde cero de la React PWA en `003/T-006`.
- Workflow `repository-quality` ejecutado correctamente y asociado automáticamente a las Pull Requests `#14` y `#15`.
- La PR `#17` se integró en `dev` y verificó en Linux las suites Python, convenciones, whitespace, auditoría npm, diagnóstico y validación estricta de OpenSpec; la ejecución `30000072621` finalizó correctamente.
- El piloto con Víctor ya no bloquea la implantación; su tarea real servirá para recoger feedback del uso heredado y adaptar decisiones nuevas mediante OpenSpec.
- Ruleset `Protect dev` activo con PR y check de calidad obligatorios, historial lineal y bloqueo de force push y borrado.
- Aprobaciones humanas no requeridas temporalmente.
- Estructura simplificada para crear subcarpetas de aplicación, ML, MLOps, infraestructura y evidencias únicamente cuando contengan una capacidad real.

## Capacidades previstas, no implementadas

- Pipeline de datos y entrenamiento.
- Aplicación React PWA multiclase.
- Persistencia y feedback.
- Docker y despliegue.
- CI/CD completo.
- Red neuronal, A/B testing, drift y promoción.

## Riesgos actuales

- Tratar la viabilidad condicionada como si idioma, privacidad y partición ya estuvieran cerrados.
- Confundir estructura preparada con funcionalidad implementada.
- Integrar entregas heredadas de frontend o EDA sin adaptar mediante OpenSpec cualquier decisión que cambie contratos o alcance.
- Los roles de respaldo y la cobertura estable de producto, MLOps y QA siguen sin asignar.
- La normalización de target está versionada; idioma, deduplicación final, partición, desbalanceo y privacidad siguen pendientes de la evidencia del EDA.
- El fuerte crecimiento de reclamaciones de informes de crédito puede producir desbalanceo extremo y cambios de procedencia que limiten la representatividad.
- La muestra temporal detecta drift de etiquetas y duplicación: el extremo de 2023 concentra la etiqueta histórica y muchos más duplicados que el extremo de 2026.
- La publicación reciente de narrativas presenta retraso y la API tiene comportamiento dependiente del cliente y paginación no trivial.
