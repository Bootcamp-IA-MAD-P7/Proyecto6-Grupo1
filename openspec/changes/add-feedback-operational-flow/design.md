## Context

`PG-14` ya valida y conserva registros de feedback minimizados en SQLite local,
aislado de la predicción. ClaimVox y FastAPI no exponen todavía una operación
para registrar una decisión humana ni un resumen de seguimiento. `PG-13`
conecta ambas fronteras localmente para aportar evidencia a `MED-04` y preparar
`MED-05`, sin convertir el almacenamiento local en una operación compartida.

## Goals / Non-Goals

**Goals:**

- Registrar, tras una predicción y una acción explícita, feedback que cumpla
  `config/claimvox_feedback_persistence_policy.json`.
- Exponer al cliente local un resumen agregado por `model_version`,
  `suggested_class` y `decision`, sin registros individuales.
- Mostrar en ClaimVox una revisión humana de vocabulario cerrado y sus estados
  seguros, sin bloquear la predicción.
- Definir candidatos de reentrenamiento como metadatos sujetos a revisión
  posterior, sin incorporarlos a corpus ni entrenamiento.

**Non-Goals:**

- Autenticación, autorización, cuentas, permisos multiusuario, base de datos
  compartida, red, Docker, despliegue, analítica de usuarios o MLOps.
- Persistir narrativas, transcripciones, identidad, texto libre, probabilidades
  completas o cualquier campo prohibido por la política.
- Seleccionar o promover un Champion, modificar predicciones o reentrenar un
  modelo automáticamente.

## Decisions

### Operación local posterior y aislada

Se añadirá un contrato local separado de predicción para crear feedback y leer
un resumen agregado. La creación recibirá únicamente el `prediction_id` de la
respuesta, versiones, clases canónicas, decisión, finalidad y marcas UTC. La
predicción seguirá funcionando si el registro falla; el error se comunicará sin
revelar la entrada. Se descarta acoplar feedback al endpoint de predicción para
preservar la frontera explícita aprobada en PG-14.

### Política como autoridad de campos y retención

El esquema, el servicio y la interfaz derivarán decisiones, finalidades,
clases, campos prohibidos, raíz local y retención de la política versionada. Se
rechazarán propiedades adicionales antes de persistir. Se descarta un formulario
libre porque no permite controlar privacidad ni reutilización.

### Métrica agregada, no analítica operativa

El resumen devolverá contadores agrupados por versión, clase sugerida y
decisión, tras purgar vencidos de forma idempotente. No habrá exportación de
registros individuales, panel administrativo operativo ni telemetría de
usuarios. Esta decisión genera evidencia local de feedback, no observabilidad
de producción.

### Recolección como candidato revisable

La finalidad `future_retraining_candidate` identifica únicamente un registro
de metadatos elegible para una revisión futura. No representa nuevos datos de
entrenamiento porque carece de narrativa y porque faltan validación,
deduplicación, política de incorporación y aprobación humana.

## Risks / Trade-offs

- [Sin identidad ni permisos] → el alcance se restringe a ejecución local y se
  documenta que no es un servicio multiusuario ni desplegable.
- [Un `prediction_id` técnico no autentica una persona] → no se usa para
  autorizar operaciones ni se expone en resúmenes.
- [Feedback sin narrativa no permite reentrenar] → se conserva solo como señal
  agregada y candidata, no como corpus.
- [Error de persistencia] → la respuesta de clasificación no se modifica y el
  cliente ofrece recuperación segura.

## Migration Plan

1. Añadir esquemas y rutas locales versionadas sobre el repositorio PG-14.
2. Añadir cliente y controles de revisión tras un resultado válido.
3. Probar con fixtures sintéticos y una base temporal bajo la raíz controlada.
4. Registrar evidencia agregada y actualizar el estado de entrega solo si se
   cumplen los criterios mínimos.

Reversión: retirar las rutas y la interfaz de feedback; la predicción conserva
su contrato y el almacén local existente no se migra a un servicio compartido.

## Open Questions

- Qué validación, deduplicación y aprobación harán que un candidato pueda
  incorporarse a un corpus futuro.
- Qué identidad, permisos y almacenamiento compartido exigiría una operación
  fuera del equipo local.
