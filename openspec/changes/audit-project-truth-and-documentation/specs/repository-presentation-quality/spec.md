## ADDED Requirements

### Requirement: Recuento automático del estado de entrega

La comprobación de calidad del repositorio MUST derivar de
`docs/project_management/delivery_levels.md` los criterios `ESS`, `MED`, `ADV`
y `EXP`, comprobar que los 25 identificadores son únicos y validar que el
gráfico activo declara los mismos conteos por estado y nivel.

#### Scenario: Resumen visual desactualizado

- **WHEN** un criterio cambia de `En curso` a `Verificado` sin regenerar el
  gráfico activo
- **THEN** la comprobación de calidad falla e identifica la divergencia

#### Scenario: Tabla canónica incompleta o duplicada

- **WHEN** falta uno de los 25 identificadores esperados o aparece duplicado
- **THEN** la comprobación de calidad falla antes de integrar la documentación

### Requirement: Un único gráfico de estado activo

README, catálogo de activos, fuentes NotebookLM y guion de presentación MUST
enlazar el mismo gráfico de estado vigente y MUST conservar los gráficos
anteriores únicamente como cortes históricos no activos.

#### Scenario: Publicación de un nuevo corte

- **WHEN** se actualiza el estado canónico de los niveles de entrega
- **THEN** las fuentes activas enlazan el nuevo recurso fechado y el catálogo
  identifica el anterior como histórico
