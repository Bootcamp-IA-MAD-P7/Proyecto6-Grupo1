# Atributos de calidad

## Seguridad

- Mínimo privilegio.
- Secretos fuera del repositorio.
- Validación en límites de entrada.
- Dependencias y artefactos trazables.
- Datos sensibles minimizados y protegidos.

## Escalabilidad

- Componentes desacoplados.
- Inferencia sin estado cuando sea viable.
- Persistencia y trabajos pesados separables.
- Límites y paginación en operaciones de datos.

## Mantenibilidad

- Dependencias dirigidas hacia el dominio.
- Configuración tipada y documentada.
- Tests por capa y contratos explícitos.
- Decisiones registradas mediante ADR.

## Fiabilidad

- Health y readiness diferenciados.
- Timeouts y errores controlados.
- Migraciones y rollback.
- Backups antes de promociones o cambios de esquema.

## Observabilidad

- Logs estructurados sin payloads sensibles.
- Correlación de solicitudes y predicciones.
- Métricas de servicio, datos y modelo separadas.
- Alertas accionables con propietario.

## Usabilidad

- Flujos centrados en tareas.
- Accesibilidad y responsive.
- Explicaciones multiclase comprensibles.
- Estados vacíos, carga, error y baja confianza.
