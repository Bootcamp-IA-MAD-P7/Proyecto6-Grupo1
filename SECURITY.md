# Política de seguridad

## Reporte responsable

No publiques vulnerabilidades, credenciales o datos sensibles en Issues, Pull Requests, dailies o capturas.

Comunica el hallazgo de forma privada al equipo y registra públicamente únicamente la corrección cuando sea seguro hacerlo. El canal privado se documentará cuando el equipo acuerde la herramienta de coordinación.

## Alcance inicial

- Secretos y configuración.
- Dependencias.
- Datos y privacidad.
- API e inputs de usuario.
- Artefactos de modelos.
- Contenedores y cloud.
- Automatizaciones y permisos de GitHub.

## Reglas mínimas

- No versionar `.env`, claves, tokens, contraseñas o cadenas de conexión.
- No incluir datos personales en logs o fixtures sin anonimización.
- Validar entradas en los límites del sistema.
- Utilizar permisos mínimos en workflows y despliegues.
- Revisar dependencias y actualizar vulnerabilidades conocidas.
- Verificar origen, integridad y compatibilidad de artefactos de modelo.
- No promocionar modelos sin evidencia, backup y rollback.
