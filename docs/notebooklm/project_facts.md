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

## Modelo

- Baseline: pendiente.
- Champion: pendiente.
- Métrica principal: pendiente.
- Resultados finales: pendiente.

## Producto y operación

- Aplicación: React PWA como dirección frontend inicial; todavía no implementada. Existe un flujo y OpenAPI `0.1.0` contract-only para mocks. La necesidad de una evolución nativa se evaluará después de cubrir el alcance web instalable.
- Despliegue: pendiente.
- Persistencia: pendiente.
- Estado MLOps: pendiente.

## Regla

Cada cifra futura debe enlazar su informe, artefacto o evidencia reproducible.

La selección fue aprobada por José, Abel, Víctor y Miguel el 22 de julio de 2026. No equivale a un dataset validado ni a una capacidad implementada.
