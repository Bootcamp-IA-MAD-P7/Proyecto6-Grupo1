## ADDED Requirements

### Requirement: Auditoría final de la rama integrada

La documentación activa MUST derivar sus afirmaciones de capacidad del SHA
auditado de `origin/dev`, MUST identificar las Pull Requests relevantes y MUST
separar las ramas no integradas, archivos locales y ejecuciones externas no
versionadas de la evidencia de entrega.

#### Scenario: Rama con trabajo posterior no integrado

- **WHEN** una rama remota contiene commits que no son ancestros del SHA
  auditado de `origin/dev`
- **THEN** la auditoría registra la rama y su clasificación sin presentar sus
  cambios como capacidad integrada

#### Scenario: Pull Request fusionada cambia el estado

- **WHEN** código, pruebas y evidencia de una Pull Request fusionada satisfacen
  la evidencia mínima de un criterio
- **THEN** los niveles, README, NotebookLM y gráfico activo reflejan el mismo
  estado y enlazan su evidencia

### Requirement: Evidencia final reproducible y limitada

La auditoría MUST registrar SHA, comandos, resultados, capacidades, criterios,
documentos actualizados, riesgos y pendientes en un informe agregado. El
informe MUST NOT contener narrativas, datos brutos, credenciales, modelos,
resultados por fila ni logs sensibles.

#### Scenario: Cierre de la auditoría

- **WHEN** finalizan las verificaciones acordadas
- **THEN** una persona revisora puede reproducir las comprobaciones y distinguir
  hechos integrados, límites locales y capacidades pendientes desde el informe
  final

### Requirement: Paquete NotebookLM apto para presentación

Las fuentes activas de NotebookLM MUST separar hechos verificados, resultados
históricos, estado técnico actual, decisiones, límites y trabajo pendiente, y
MUST proporcionar rutas exactas a las fuentes canónicas y evidencias.

#### Scenario: Generación de una presentación

- **WHEN** NotebookLM utiliza el paquete activo
- **THEN** puede explicar el problema, la arquitectura, las métricas, el estado
  de entrega y los límites sin convertir Docker local, una rama o una intención
  en despliegue productivo
