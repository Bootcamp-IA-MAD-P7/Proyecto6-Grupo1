# Contratos de aplicación

## Contrato disponible

[`openapi.json`](openapi.json) define el contrato `0.1.0` entre ClaimVox y el
servicio local de inferencia, y también permite el mock seguro por defecto de la
PWA.

Estado: `local-implemented`. Existe un servicio FastAPI para ejecución local;
no existe un servicio desplegado ni una API pública.

El contrato incluye:

- predicción puntual desde una narrativa;
- once clases sincronizadas con `config/cfpb_target_contract.json`;
- confianza opcional y revisión explícita;
- versión de modelo y taxonomía;
- errores seguros de validación, frecuencia e indisponibilidad;
- health check sin información sensible.
- creación local de feedback minimizado después de una predicción real;
- resumen agregado por versión, clase sugerida y decisión.

No incluye historial individual, persistencia de narrativas, identidad,
autenticación, operación compartida ni mapping a colas.
