# Contratos de aplicación

## Contrato disponible

[`openapi.json`](openapi.json) define el contrato `0.1.0` entre ClaimVox y el
servicio de inferencia y feedback.

Estado: `local-implemented`. Existe un servicio FastAPI para ejecución local;
no existe evidencia versionada de una API pública desplegada.

El contrato incluye:

- predicción puntual desde una narrativa;
- once clases sincronizadas con `config/cfpb_target_contract.json`;
- confianza opcional y revisión explícita;
- versión de modelo y taxonomía;
- errores seguros de validación, frecuencia e indisponibilidad;
- health y estado operativo sin contenido de entrada;
- login JWT de demostración configurado mediante entorno;
- creación local de feedback minimizado después de una predicción real;
- resumen agregado por versión, clase sugerida y decisión.

No incluye historial individual, persistencia de narrativas, identidad
compartida, autorización productiva, operación multiusuario ni mapping a colas.
