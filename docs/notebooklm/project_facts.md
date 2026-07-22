# Hechos verificados del proyecto

> Este documento se completará únicamente con información respaldada por el repositorio.

## Identidad del producto

- Nombre: pendiente.
- Problema de negocio: apoyar la clasificación y el enrutamiento de reclamaciones financieras escritas.
- Usuario principal: personal de operaciones o atención al cliente; el flujo concreto debe validarse en la siguiente spec.
- Resultado esperado: predecir una familia de producto y proponer una cola configurable, con confianza, alternativas y revisión humana.

## Datos

- Dataset: Consumer Complaint Database del CFPB, seleccionado como candidato y pendiente de spike de viabilidad.
- Fuente y condiciones: fuente oficial pública del CFPB; la página permite usar, analizar y construir sobre los datos publicados, pero las condiciones exactas del tratamiento y reutilización de narrativas se revisarán antes de una explotación comercial.
- Número de observaciones: 2.306.723 reclamaciones con narrativa en la ventana `[2023-08-24, 2026-07-23)`, según probe de la API del 22 de julio de 2026. Las variables de modelado definitivas siguen pendientes.
- Target y clases: `product` propuesto. La API devuelve catorce etiquetas, tres históricas o ambiguas; el contrato final pretende once familias tras aprobar su normalización.
- Desbalanceo: la etiqueta mayoritaria contiene 1.671.242 observaciones, el 72,45 % del total.
- Calidad preliminar: una muestra temporal de 1.000 registros contiene cero IDs repetidos, 122 narrativas exactamente duplicadas y cuatro señales heurísticas de URL; no es una muestra aleatoria.

## Modelo

- Baseline: pendiente.
- Champion: pendiente.
- Métrica principal: pendiente.
- Resultados finales: pendiente.

## Producto y operación

- Aplicación: pendiente.
- Despliegue: pendiente.
- Persistencia: pendiente.
- Estado MLOps: pendiente.

## Regla

Cada cifra futura debe enlazar su informe, artefacto o evidencia reproducible.

La selección fue aprobada por José, Abel, Víctor y Miguel el 22 de julio de 2026. No equivale a un dataset validado ni a una capacidad implementada.
