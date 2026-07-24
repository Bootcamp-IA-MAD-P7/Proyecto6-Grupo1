## MODIFIED Requirements

### Requirement: Ciclo OpenSpec para cambios nuevos

Todo cambio nuevo relevante MUST comenzar en `openspec/changes/`, completar los artefactos exigidos por su esquema y enlazar su elemento Jira antes de aplicar tareas, salvo una excepción explícita de bootstrap, emergencia o automatización.

#### Scenario: Propuesta antes de implementación

- **WHEN** se solicita una nueva funcionalidad, cambio arquitectónico, automatización o modificación de contrato
- **THEN** se crea un cambio OpenSpec con propuesta, delta de requisitos, diseño cuando corresponda y tareas
- **AND** se enlaza la clave Jira después de aprobar el desglose operativo
- **AND** no comienza la implementación mientras el estado de OpenSpec indique artefactos bloqueados o falte tracking sin excepción
