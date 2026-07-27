## Context

El informe `reports/validation/cfpb_eda.md`, generado por
`notebooks/01_eda.py`, ya contiene población, distribución de clases,
temporalidad, duplicados, longitud, idioma, nulos y desbalanceo. Sus cuatro
figuras agregadas están versionadas. Las decisiones operativas posteriores se
encuentran en `config/cfpb_training_policy.json` y en los informes de
preparación de la fuente de entrenamiento, que no es la misma instantánea que
la del EDA.

El contrato de entrega exige un análisis de correlación pertinente. Para este
caso, la única entrada candidata es una narrativa textual y el target es una
categoría; una matriz de correlación numérica no responde a una pregunta válida
del problema ni sustituye las visualizaciones específicas de clasificación.

## Goals / Non-Goals

**Goals:**

- Completar la explicación metodológica y la trazabilidad que faltan para
  evaluar `ESS-02` con la evidencia ya disponible.
- Mantener separadas las cifras de la instantánea EDA y de la preparación del
  baseline.
- Comprobar referencias a código, figuras e informes sin exponer narrativas.
- Actualizar los estados de entrega solo si la revisión confirma toda la
  evidencia mínima.

**Non-Goals:**

- Reejecutar el notebook, descargar datos, cambiar el conversor o modificar la
  política de preparación.
- Entrenar, ajustar, comparar o evaluar modelos.
- Reabrir decisiones cerradas en `T-006`, repetir el test protegido o cambiar
  el estado operativo de Jira.
- Añadir correlaciones artificiales, figuras sin utilidad para texto o casos de
  reclamación reales.

## Decisions

### Declarar la no aplicabilidad de correlación numérica

El informe documentará que no existen features numéricas de entrada cuyo
coeficiente de correlación aporte una señal útil para el modelo de texto. Las
figuras ya existentes de clase, tiempo, duplicados y longitud son las
visualizaciones pertinentes para el objetivo de clasificación.

Alternativa descartada: fabricar una matriz de correlación usando longitudes,
conteos o códigos de clase. Esa matriz sería fácil de producir, pero no
representaría relaciones entre features de inferencia y podría inducir a una
lectura errónea.

### Separar exploración y decisiones posteriores

El informe EDA conservará sus cifras y preguntas originales. Una sección de
continuidad enlazará las decisiones aprobadas posteriormente sin reescribir la
instantánea ni mezclar sus recuentos con los de entrenamiento.

Alternativa descartada: sustituir las preguntas abiertas del EDA por cifras de
la preparación posterior. Rompería la trazabilidad histórica del análisis.

### Verificar ESS-02 mediante evidencia existente

`ESS-02` solo cambiará a `Verificado` si se confirman el script reproducible,
las cuatro figuras versionadas, el informe agregado, la justificación de
visualizaciones, las conclusiones y las referencias a decisiones posteriores.

Alternativa descartada: declararlo verificado únicamente porque `PG-2` está en
Jira como listo. Jira registra estado operativo, no evidencia técnica.

## Risks / Trade-offs

- [La correlación no aplicable se interprete como una omisión] → explicitar el
  motivo metodológico y enumerar las visualizaciones pertinentes ya entregadas.
- [Se mezclen dos instantáneas de datos] → conservar los recuentos del EDA y
  enlazar la política posterior solo como continuidad, con su propia huella.
- [Se expongan narrativas al ampliar la explicación] → limitar todos los
  documentos a resultados agregados, rutas y configuraciones.
- [El cierre documental oculte carencias de otros criterios] → actualizar solo
  `ESS-02` y mantener sin cambios los estados de modelo, integración y análisis
  posterior.

## Migration Plan

1. Revisar y actualizar exclusivamente documentos de evidencia y estado.
2. Ejecutar las comprobaciones ligeras de repositorio y OpenSpec.
3. Regenerar el paquete NotebookLM.
4. Presentar los cambios para revisión humana mediante Pull Request.

La reversión consiste en revertir el commit documental; no hay artefactos de
datos, modelos ni migraciones que revertir.

## Open Questions

- Ninguna para el cierre de `ESS-02`. La cobertura multilingüe posterior sigue
  siendo una decisión de modelado futura y no impide documentar el EDA actual.
