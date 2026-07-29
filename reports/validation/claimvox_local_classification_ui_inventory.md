# Inventario: clasificación local de ClaimVox

Fecha: `2026-07-29`

Cambio OpenSpec: `improve-local-classification-usability`

## Campos contractuales ya consumidos

La pantalla consume `predicted_class`, `confidence`, `alternatives`,
`review_required`, `review_reasons`, `model_version`, `taxonomy_version`,
`prediction_id` y `warnings`. No recibe ni muestra la narrativa después de
enviar la solicitud.

## Estados ya implementados

- Validación de narrativa vacía y de longitud máxima.
- Estado de envío que deshabilita el formulario y evita dobles envíos.
- Mensajes recuperables para conexión, límite de frecuencia, validación y
  respuesta contractual inválida.
- Reinicio explícito del resultado y foco accesible en el encabezado.

## Ajustes necesarios

- El modo del cliente configurado (`local_api` o `mock`) se descarta antes de
  renderizar; la interfaz infiere mock solo mediante `model_version`.
- Las alternativas se muestran sin límite, aunque la respuesta puede contener
  las diez clases restantes.
- Si `review_reasons` está vacío, la tarjeta de revisión queda sin motivo.
- La clasificación ya mantiene separada la administración conceptual, pero esta
  no debe utilizarse como evidencia del flujo funcional.

No contiene narrativas CFPB reales ni acredita despliegue, administración
operativa, autenticación o una decisión automática.
