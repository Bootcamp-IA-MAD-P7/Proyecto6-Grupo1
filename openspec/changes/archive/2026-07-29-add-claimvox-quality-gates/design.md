## Context

El repositorio ya dispone de construcción de corpus, preparación con partición
aislada por `narrative_hash`, baseline local y evidencia agregada de evaluación.
Existen pruebas parciales de cada componente, pero no una puerta unificada que
impida aceptar datos, artefactos o métricas que contradigan sus contratos. El
cambio `PG-12` convierte esas comprobaciones en quality gates locales y
reproducibles para `ADV-04`, `ADV-05` y `ADV-06`.

## Goals / Non-Goals

**Goals:**

- Verificar contratos de datos, comportamiento del modelo y métricas mediante
  entradas sintéticas o evidencia agregada versionada.
- Fallar de forma explícita ante un esquema, clase, grupo, artefacto o métrica
  no conforme.
- Mantener el test protegido y los corpus locales fuera de los checks.
- Producir resultados concisos, sin narrativas CFPB ni información sensible.

**Non-Goals:**

- Entrenar, reentrenar, optimizar o promover modelos.
- Modificar los valores de métricas, la partición, la política de datos o la
  inferencia de ClaimVox.
- Añadir despliegue, persistencia, autenticación, dependencias externas o CI/CD.

## Decisions

### Tres puertas locales con una interfaz común

Se implementarán puertas separadas de datos, modelo y métricas, invocables de
forma individual y desde un comprobador local común. Cada puerta recibirá rutas
explícitas de artefactos permitidos y devolverá éxito o fallo con un mensaje
agregado. Esta separación permite aislar errores y evita cargar el corpus o
entrenar durante la verificación.

Alternativa descartada: una única suite que ejecute preparación y entrenamiento.
Consumiría recursos, mezclaría responsabilidades y aumentaría el riesgo de
exponer datos locales.

### Contratos versionados y fixtures sintéticos

Los umbrales aprobados, clases y rutas permitidas se obtendrán de contratos
versionados existentes o de una configuración específica del gate. Las pruebas
usarán fixtures sintéticos; las ejecuciones sobre evidencia real leerán solo
manifiestos y reportes agregados ya versionables.

Alternativa descartada: codificar umbrales y clases en cada test. Duplicaría los
contratos y permitiría divergencias silenciosas.

### Inventario canónico de entradas de cada puerta

La puerta de datos consumirá `config/cfpb_target_contract.json` como fuente de
las once etiquetas, la feature permitida, las columnas prohibidas y la política
de privacidad; consumirá `config/cfpb_training_policy.json` como fuente de
`narrative_hash`, política de duplicados, partición temporal aislada, test
protegido y soporte mínimo por clase. No duplicará estos valores.

La puerta de modelo consumirá el contrato de feature y clases de
`config/cfpb_target_contract.json`, y la configuración agregada del baseline en
`reports/validation/cfpb_baseline_metrics.json`. La ubicación concreta del
artefacto controlado quedará declarada en la configuración de la tarea 1.2; no
existe un binario versionado que pueda convertirse en fuente de verdad.

La puerta de métricas consumirá el macro F1 y el límite de gap de
`config/cfpb_training_policy.json`, junto con los campos agregados de train,
validation y métricas por clase de
`reports/validation/cfpb_baseline_metrics.json`. El bloque de test protegido no
participará en ningún umbral de selección o promoción.

### Integridad de datos sin leer narrativas

La puerta de datos validará columnas autorizadas, once clases, nulos, grupos
duplicados, conflictos y separación de `narrative_hash` entre particiones. No
debe imprimir textos, identificadores de reclamación ni filas del corpus.

### Modelo y métricas como contratos distintos

La puerta de modelo comprobará carga desde ubicación controlada, compatibilidad
de features, forma de probabilidades, clases canónicas e inferencia controlada.
La puerta de métricas comprobará que un reporte agregado contiene los campos
requeridos y respeta los umbrales ya aprobados, incluido el gap train-validation
inferior a 0.05. Ninguna puerta decidirá un Champion.

## Risks / Trade-offs

- [Evidencia agregada incompleta] → el gate falla y solicita el campo faltante,
  sin recalcular métricas ni acceder a datos locales.
- [Artefacto no compatible] → el gate rechaza la carga antes de servir una
  predicción.
- [Umbral no aprobado] → el gate no inventa un valor; exige configuración
  versionada y deja la decisión abierta.
- [Falsa sensación de producción] → las evidencias declararán que son controles
  locales y no sustituyen despliegue, monitorización o autorización distribuida.

## Migration Plan

No hay migración de datos ni de APIs. Los gates se añadirán como comprobaciones
locales y pruebas unitarias; si un gate produce falsos positivos, se revierte el
cambio completo y se conserva el comportamiento actual sin alterar artefactos.

## Open Questions

- Confirmar qué artefacto agregado será la fuente canónica del gate de métricas
  para una futura selección de modelo gobernada.
- Confirmar si los gates se incorporarán a CI en un cambio posterior de
  infraestructura, sin ejecutar entrenamiento en GitHub Actions.
