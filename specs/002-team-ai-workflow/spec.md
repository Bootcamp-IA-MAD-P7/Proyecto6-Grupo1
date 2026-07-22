# SPEC: Flujo de trabajo del equipo con IA

- ID: `002`
- Estado: `closed`
- Responsable: `Equipo / QA documental`
- Fecha: `2026-07-22`

## Contexto y problema

El equipo utiliza distintas herramientas de IA según la tarea. El repositorio ya contiene intent, specs, tareas y reglas Git, pero el contexto que leen los agentes ha quedado parcialmente desactualizado y no existe una forma automática de preparar el conjunto mínimo de fuentes para una IA sin acceso al repositorio.

La solución debe unificar el método, no la herramienta. Cada integrante conserva la responsabilidad sobre el alcance, la revisión y las evidencias de su trabajo.

## Objetivo observable

Permitir que cualquier integrante comience una tarea desde Jira y una spec, trabaje con una IA con o sin acceso al repositorio y cierre el cambio con las mismas reglas, sin recopilar documentos manualmente ni compartir datos sensibles.

## Alcance

### Incluido

- Contexto vigente y reglas comunes en `AGENTS.md`.
- Guía práctica en el workflow existente.
- Prompt reutilizable para iniciar y cerrar una tarea.
- Generador de un paquete Markdown por spec y tarea.
- Validación de spec, tarea, rutas, formatos y seguimiento Git.
- Registro de React PWA como dirección frontend confirmada.

### Fuera de alcance

- Obligar al equipo a utilizar una IA concreta.
- Ejecutar automáticamente código propuesto por una IA.
- Incluir datasets, secretos, narrativas o artefactos locales en los paquetes.
- Asignar roles o tareas que todavía no haya acordado el equipo.
- Sustituir Jira, las Pull Requests o la revisión humana.

## Escenario principal

1. Una persona recibe o elige una historia de Jira.
2. Identifica la spec y tarea relacionadas.
3. Si su IA accede al repositorio, abre la raíz y le indica que lea `AGENTS.md`.
4. Si no accede, genera un paquete acotado mediante el script del proyecto.
5. La IA propone alcance y archivos antes de editar.
6. La persona revisa, verifica y publica mediante Pull Request.
7. Tareas, decisiones y documentación se actualizan solo cuando cambian.

## Requisitos

- R-001: Las instrucciones deben ser independientes de proveedor, editor o modelo.
- R-002: El estado confirmado debe distinguirse de las decisiones abiertas.
- R-003: El paquete debe incluir reglas comunes, README, contribución y el bundle completo de la spec.
- R-004: La tarea solicitada debe existir en `tasks.md`.
- R-005: Los `--include` solo pueden ser archivos documentales versionados dentro del repositorio.
- R-006: La salida debe generarse en `exports/`, fuera de Git.
- R-007: Ningún paquete debe incluir datos brutos, secretos, notebooks, modelos o narrativas.
- R-008: El workflow debe explicar responsabilidades, inicio, verificación y cierre.
- R-009: La decisión React PWA debe constar como dirección confirmada, sin presentar aplicación ni arquitectura nativa como implementadas.

## Criterios de aceptación

- AC-001: Dada una spec y tarea válidas, cuando se genera el paquete, entonces contiene las fuentes comunes, cuatro archivos de la spec y configuraciones JSON referenciadas.
- AC-002: Dada una tarea inexistente, cuando se solicita el paquete, entonces el comando falla con un mensaje claro.
- AC-003: Dada una ruta externa, no versionada o con formato no permitido, cuando se añade con `--include`, entonces el comando la rechaza.
- AC-004: Dada una IA con acceso al repositorio, cuando recibe el prompt común, entonces puede identificar spec, tarea, límites y verificaciones sin un paquete adicional.
- AC-005: Dada una persona nueva, cuando lee el workflow, entonces puede completar el ciclo rama, trabajo, verificación y PR.
- AC-006: Dado el estado actual, cuando un agente lea `AGENTS.md`, entonces no tratará idea, dataset, target o React PWA como decisiones pendientes.

## Evidencia de cierre esperada

- Generador probado con `001-cfpb-target-contract/T-004`.
- Tests de generación y rechazo de entradas inválidas.
- Paquete de ejemplo generado fuera de Git.
- Instrucciones, estado técnico y fuentes de NotebookLM sincronizados.
