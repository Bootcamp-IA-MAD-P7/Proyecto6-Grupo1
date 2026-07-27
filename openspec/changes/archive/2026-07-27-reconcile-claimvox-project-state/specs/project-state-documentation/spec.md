## ADDED Requirements

### Requirement: Estado integrado documentado y trazable

El repositorio MUST mantener alineados el README, el contexto operativo, la
guía de equipo, la daily, el changelog y las fuentes de NotebookLM cuando una
Pull Request fusionada cambie de forma verificable el estado, la identidad o
los límites de una capacidad integrada. La actualización MUST enlazar o
nombrar la evidencia GitHub, el elemento Jira y el cambio OpenSpec relevantes
sin sustituirlos por texto narrativo.

#### Scenario: Pull Request integrada cambia el estado visible

- **WHEN** una Pull Request fusionada modifica de forma verificable la identidad
  o el comportamiento visible de una capacidad
- **THEN** la documentación afectada reflejará la nueva situación y conservará
  sus límites, trazabilidad y estado de entrega reales

#### Scenario: Información no confirmada

- **WHEN** una prueba, decisión, métrica, asignación o estado no pueda
  confirmarse mediante evidencia versionada o Jira
- **THEN** la documentación no lo presentará como realizado y lo mantendrá como
  pendiente, propuesto o no aplicable según corresponda

### Requirement: Daily equilibrada y fiel a las responsabilidades

Cada daily MUST separar las aportaciones de las personas activas y distinguir
entre contribución completada, coordinación, responsabilidad vigente,
preparación y bloqueo. La daily MUST NOT atribuir trabajo, pruebas o decisiones
a una persona que no pueda justificarse con la actividad conocida del proyecto.

#### Scenario: Actividad distribuida entre áreas

- **WHEN** una intervención afecta frontend, datos, arquitectura y backend en
  distinto grado
- **THEN** la daily describirá el estado de cada área sin inventar equivalencia
  de volumen ni ocultar bloqueos reales

### Requirement: Paquete de NotebookLM con narrativa separada del gobierno

Las fuentes de NotebookLM MUST conservar una separación entre la narrativa para
cliente, los hechos verificados y el contexto técnico interno. Una identidad
visual integrada puede aparecer en la narrativa de producto, pero MUST NOT
presentarse como modelo, servicio operativo o resultado de ML si solo existe un
prototipo.

#### Scenario: Presentación de un prototipo visual

- **WHEN** el paquete de NotebookLM incluya una interfaz integrada con datos o
  respuestas sintéticas
- **THEN** describirá el recorrido y su valor potencial sin afirmar inferencia,
  autenticación, administración, despliegue o métricas no existentes
