# mvp-presentation-documentation Specification
## Purpose

Mantener una presentación del MVP que comience con el problema y el valor para
la persona usuaria, y que distinga una demostración local de un producto
desplegado.
## Requirements
### Requirement: README de MVP verificable

El README SHALL ofrecer una lectura inicial que conecte problema, usuario,
recorrido local, arquitectura, evidencia, seguridad, escalabilidad y límites,
sin duplicar informes detallados ni afirmar capacidades no implementadas.

#### Scenario: Evaluador nuevo

- **WHEN** una persona abre el repositorio sin conocer el proyecto
- **THEN** puede localizar cómo ejecutar la demo local, qué evidencia sostiene el nivel esencial y qué capacidades siguen fuera de alcance

### Requirement: Narrativa de presentación orientada a cliente

Las fuentes de NotebookLM SHALL comenzar por el problema de clasificación y el
valor de una recomendación revisable, y solo después explicar métricas,
arquitectura, seguridad y escalabilidad. SHALL distinguir la demo local de un
producto desplegado.

#### Scenario: Presentación generada

- **WHEN** NotebookLM usa las fuentes catalogadas del proyecto
- **THEN** puede construir una narrativa que no expone narrativas CFPB ni sitúa el proceso técnico antes de la necesidad del cliente

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
