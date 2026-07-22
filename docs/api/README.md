# Contratos de aplicación

## Contrato disponible

[`openapi.json`](openapi.json) define el contrato `0.1.0` para mocks de la React PWA y una futura integración de inferencia.

Estado: `contract-only`. No existe todavía un servicio desplegado.

El contrato incluye:

- predicción puntual desde una narrativa;
- once clases sincronizadas con `config/cfpb_target_contract.json`;
- confianza opcional y revisión explícita;
- versión de modelo y taxonomía;
- errores seguros de validación, frecuencia e indisponibilidad;
- health check sin información sensible.

No incluye feedback, historial, persistencia de narrativas ni mapping a colas.
