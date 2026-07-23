## MODIFIED Requirements

### Requirement: Etiquetas visuales contenidas

Las etiquetas de estado del diagrama principal MUST usar fondos de al menos 120 unidades de anchura, conservar alineación centrada y ofrecer una separación visual inequívoca para que el texto no toque ni desborde sus bordes con la tipografía del documento.

#### Scenario: Etiquetas del flujo principal

- **WHEN** se renderiza el diagrama principal del README
- **THEN** `ENTRADA` y las dos etiquetas `PREVISTO` quedan centradas dentro de fondos de al menos 120 unidades
- **AND** ninguna palabra toca ni supera el borde de su fondo
