## Why

La comparación ensemble verificó alternativas sobre una muestra, pero no puede
seleccionar un modelo definitivo porque los gaps de overfitting superan el 5 % y
no existe todavía validación cruzada estratificada sobre el protocolo aprobado.
PG-11 convierte la selección posterior en una decisión reproducible, sin usar
el test protegido para ajustar ni elegir.

## Tracking

- Jira: `PG-11`.
- Criterios afectados: `MED-02` y `MED-03`. No modifica el estado de ningún
  criterio hasta que exista evidencia reproducible revisada.

## What Changes

- Definir el protocolo gobernado de validación cruzada estratificada,
  configuraciones, semillas, presupuesto de ejecución y resultados por fold.
- Ejecutar la optimización de hiperparámetros solo sobre los datos permitidos,
  con macro F1 como métrica primaria y controles explícitos de overfitting.
- Registrar una decisión de candidato basada en criterios establecidos antes de
  consultar el test protegido, incluyendo variabilidad, coste y limitaciones.
- Producir evidencias agregadas y reproducibles sin versionar narrativas, datos
  pesados ni artefactos de modelo.

No se cambia la partición aprobada, la política de idioma, la prevención de
leakage, el contrato de once clases, la API, ClaimVox ni el uso protegido del
test. No se implementa un Champion desplegado, feedback, base de datos,
persistencia, Docker, cloud ni MLOps.

## Capabilities

### New Capabilities

- `governed-model-selection`: protocolo reproducible para comparar y elegir un
  candidato multiclase mediante validación cruzada y optimización sin contaminar
  el test protegido.

### Modified Capabilities

- Ninguna. El baseline vigente conserva su evidencia y contrato; este cambio
  añade el proceso de selección posterior.

## Impact

- Código de entrenamiento y optimización ya existente, limitado al alcance de
  evaluación de PG-11.
- Pruebas unitarias directamente relacionadas y reportes agregados de CV y
  búsqueda.
- Documentación de decisiones y evidencia de modelo solo cuando los resultados
  reales estén disponibles.
- Riesgo de privacidad bajo: no se incluirán narrativas CFPB, datos brutos,
  credenciales ni binarios en Git, informes o prompts.
