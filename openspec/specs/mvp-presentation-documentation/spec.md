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
