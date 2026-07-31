## ADDED Requirements

### Requirement: Gráfico activo derivado del corte auditado

El gráfico de entrega activo MUST identificar la fecha y el SHA del corte,
MUST representar los conteos derivados de los 25 criterios canónicos y MUST
mantener los SVG anteriores como cortes históricos no activos.

#### Scenario: Cambio de estado con evidencia nueva

- **WHEN** la auditoría cambia el estado verificable de uno o más criterios
- **THEN** se genera un nuevo SVG fechado, accesible y coherente con
  `delivery_levels.md`, y todas las fuentes activas enlazan ese SVG

### Requirement: Resumen profesional sin sobreafirmaciones

README, guía de presentación y fuentes NotebookLM MUST describir de forma
consistente las capacidades locales, contenerizadas, compartidas y desplegadas,
y MUST NOT usar una capacidad de una capa como evidencia automática de otra.

#### Scenario: Docker y base compartida sin evidencia cloud

- **WHEN** existen imágenes reproducibles y persistencia PostgreSQL verificadas
  localmente pero no existe smoke cloud versionado
- **THEN** la documentación puede acreditar contenerización y base integrada,
  pero mantiene el despliegue cloud como pendiente
