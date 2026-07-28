## ADDED Requirements

### Requirement: Corte de MVP trazable

El proyecto SHALL definir un corte anotado `v0.1.0-essential-mvp` únicamente después de que una revisión humana confirme que `ESS-01` a `ESS-10` siguen verificados en `dev` y que las comprobaciones obligatorias han pasado.

#### Scenario: Creación del tag

- **WHEN** la PR de madurez se haya fusionado y la revisión humana haya confirmado la evidencia
- **THEN** el tag anotado referirá un commit de `dev`, enlazará la evidencia de entrega y declarará que el alcance es local, revisable y no desplegado

### Requirement: Backlog posterior gobernado

El repositorio SHALL mantener un mapa único hacia Jira para los criterios no verificados, con responsable, dependencia, estado, OpenSpec asociado y evidencia mínima. El mapa SHALL diferenciar planificación de implementación.

#### Scenario: Criterio pendiente consultado

- **WHEN** una persona consulta un criterio no verificado del briefing
- **THEN** puede localizar su elemento Jira, dependencia, cambio OpenSpec o condición de inicio sin que el estado de Jira se presente como evidencia suficiente
