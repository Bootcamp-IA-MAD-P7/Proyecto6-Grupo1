## ADDED Requirements

### Requirement: Comunicación de privacidad y disponibilidad del servicio local

ClaimVox SHALL comunicar de forma accesible cuándo el servicio local no está disponible, cuándo limita solicitudes y qué datos no conserva. SHALL NOT añadir identidad, analítica persistente ni almacenamiento de narrativas para mostrar esos estados.

#### Scenario: Servicio limitado o no disponible

- **WHEN** la API devuelve una respuesta `429` o no está disponible
- **THEN** la interfaz muestra una acción de recuperación comprensible y mantiene la narrativa fuera de URL, logs, almacenamiento y mensajes de error
