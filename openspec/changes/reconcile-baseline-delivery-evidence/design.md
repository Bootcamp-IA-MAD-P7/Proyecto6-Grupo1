## Context

La PR #31 fusionó el baseline `TF-IDF + LogisticRegression` y archivó el cambio
`train-cfpb-baseline`. Sus informes versionados registran macro F1 train de
`0.6455`, macro F1 validation de `0.5973`, gap de `0.0482`, accuracy en
validation y test protegido, y métricas por clase. Sin embargo, la
documentación conserva estados anteriores a la fusión y una interpretación
demasiado fuerte del resultado de test.

El cambio afecta a las fuentes de estado y presentación, no al pipeline ni a
los datos locales. El destinatario es el equipo, la evaluación del bootcamp y
NotebookLM; por tanto, debe poder distinguir evidencia de ML, límites del
prototipo y trabajo pendiente.

## Goals / Non-Goals

**Goals:**

- Alinear la documentación con PR #31, Jira `PG-3`, el OpenSpec archivado y los
  informes de baseline.
- Marcar `ESS-03`, `ESS-05` y `ESS-06` como `Verificado` si las evidencias
  versionadas satisfacen literalmente sus mínimos; mantener los demás estados
  conservadores.
- Corregir la explicación estadística del test y mantener visibles las clases
  débiles y limitaciones.
- Regenerar las fuentes seguras de NotebookLM sin datos ni narrativas reales.

**Non-Goals:**

- Reentrenar, ajustar hiperparámetros, repetir el test protegido o alterar sus
  resultados.
- Declarar `ESS-01`, `ESS-02`, `ESS-04` o `ESS-07` a `ESS-10` terminados.
- Modificar scripts, corpus, modelo binario, interfaz, backend, CI, Jira o
  infraestructura.

## Decisions

### Verificar únicamente criterios con evidencia mínima literal

`ESS-03` se actualizará a `Verificado`: el informe registra la misma métrica
macro F1 en train y validation y un gap absoluto de `0.0482`, inferior a
`0.05`. `ESS-05` y `ESS-06` se actualizarán a `Verificado`: las métricas
agregadas y por clase están en informes JSON versionados para validation y test
protegido, con configuración, semilla y contrato referenciables.

`ESS-01` seguirá `En curso`: existe un pipeline funcional y un artefacto local
ignorado por Git, pero aún falta la decisión de versionado o manifiesto
verificable del artefacto de modelo. `ESS-02` conservará su estado hasta cerrar
el conjunto completo de conclusiones de EDA. Los criterios de matriz de
confusión, importancia de variables y análisis de errores no se actualizarán
porque no disponen todavía de su evidencia mínima.

Alternativa descartada: mantener todos los criterios en curso hasta completar
el nivel esencial. Se descarta porque contradice la definición del propio
contrato: cada criterio puede verificarse individualmente con evidencia
reproducible.

### Interpretar el test como evaluación final, no como prueba causal

El control de sobreajuste se atribuirá exclusivamente al gap train/validation.
El test protegido se describirá como evaluación final one-shot; que su macro
F1 sea mayor que validation es una observación compatible con una partición
temporal distinta, no una prueba de que validation sea necesariamente más
difícil ni de ausencia de sobreajuste.

Alternativa descartada: eliminar los valores de test. Se conserva la evidencia
porque es útil y se declara su alcance de forma correcta.

### Mantener trazabilidad sin versionar datos ni binarios sensibles

Las referencias a datos y modelo enlazarán código, configuración, informe,
particiones agregadas y PR, pero no añadirán corpus, narrativas ni
`models/cfpb_baseline.pkl` al repositorio. La futura tarea de empaquetado o
servicio decidirá la procedencia del artefacto para `ESS-01`.

## Risks / Trade-offs

- [Los estados se perciben como demasiado conservadores] → El contrato de
  niveles explica qué evidencia falta para cada criterio no verificado.
- [El test se use para seleccionar de nuevo modelos] → La documentación
  conservará su condición one-shot y prohibirá reutilizarlo para tuning.
- [Las fuentes de presentación prometan una aplicación completa] → NotebookLM
  mantendrá separados baseline, PWA mock y backend pendiente.

## Migration Plan

1. Actualizar informes y documentación de estado en una única rama documental.
2. Ejecutar comprobaciones ligeras de calidad, diff y OpenSpec.
3. Regenerar el paquete de NotebookLM.
4. Revisar humanamente la PR; si se revierte, restaurar el commit documental
   sin tocar la PR #31 ni los artefactos del baseline.

## Open Questions

- Qué formato de manifiesto o registro del artefacto local permitirá verificar
  `ESS-01` antes de integrarlo en el backend.
- Si las clases débiles requieren mínimos por clase antes de seleccionar un
  modelo para integración.
