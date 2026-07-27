# Hechos verificados del proyecto

> Este documento se completará únicamente con información respaldada por el repositorio.

## Identidad del producto

- Nombre: pendiente.
- Problema de negocio: apoyar la clasificación y el enrutamiento de reclamaciones financieras escritas.
- Usuario principal: personal de operaciones o atención al cliente; el flujo concreto debe validarse en la siguiente spec.
- Resultado esperado: predecir una familia de producto y proponer una cola configurable, con confianza, alternativas y revisión humana.

## Datos

- Dataset: Consumer Complaint Database del CFPB, viable con condiciones según el spike reproducible.
- Fuente y condiciones: fuente oficial pública del CFPB; la página permite usar, analizar y construir sobre los datos publicados, pero las condiciones exactas del tratamiento y reutilización de narrativas se revisarán antes de una explotación comercial.
- Número de observaciones: 2.306.723 reclamaciones con narrativa en la ventana `[2023-08-24, 2026-07-23)`, según probe de la API del 22 de julio de 2026. Las variables de modelado definitivas siguen pendientes.
- Target y clases: `product` como origen y `product_canonical` como target derivado. El contrato `1.0` conserva once familias, normaliza dos etiquetas históricas equivalentes y excluye 111 registros de `Credit card or prepaid card` por ambigüedad.
- Desbalanceo: la etiqueta mayoritaria contiene 1.671.242 observaciones, el 72,45 % del total.
- Calidad preliminar: una muestra temporal de 1.000 registros contiene cero IDs repetidos, 122 narrativas exactamente duplicadas y cuatro señales heurísticas de URL; no es una muestra aleatoria.
- Contrato del EDA: única entrada candidata `complaint_what_happened`; resultados agregados y ninguna narrativa real en Git, informes o NotebookLM.
- EDA incorporado mediante la PR #24: notebook reproducible, conversor CSV→Parquet, cuatro figuras agregadas e informe `reports/validation/cfpb_eda.md`.
- Hallazgos del EDA: 2.272.802 filas canónicas en el informe, mayoría del 73,5 %, 171.426 grupos de narrativas duplicadas, 1.744 grupos conflictivos y 98,6 % de inglés en una muestra de 5.000.
- Constructor local de entrenamiento candidato: el 27 de julio se generaron 1.998.570 filas tras aplicar el contrato y excluir 273.831 filas de 1.744 grupos conflictivos. La fuente de esa ejecución tiene SHA-256 `f1cb8b412f6af5039ae630b3d0a1e4b5eab93be900a247ae60ea33cea073b351`; es una instantánea distinta de la usada por el informe EDA, por lo que los recuentos no se mezclan. Véase `reports/validation/cfpb_training_dataset.md`.
- Preparación aprobada del baseline: 1.961.073 filas clasificadas como inglés con `langdetect 1.0.9`, semilla `0` y máximo de 500 caracteres; 37.497 filas quedan fuera por idioma no inglés o no clasificable. Las particiones locales contienen 1.372.751 filas de train, 294.161 de validation y 294.161 de test protegido. Todas las clases superan 100 filas en validation y test. Véase `reports/validation/cfpb_training_preparation.md`.

## Modelo

- Baseline: pendiente.
- Champion: pendiente.
- Métrica principal del baseline: macro F1; accuracy, métricas por clase y F1 weighted serán complementarias.
- Política inicial de desbalanceo: `class_weight="balanced"`, sin re-muestreo; todavía no se ha entrenado ni evaluado un modelo.
- Resultados finales: pendiente.

## Producto y operación

- Aplicación: prototipo React PWA incorporado, validado y fusionado mediante la
  PR #25, con revisión humana completada. Permite
  revisar con texto sintético el formulario, dictado, respuesta mock, revisión
  humana, instalación y shell offline. No existe backend, modelo ni inferencia
  real, por lo que `ESS-04` continúa sin verificar. La necesidad de una
  evolución nativa se evaluará después de cubrir el alcance web instalable.
- Despliegue: pendiente.
- Persistencia: pendiente.
- Estado MLOps: pendiente.

## Regla

Cada cifra futura debe enlazar su informe, artefacto o evidencia reproducible.

La selección fue aprobada por José, Abel, Víctor y Miguel el 22 de julio de 2026. No equivale a un dataset validado ni a una capacidad implementada.
