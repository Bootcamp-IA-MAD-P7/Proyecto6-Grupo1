## Why

El constructor local de `T-005` ya genera un corpus contractual reproducible, pero el entrenamiento sigue bloqueado porque aún no hay una política aprobada para la instantánea de referencia, idioma, duplicados no conflictivos, partición y desbalanceo. Cerrar estas decisiones ahora permite iniciar un baseline honesto sin convertir hipótesis en resultados.

## What Changes

- Fijar la instantánea CFPB descargada el 27 de julio de 2026 como referencia inicial para el baseline, identificada por su huella de fuente y contrato.
- Adoptar una política inicial de idioma inglés, cuantificada y reversible antes de cualquier entrenamiento.
- Preservar los grupos duplicados no conflictivos como grupos indivisibles y excluir los grupos con targets contradictorios ya cuantificados.
- Definir una partición temporal con grupos de narrativa aislados entre train, validation y test.
- Adoptar `macro F1` como métrica primaria del baseline y `class_weight="balanced"` como tratamiento inicial del desbalanceo.
- Mantener explícitamente fuera de alcance el entrenamiento, la comparación de modelos y la verificación de criterios de entrega.

## Capabilities

### New Capabilities

- `cfpb-training-policy`: política versionada y verificable para preparar el corpus local CFPB antes de entrenar un baseline multiclase.

### Modified Capabilities

- Ninguna. No cambia las capacidades vigentes de interfaz, Jira, gobierno OpenSpec o calidad de presentación.

## Impact

- **Entrega:** prepara `ESS-01`, `ESS-02`, `ESS-03`, `ESS-05` a `ESS-09` y `MED-02`, sin verificar ninguno.
- **Datos / ML:** afectará al siguiente constructor de particiones y al baseline; no modifica las once clases ni permite campos prohibidos.
- **Privacidad:** mantiene las narrativas únicamente en artefactos locales ignorados; Git, Jira, informes y prompts externos conservan cifras agregadas.
- **Producto:** no modifica React PWA, backend, contratos de inferencia, despliegue ni MLOps.

## Tracking

- Jira: `PG-2`.
- Expediente de compatibilidad: `specs/001-cfpb-target-contract/`, tarea `T-006`.
