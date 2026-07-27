## Why

El EDA de `001/T-004` ya aporta evidencia agregada sobre la población elegible, las once clases canónicas, los duplicados y el desbalanceo, pero el corpus local todavía no dispone de un constructor de entrenamiento separado, repetible y verificable. Sin ese constructor no puede avanzarse de forma segura hacia `PG-3`, porque no hay garantía versionada de que los filtros, el mapping, las exclusiones y las huellas de narrativa se apliquen de manera idéntica en cada ejecución.

Este cambio implementará `001/T-005` y la parte constructiva de `PG-2`: transformar una fuente CFPB local en un dataset de entrenamiento local conforme al contrato vigente, sin publicar narrativas ni cerrar las decisiones que corresponden a `T-006`.

## What Changes

- Incorporar un constructor reproducible para crear un corpus local de entrenamiento a partir de una fuente CFPB disponible localmente.
- Aplicar la ventana temporal, los campos obligatorios, la normalización de etiquetas, la exclusión de la etiqueta ambigua y la política de etiquetas desconocidas definidas en `config/cfpb_target_contract.json`.
- Generar la huella de narrativa y los recuentos agregados necesarios para comprobar elegibilidad, exclusiones, clases, grupos duplicados y conflictos de target.
- Añadir validaciones y pruebas sobre muestras locales que confirmen el cumplimiento del contrato y la ausencia de persistencia de narrativas en Git, informes y logs.
- Generar únicamente artefactos locales ignorados por Git y evidencia agregada versionable.
- Mantener sin decidir la política final de idioma, la conservación o ponderación dentro de grupos duplicados, la partición final y la estrategia de desbalanceo.

### Resultados verificables

- El proceso produce un dataset local con exactamente las once etiquetas canónicas o falla explícitamente ante etiquetas no contempladas.
- Los registros de la etiqueta histórica ambigua y los grupos con targets contradictorios se excluyen y cuantifican.
- Las evidencias versionadas contienen solo métricas agregadas y no narrativas CFPB.
- El constructor se puede repetir sobre la misma fuente local con el mismo contrato y producir los mismos recuentos de control.

### Fuera de alcance

- Entrenar, evaluar o seleccionar modelos.
- Marcar `ESS-02`, `PG-2` o `PG-3` como terminados.
- Cerrar las decisiones abiertas de `001/T-006` sobre idioma, duplicados, partición, privacidad ampliada o desbalanceo.
- Exponer datos CFPB, narrativas, credenciales o artefactos locales mediante Git, informes, capturas, logs o prompts externos.
- Modificar la interfaz React, el backend, el despliegue o capacidades MLOps.

## Capabilities

### New Capabilities

- `cfpb-training-dataset`: construir y validar localmente un corpus de entrenamiento CFPB trazable al contrato de target, con evidencia agregada y controles de privacidad.

### Modified Capabilities

- Ninguna. Este cambio no altera requisitos vigentes de `complaint-routing-interface`, `jira-work-tracking`, `openspec-governance` ni `repository-presentation-quality`.

## Impact

- **Nivel de entrega:** contribuye a `ESS-02` y prepara el prerrequisito de datos para `ESS-01`, pero no verifica ninguno de esos criterios por sí solo.
- **Código y configuración previstos:** constructor de datos, configuración existente `config/cfpb_target_contract.json`, pruebas de contrato y documentación/evidencias agregadas.
- **Datos:** la fuente y el dataset resultante permanecen locales e ignorados por Git; no se añade ningún dato bruto ni narrativa al repositorio.
- **Seguridad y privacidad:** se preservan las restricciones de narrativa, logs e informes del contrato vigente; cualquier ampliación de persistencia requerirá una decisión posterior.

## Tracking

- Jira: `PG-2`.
- Expediente de compatibilidad: `specs/001-cfpb-target-contract/`, tarea `T-005`.
