# Revisión manual: usabilidad de clasificación local

Fecha: `2026-07-29`

Cambio OpenSpec: `improve-local-classification-usability`

## Recorrido confirmado

Se revisó localmente el recorrido público de ClaimVox con texto sintético:

- La cabecera identifica el prototipo de clasificación local y no ofrece inicio
  de sesión mock ni administración como capacidad operativa.
- La clasificación muestra una respuesta solicitada a la API local, clase,
  confianza disponible, versión de modelo y revisión humana obligatoria.
- La presentación limita alternativas a tres y conserva un motivo seguro de
  revisión cuando el contrato no entrega razones.
- El reinicio devuelve al formulario sin retener el texto mostrado.

## Límites

La revisión no acredita autenticación, administración operativa, persistencia,
base compartida, despliegue ni decisión automática. El recorrido no usa
narrativas CFPB reales.
