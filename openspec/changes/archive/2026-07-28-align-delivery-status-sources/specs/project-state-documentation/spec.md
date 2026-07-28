## ADDED Requirements

### Requirement: Fuente canónica de estado y recursos activos fechados

La documentación activa SHALL identificar
`docs/project_management/delivery_levels.md` como la fuente canónica del estado
de los criterios de entrega. Todo resumen visual activo SHALL reflejar ese
documento, incluir una fecha de corte coherente con su contenido, representar
por nivel la distribución de criterios verificados, en curso y no iniciados, y
usar una ruta que no sugiera un corte distinto. README, catálogo NotebookLM y
guion de presentación SHALL enlazar exclusivamente el recurso visual activo.

#### Scenario: Consulta del estado del briefing

- **WHEN** una persona consulta el README o una fuente activa de presentación
- **THEN** encuentra un gráfico con la misma fecha y recuento que
  `delivery_levels.md`, incluida la distribución por nivel de cada estado, y
  puede localizar la tabla canónica sin inferir estado desde otro documento

### Requirement: Conservación explícita de documentación histórica

La documentación activa SHALL distinguir las fuentes canónicas de los
expedientes históricos. Los cambios OpenSpec archivados, los expedientes de
compatibilidad bajo `specs/`, las dailies e informes puntuales SHALL conservar
su contexto de fecha y MUST NOT reescribirse para representar el estado actual.

#### Scenario: Documento con estado anterior

- **WHEN** un lector encuentra una daily, informe o cambio archivado con un
  estado anterior
- **THEN** las fuentes activas le indican que consulte
  `delivery_levels.md` para el estado vigente sin eliminar ni alterar la
  evidencia histórica
