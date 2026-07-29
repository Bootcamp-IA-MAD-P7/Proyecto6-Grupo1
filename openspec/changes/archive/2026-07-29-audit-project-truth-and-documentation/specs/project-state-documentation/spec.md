## ADDED Requirements

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
