# Hechos verificados del proyecto

> Este documento se completará únicamente con información respaldada por el repositorio.

## Identidad del producto

- Nombre: pendiente.
- Problema de negocio: apoyar la clasificación y el enrutamiento de reclamaciones financieras escritas.
- Usuario principal: personal de operaciones o atención al cliente; el flujo concreto debe validarse mediante `003/T-005`.
- Resultado esperado: sugerir una familia de producto con confianza opcional, alternativas y revisión humana. El mapping a colas no está validado ni incluido en la primera versión.

## Equipo y responsabilidades

- Miguel: arquitectura y coherencia transversal.
- José: backend; revisión del contrato y futura integración cuando se levanten los bloqueantes.
- Abel: frontend y UX; responsable operativo de `003/T-008` y la PR #14.
- Víctor: datos y EDA; responsable de estudiar el CSV bajo `001/T-004`.
- Josué: fuera del equipo desde el 22 de julio de 2026.
- Jira: comienzo previsto el 23 de julio; enlace pendiente de creación.

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

- Aplicación: React PWA implementada en la PR #14 contra un mock explícito y el OpenAPI `0.1.0`. Incluye formulario, resultado, alternativas, revisión humana, errores y shell offline; no está conectada a un modelo ni backend. La PR continúa en borrador mientras Abel completa `003/T-008`.
- Despliegue: pendiente.
- Persistencia: pendiente.
- Estado MLOps: pendiente.

## Regla

Cada cifra futura debe enlazar su informe, artefacto o evidencia reproducible.

La selección fue aprobada por José, Abel, Víctor y Miguel el 22 de julio de 2026. La viabilidad preliminar, el contrato de datos y la PWA mock tienen evidencias propias; todavía no equivalen a un modelo validado, inferencia real o impacto comercial demostrado.
