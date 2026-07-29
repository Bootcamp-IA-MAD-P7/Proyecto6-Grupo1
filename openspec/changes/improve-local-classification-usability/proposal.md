# Propuesta: mejorar la usabilidad de clasificación local

## Contexto

ClaimVox ya puede consumir una predicción local real cuando la PWA se configura
contra FastAPI, pero el resultado mezcla señales de modelo, mock y revisión
humana de forma difícil de interpretar. La vista de administración es un
concepto aislado y no debe confundirse con el recorrido funcional de
clasificación.

## Objetivo

Hacer comprensible el flujo local de clasificación sin cambiar la identidad
visual, el modelo, el backend, los contratos públicos ni la arquitectura de
despliegue. La persona usuaria debe distinguir claramente una predicción local
real de una respuesta mock y entender qué decisión sigue requiriendo revisión
humana.

## Alcance propuesto

- Mejorar la jerarquía y los estados del formulario y resultado de clasificación.
- Mostrar fuente, versión, confianza, alternativas limitadas y revisión humana
  solo con datos presentes en el contrato de respuesta.
- Sustituir listas extensas de clases por un máximo de tres alternativas
  relevantes.
- Mantener visible una razón de revisión segura cuando el contrato no aporte
  una razón textual.
- Mantener las rutas administrativas conceptuales fuera del flujo funcional de
  clasificación.
- Añadir pruebas directas y evidencia de recorrido local con texto sintético.

## Fuera de alcance

- Cambiar el modelo, entrenamiento, métricas, API, contratos, CORS, Docker,
  despliegue, autenticación, permisos, base de datos o feedback.
- Convertir la administración conceptual en un panel operativo.
- Presentar una respuesta mock como predicción de modelo o incorporar
  narrativas CFPB reales.

## Éxito y trazabilidad

- La PWA comunica sin ambigüedad estado de carga, error, mock o API local.
- Una respuesta real muestra clase, confianza, versión y revisión humana de
  forma legible; una mock conserva sus avisos explícitos.
- La evidencia usa solo texto sintético y no acredita despliegue ni operación
  productiva.

## Tracking

- Jira: `PG-18`.
