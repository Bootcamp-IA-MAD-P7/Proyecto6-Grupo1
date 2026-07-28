## ADDED Requirements

### Requirement: Informe técnico esencial reproducible

El proyecto SHALL mantener un informe técnico que conecte la fuente de datos,
contrato de clases, preparación, evaluación, artefacto local, métricas,
diagnósticos, límites y pasos de ejecución de la PWA y el servicio local.

#### Scenario: Consulta de la entrega esencial

- **WHEN** una persona evaluadora consulta el informe técnico y la guía
- **THEN** podrá localizar comandos, informes, figuras, limitaciones y el estado
  real de cada criterio esencial sin necesitar datos CFPB ni conocimientos
  implícitos del equipo

### Requirement: Comunicación precisa de madurez

El informe SHALL diferenciar el modelo local evaluado, la integración local de
ClaimVox, las capacidades mock y las capacidades no implementadas, incluidos
despliegue, persistencia, autenticación y MLOps.

#### Scenario: Lectura de la sección operativa

- **WHEN** la guía describe cómo ejecutar la solución
- **THEN** declarará explícitamente que el flujo es local y requiere revisión
  humana, sin presentarlo como servicio desplegado o producto productivo
