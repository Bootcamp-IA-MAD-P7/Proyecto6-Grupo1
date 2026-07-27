## ADDED Requirements

### Requirement: Contexto operativo vigente para personas e IAs

El contexto operativo distribuido mediante `AGENTS.md`, documentación de
equipo, guía de Jira y el arnés MUST reflejar el estado integrado más reciente
de las tareas, responsables y bloqueos relevantes. Los expedientes heredados
MUST conservarse como compatibilidad, pero MUST NOT prevalecer sobre un cambio
OpenSpec archivado, una PR fusionada o un estado Jira confirmado.

#### Scenario: Hito heredado cerrado

- **WHEN** una tarea heredada queda cerrada con evidencia y su Jira asociado se
  encuentra en el estado confirmado de finalización
- **THEN** el contexto operativo dejará de presentarla como trabajo activo y
  señalará el siguiente hito que corresponda

#### Scenario: Generación de contexto por el arnés

- **WHEN** una persona genera un paquete de inicio para una IA tras actualizar
  el repositorio
- **THEN** el paquete utilizará referencias vigentes y no indicará tareas o
  bloqueos que ya no describen el estado integrado
