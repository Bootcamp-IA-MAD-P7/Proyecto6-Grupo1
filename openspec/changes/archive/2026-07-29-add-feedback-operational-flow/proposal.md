## Why

ClaimVox ya puede clasificar localmente y `PG-14` conserva feedback minimizado
en un almacén SQLite local, pero no existe una operación explícita para que una
persona registre su revisión ni para consultar sus resultados agregados. Sin
esa frontera, `MED-04` y `MED-05` no pueden demostrar un ciclo de feedback
trazable y privado.

## What Changes

- Añadir un flujo local explícito y posterior a la predicción para registrar
  feedback humano conforme a la política versionada de PG-14.
- Exponer únicamente un resumen local agregado por versión de modelo, clase
  sugerida y decisión; no se expondrán registros individuales ni contenido de
  entrada.
- Integrar en ClaimVox controles de revisión con vocabularios cerrados y
  estados de éxito o error seguros.
- Definir la frontera de una futura recolección para reentrenamiento: candidatos
  trazables y sujetos a revisión posterior, sin incorporar datos ni entrenar
  automáticamente.

## Capabilities

### New Capabilities

- `governed-feedback-operational-flow`: registro local validado, resumen
  agregado y frontera de recolección de feedback para revisión humana.

### Modified Capabilities

- `complaint-routing-interface`: la interfaz de resultado incorpora una acción
  explícita de feedback local y comunica sus límites de privacidad sin cambiar
  la predicción ni convertir la recomendación en una decisión automática.

## Impact

- Jira: `PG-13`; contribuye a `MED-04` y `MED-05`, sin verificarlos por
  anticipado.
- Áreas previstas: contrato OpenAPI local, esquema y servicio FastAPI,
  repositorio SQLite local ya aprobado, cliente y componentes React, pruebas
  sintéticas e informes agregados.
- No introduce autenticación, permisos reales, base compartida, identidad,
  almacenamiento de narrativas, Docker, despliegue, MLOps, Champion ni
  reentrenamiento automático.

## Tracking

- Jira: `PG-13`.
