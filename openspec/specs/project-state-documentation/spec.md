# project-state-documentation Specification
## Purpose

Mantener una documentación operativa y de presentación que refleje el estado
integrado del proyecto, preserve la trazabilidad y no convierta propuestas o
mocks en capacidades no verificadas.
## Requirements
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

### Requirement: Estado de entrega y backlog coherentes

La documentación de estado SHALL mantener coherentes README, niveles de entrega,
AGENTS, changelog, Jira y fuentes NotebookLM. Un criterio solo podrá presentarse
como verificado si enlaza evidencia reproducible; un criterio planificado SHALL
mostrar su dependencia y estado sin convertirse en una afirmación de entrega.

#### Scenario: Actualización tras un corte de MVP

- **WHEN** se prepara una release local del MVP
- **THEN** los documentos principales muestran el mismo conteo de criterios, el mismo alcance local y el mismo mapa de trabajo pendiente

### Requirement: Fuente canónica de estado y recursos activos fechados

La documentación activa SHALL identificar
`docs/project_management/delivery_levels.md` como la fuente canónica del estado
de los criterios de entrega. Todo resumen visual activo SHALL reflejar ese
documento, incluir una fecha de corte coherente con su contenido, representar
por nivel la distribución de criterios verificados, en curso y no iniciados, y
usar una ruta que no sugiera un corte distinto. README, catálogo NotebookLM y
guion de presentación SHALL enlazar exclusivamente el recurso visual activo.

#### Scenario: Consulta del estado del briefing

- **WHEN** una persona consulta el README o una fuente activa de presentación
- **THEN** encuentra un gráfico con la misma fecha y recuento que
  `delivery_levels.md`, incluida la distribución por nivel de cada estado, y
  puede localizar la tabla canónica sin inferir estado desde otro documento

### Requirement: Conservación explícita de documentación histórica

La documentación activa SHALL distinguir las fuentes canónicas de los
expedientes históricos. Los cambios OpenSpec archivados, los expedientes de
compatibilidad bajo `specs/`, las dailies e informes puntuales SHALL conservar
su contexto de fecha y MUST NOT reescribirse para representar el estado actual.

#### Scenario: Documento con estado anterior

- **WHEN** un lector encuentra una daily, informe o cambio archivado con un
  estado anterior
- **THEN** las fuentes activas le indican que consulte
  `delivery_levels.md` para el estado vigente sin eliminar ni alterar la
  evidencia histórica

### Requirement: Auditoría de afirmaciones activas contra evidencia

La documentación activa MUST presentar como implementada o verificada una
capacidad únicamente cuando exista código o evidencia versionada en la rama
integrada. Las ramas no fusionadas, los archivos locales no versionados y las
ejecuciones fallidas MUST NOT utilizarse como evidencia de entrega.

#### Scenario: Resultado existente solo fuera de la rama integrada

- **WHEN** una rama no fusionada o un archivo local contiene un resultado que
  no está presente en `dev`
- **THEN** README, niveles de entrega y fuentes NotebookLM no lo presentan como
  capacidad o criterio verificado

#### Scenario: Capacidad local con alcance limitado

- **WHEN** existe evidencia versionada de una capacidad ejecutada solo en local
- **THEN** la documentación la describe como local y conserva explícitamente
  pendientes autenticación, operación compartida, despliegue y MLOps cuando
  correspondan

### Requirement: Inventario documental profesional y navegable

El README y el catálogo de fuentes MUST proporcionar rutas directas desde cada
afirmación principal hasta su contrato, evidencia o guía canónica, evitando
lenguaje publicitario y duplicación de fuentes de verdad.

#### Scenario: Persona revisora busca la evidencia de un criterio

- **WHEN** una persona consulta el estado resumido del proyecto
- **THEN** puede localizar la fuente canónica del criterio y su evidencia sin
  depender de mensajes, ramas experimentales o conocimiento oral
