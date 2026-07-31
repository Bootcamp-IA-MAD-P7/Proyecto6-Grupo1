## Context

El corte auditado parte de `origin/dev` en
`1366ef202cbabe45a1c53a96d57e6284e690993a`. Los commits recientes incorporan
Docker, PostgreSQL y estado operativo en el Dashboard, mientras las fuentes
activas todavía describen esas capacidades como inexistentes. También existen
ramas históricas y cambios OpenSpec activos que no deben confundirse con la
rama integrada.

La auditoría cruza Git/GitHub, código, contratos, tests, evidencias,
documentación, NotebookLM y activos gráficos. Los destinatarios son el equipo,
las personas evaluadoras y quienes preparan la presentación.

Restricciones:

- no entrenar, retunar ni ejecutar CV;
- no procesar narrativas reales;
- no publicar, fusionar, archivar ni tocar `main`;
- no usar archivos locales sin seguimiento como evidencia;
- no acreditar cloud, operación productiva o MLOps sin evidencia mínima;
- preservar documentos históricos fechados.

## Goals / Non-Goals

**Goals:**

- establecer un inventario reproducible de lo contenido en `dev`;
- verificar aplicación, contratos, Docker y persistencia con pruebas locales;
- reconciliar criterios, documentación, NotebookLM y gráfico activo;
- corregir inconsistencias seguras dentro del alcance;
- registrar comandos, resultados, límites y pendientes en una evidencia final.

**Non-Goals:**

- decidir un Champion o cerrar selección de modelo;
- producir una ejecución ML nueva;
- desplegar o modificar infraestructura;
- convertir pruebas locales en evidencia cloud;
- reescribir dailies, archivos OpenSpec archivados o informes históricos;
- gestionar ramas remotas.

## Decisions

### D1. `origin/dev` es la única base de capacidad integrada

Solo se consideran implementadas las capacidades contenidas en el SHA auditado.
Las ramas no contenidas se inventarían y clasificarán, pero no alterarán los
estados de entrega.

Alternativa descartada: deducir el estado desde ramas recientes o Jira. No
garantiza integración ni verificación.

### D2. Los criterios se actualizan por evidencia mínima

Cada transición se contrasta con el contrato de
`docs/project_management/delivery_levels.md`. Docker y PostgreSQL solo podrán
verificar `ADV-01`/`ADV-02` si código, configuración, pruebas y guía
reproducible satisfacen sus mínimos. `ADV-03` requiere evidencia cloud
versionada adicional y no se infiere de archivos Docker.

Alternativa descartada: conservar recuentos antiguos pese a evidencia nueva.
Produciría documentación falsa.

### D3. Verificación local con fixtures sintéticos

Se ejecutarán suites existentes, builds, quality gates y comprobaciones Docker
que no requieran datos reales. El baseline local puede inspeccionarse y usarse
en smoke seguro si el artefacto existe; su binario no se versionará.

Alternativa descartada: entrenamiento o narrativas CFPB, fuera de alcance y de
la frontera de privacidad.

### D4. Un único corte gráfico activo

El gráfico fechado `2026-07-31` se derivará del estado canónico y será la única
referencia activa. Los SVG anteriores seguirán versionados como históricos.

Alternativa descartada: sobrescribir el SVG anterior, porque perdería el
contexto histórico.

### D5. Documentación por fuente de verdad

README resume; `delivery_levels.md` gobierna criterios; las evidencias registran
comprobaciones; NotebookLM separa hechos, estado técnico y narrativa; OpenSpec
conserva el cambio. Se actualizarán solo documentos activos cuyo significado
cambie.

Alternativa descartada: duplicar todos los detalles en cada documento, lo que
aumenta contradicciones.

## Security

- Buscar secretos por patrones sin imprimir valores sensibles.
- Mantener credenciales y variables reales fuera de Git.
- Usar datos y payloads sintéticos.
- Confirmar que feedback y Dashboard exponen únicamente agregados permitidos.
- No abrir puertos, modificar recursos cloud ni contactar servicios de
  despliegue.

## Testing

- `python scripts/harness.py doctor`
- suites unitarias y de contrato Python;
- pruebas directas de predicción, feedback y persistencia;
- quality gates de datos, modelo, métricas y repositorio;
- type-check, lint, formato, tests y build frontend;
- comprobaciones Docker/Compose disponibles sin desplegar;
- validación OpenSpec estricta del cambio y del conjunto;
- validación XML/accesibilidad del SVG;
- `git diff --check`.

## Documentation Impact

Se revisarán README, AGENTS, intent, changelog, guías operativas, niveles,
presentación, fuentes NotebookLM, catálogos de activos y evidencia final. Las
dailies e informes históricos no se reescribirán; solo se creará una daily
nueva si existe actividad verificable de esta intervención.

## Risks / Trade-offs

- [Ramas antiguas contienen trabajo no integrado] → clasificarlas con commits y
  PRs, sin fusionarlas.
- [Docker disponible pero daemon ausente] → distinguir revisión estática,
  build y ejecución; no verificar lo que no se ejecute.
- [PostgreSQL implementado pero sin migración/privilegios suficientes] →
  contrastar esquema, inicialización, configuración y pruebas antes de cambiar
  `ADV-02`.
- [Despliegue externo no visible desde el repositorio] → mantener `ADV-03` sin
  verificar y pedir URL, smoke, secretos protegidos y rollback.
- [Gráfico divergente] → derivar sus conteos de la tabla canónica y ejecutar el
  quality gate.
- [Auditoría extensa introduce cambios editoriales] → limitar ediciones a
  afirmaciones contradictorias o fuentes activas afectadas.

## Migration Plan

1. Auditar el SHA y producir inventarios.
2. Ejecutar verificaciones funcionales y de infraestructura local.
3. Reconciliar criterios con evidencia.
4. Actualizar fuentes activas y generar gráfico/evidencia.
5. Ejecutar la batería final.

Rollback: descartar la rama de auditoría. No se modifican datos, servicios
externos ni ramas remotas.

## Open Questions

- ¿Existe evidencia versionada de un despliegue AWS con smoke y rollback?
  Hasta encontrarla, `ADV-03` permanece sin verificar.
- ¿Las ramas de PG-11 contienen resultados válidos no integrados? Solo una
  revisión humana posterior puede decidir su cierre o eliminación.
