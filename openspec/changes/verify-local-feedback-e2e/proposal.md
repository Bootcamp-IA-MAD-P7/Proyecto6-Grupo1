## Why

El flujo local de feedback ya tiene contrato, persistencia privada y rutas
locales, pero `MED-04` solo puede verificarse con una prueba reproducible que
conecte una predicción real con el registro permitido y su resumen agregado.

## What Changes

- Definir una verificación local extremo a extremo, con datos sintéticos, para
  predicción local válida, registro explícito de feedback y consulta agregada.
- Exigir evidencia que demuestre la minimización de datos, la retención y la
  independencia entre feedback y predicción.
- Establecer criterios para actualizar `MED-04` únicamente si la comprobación
  local se supera; `MED-05` no se verifica con este cambio.
- Mantener fuera de alcance autenticación, permisos reales, base compartida,
  despliegue, MLOps y reentrenamiento automático.

## Capabilities

### New Capabilities

- Ninguna.

### Modified Capabilities

- `governed-feedback-operational-flow`: añadir la evidencia extrema a extremo
  requerida para afirmar que el flujo local de feedback está operativo.

## Impact

- Jira: `PG-13`.
- Afecta a la evidencia local de la API de predicción y feedback, y a los
  criterios de entrega `MED-04` y `MED-05`.
- No introduce dependencias, almacenamiento compartido, cambios de modelo ni
  contratos de datos adicionales.

## Tracking

- Jira: `PG-13`
