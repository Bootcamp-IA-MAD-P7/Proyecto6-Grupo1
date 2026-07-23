## ADDED Requirements

### Requirement: Identificadores de entrega legibles

El README MUST presentar cada identificador visible de los niveles `ESS`, `MED`, `ADV` y `EXP` como una unidad no separable, sin cambiar su nomenclatura canónica.

#### Scenario: Tabla renderizada en una columna estrecha

- **WHEN** un visor Markdown reduce el ancho disponible para la tabla
- **THEN** el identificador completo permanece en una sola línea
- **AND** el criterio, estado y evidencia siguen en columnas independientes

### Requirement: Activos SVG documentales accesibles

Cada SVG versionado bajo `docs/assets/` MUST ser XML válido, declarar un `viewBox`, identificarse como imagen y proporcionar título y descripción accesibles.

#### Scenario: Validación de un SVG documental

- **WHEN** se ejecuta la comprobación de calidad del repositorio
- **THEN** un SVG sin `role="img"`, `viewBox`, título o descripción provoca un fallo
- **AND** el archivo debe corregirse antes de integrar la Pull Request

### Requirement: Etiquetas visuales contenidas

Las etiquetas de estado del diagrama principal MUST conservar fondos con margen interior suficiente y alineación centrada para que el texto no desborde.

#### Scenario: Etiquetas del flujo principal

- **WHEN** se renderiza el diagrama principal del README
- **THEN** `ENTRADA` y las dos etiquetas `PREVISTO` quedan centradas dentro de fondos de anchura consistente
- **AND** ninguna palabra toca ni supera el borde de su fondo

### Requirement: Estructura sin capacidades ficticias

El repositorio MUST limitar los archivos `.gitkeep` a las etapas de datos aprobadas y MUST NOT utilizar árboles placeholder para representar capacidades todavía no implementadas.

#### Scenario: Placeholder fuera de las etapas de datos

- **WHEN** la comprobación del repositorio encuentra un `.gitkeep` fuera de las rutas permitidas
- **THEN** la comprobación falla
- **AND** la carpeta futura solo podrá añadirse cuando contenga implementación o evidencia real

### Requirement: Estado documental veraz

Una revisión de presentación o estructura MUST NOT modificar el estado de un criterio del briefing sin evidencia mínima versionada.

#### Scenario: Cierre de una revisión documental

- **WHEN** se actualizan README, diagramas o tablas de entrega
- **THEN** los recuentos y estados coinciden con `docs/project_management/delivery_levels.md`
- **AND** mocks, contratos y documentos no se presentan como producto, modelo o despliegue implementado
