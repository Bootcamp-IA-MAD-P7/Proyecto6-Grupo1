## ADDED Requirements

### Requirement: Ruta ejecutiva verificable en el README

El README SHALL permitir que una persona nueva localice, sin recorrer documentos
internos, el problema, el valor, una prueba local de cinco minutos, el estado del
MVP, las evidencias esenciales, los límites, la arquitectura actual y el camino
de evolución. SHALL enlazar las fuentes canónicas y no sustituirlas.

#### Scenario: Evaluador sin contexto previo

- **WHEN** una persona abre el README sin conocer ClaimVox
- **THEN** puede identificar cómo probar el recorrido local con texto sintético, qué criterios están verificados y qué sigue fuera de alcance

### Requirement: Presentación honesta de evidencia y evolución

El README SHALL separar la arquitectura local implementada de la evolución
planificada y SHALL presentar métricas, seguridad, privacidad y escalabilidad
solo con enlaces a evidencia versionada. SHALL NOT presentar tag, PWA, API local
o roadmap como despliegue, autenticación, persistencia o MLOps.

#### Scenario: Consulta de madurez del MVP

- **WHEN** una persona consulta la sección de evidencia, arquitectura o roadmap
- **THEN** encuentra las fuentes verificables y comprende que el tag corresponde a un corte local, revisable y no desplegado
