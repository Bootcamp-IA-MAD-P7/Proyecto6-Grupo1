## ADDED Requirements

### Requirement: Runbook local distinguible

El repositorio SHALL ofrecer una guía local que diferencie el recorrido mock
seguro del recorrido de inferencia local real, usando únicamente texto
sintético y sin presentar ninguno como despliegue.

#### Scenario: Revisión rápida en modo mock
- **WHEN** una persona sigue el recorrido mock sin URL de API configurada
- **THEN** puede iniciar la interfaz y reconocer que la respuesta es sintética

#### Scenario: Inferencia local disponible
- **WHEN** una persona dispone del artefacto local y configura el origen local
permitido
- **THEN** puede iniciar backend y frontend, comprobar `GET /api/v1/health` y
distinguir una respuesta real de un fallback mock

### Requirement: Operación local segura y recuperable

La guía SHALL declarar rutas, puertos, variables y límites de seguridad
relevantes, e incluir una recuperación proporcional para un proceso anterior o
una caché PWA de desarrollo sin pedir que se borren datos del proyecto.

#### Scenario: Puerto o caché anterior
- **WHEN** un proceso local o un recurso PWA anterior impide revisar la versión
actual
- **THEN** la guía ofrece una comprobación sencilla y reversible antes de pasos
avanzados de navegador
