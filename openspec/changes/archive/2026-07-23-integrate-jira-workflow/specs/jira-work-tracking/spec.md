## ADDED Requirements

### Requirement: Responsabilidades separadas

El proyecto MUST utilizar Jira para asignación y estado operativo, OpenSpec para requisitos y decisiones, y GitHub para implementación y evidencia.

#### Scenario: Cambio de estado en Jira

- **WHEN** una historia pasa de pendiente a en curso
- **THEN** Jira refleja el responsable y estado operativo
- **AND** los requisitos permanecen en OpenSpec sin copiarse ni reescribirse en el ticket

### Requirement: Jerarquía proporcional

El backlog MUST utilizar Epics para resultados amplios e Historias o Tareas para unidades de entrega, sin crear un ticket por cada requisito o comprobación interna.

#### Scenario: Conversión de una spec en backlog

- **WHEN** una propuesta OpenSpec aprobada se desglosa para Jira
- **THEN** se presenta primero un Epic y entre tres y diez tickets implementables
- **AND** el equipo confirma el desglose antes de crear elementos

### Requirement: Trazabilidad estable

Todo trabajo nuevo planificado MUST enlazar una clave Jira `PG-N`, un cambio OpenSpec y su Pull Request, o registrar una excepción explícita de bootstrap, emergencia o automatización.

#### Scenario: Inicio de implementación

- **WHEN** una persona inicia un cambio nuevo mediante el arnés
- **THEN** proporciona una clave Jira válida o una excepción permitida
- **AND** la referencia aparece en el paquete de contexto y en la Pull Request

### Requirement: Validación local sin credenciales

El arnés MUST validar el formato de la clave Jira y transportarla en el contexto sin requerir tokens, acceso de red ni secretos en el repositorio.

#### Scenario: Clon sin sesión Atlassian

- **WHEN** una persona ejecuta el arnés con `--jira PG-12`
- **THEN** la clave se valida e incluye localmente
- **AND** no se intenta acceder a Jira ni se solicita almacenar credenciales

### Requirement: Contenido seguro

Los tickets Jira MUST NOT contener narrativas CFPB, datos brutos, secretos, artefactos locales ni afirmaciones no verificadas.

#### Scenario: Historia de datos

- **WHEN** se crea una historia de EDA
- **THEN** describe análisis agregados, aceptación y enlaces versionados
- **AND** no incorpora ejemplos reales de reclamaciones

### Requirement: Backlog inicial acotado

La adopción MUST comenzar con un único Epic del nivel esencial y un máximo de diez historias o tareas aprobadas.

#### Scenario: Inicio de Jira

- **WHEN** el proyecto `PG` está vacío
- **THEN** se presenta el Epic y su desglose antes de realizar escrituras
- **AND** no se crean Epics placeholder para los niveles medio, avanzado o experto
