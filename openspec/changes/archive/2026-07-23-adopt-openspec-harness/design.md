## Context

El repositorio empezó a trabajar con specs numeradas antes de adoptar OpenSpec. Esas carpetas contienen contratos, planes, decisiones, tareas activas y evidencias que ya utilizan Víctor y Abel. Paralelamente se construyó un arnés propio que valida rol, spec y tarea y genera un paquete Markdown seguro para cualquier IA.

La referencia LIDR Specboot utiliza OpenSpec como motor SDD y añade reglas, agentes, skills, verificaciones y conexiones opcionales con Jira. Instalar OpenSpec sin integrarlo produciría una herramienta vacía; copiar las specs existentes a una segunda jerarquía produciría dos fuentes de verdad.

El equipo utiliza Windows y Git Bash o PowerShell, distintas herramientas de IA y un repositorio protegido mediante Pull Requests y CI. La integración debe ser reproducible, independiente de una instalación global y compatible con el trabajo que ya está en curso.

## Goals / Non-Goals

**Goals:**

- Utilizar OpenSpec real como ciclo de vida obligatorio para todos los cambios nuevos.
- Fijar una versión común y reproducible para equipo y CI.
- Conectar OpenSpec con el contexto, los roles, los límites y las comprobaciones existentes.
- Mantener temporalmente compatibles las tareas numeradas ya asignadas.
- Proporcionar comandos sencillos y diagnósticos comprensibles.
- Validar estructura y requisitos OpenSpec automáticamente.

**Non-Goals:**

- Reescribir ahora el EDA de Víctor o las decisiones frontend de Abel.
- Migrar mecánicamente documentos sin revisar su semántica.
- Sustituir Jira, Git, las Pull Requests o la revisión humana.
- Enviar datos, narrativas, secretos o artefactos a OpenSpec o a una IA.
- Añadir backend, modelo, despliegue o MLOps.

## Decisions

### OpenSpec será una dependencia local exacta

Se utilizará `@fission-ai/openspec` `1.6.0` en `devDependencies`, con `package-lock.json` y Node.js `>=20.19.0`.

Alternativas consideradas:

1. Instalación global individual: sencilla, pero permite versiones diferentes.
2. `npx @latest` en cada ejecución: no reproducible y dependiente de red.
3. Dependencia local exacta: misma versión para personas y CI.

Se adopta la opción 3. Los comandos se ejecutarán mediante `npx openspec` o scripts npm, sin exigir una instalación global.

### OpenSpec gestionará los cambios nuevos

`openspec/specs/` representará el estado vigente de las capacidades archivadas y `openspec/changes/` contendrá propuestas activas. Cada cambio seguirá el esquema oficial:

```text
proposal → specs + design → tasks → apply → verify → archive
```

Las carpetas numeradas de `specs/` seguirán siendo expedientes de compatibilidad para tareas abiertas antes de la adopción. No se crearán nuevas specs numeradas. Cuando Abel o Víctor entreguen cambios basados en sus manuales actuales, se adaptarán mediante un cambio OpenSpec antes de integrarlos.

Alternativas consideradas:

1. Migrar y renombrar todo inmediatamente: rompe rutas y manuales activos.
2. Mantener ambas jerarquías indefinidamente: crea dos fuentes de verdad.
3. Congelar la jerarquía numerada para compatibilidad y migrar por cambios revisados.

Se adopta la opción 3.

### El arnés ampliará OpenSpec, no lo imitará

OpenSpec proporcionará propuesta, requisitos, diseño, tareas, estado, instrucciones, validación y archivo. El arnés seguirá aportando:

- selección de rol;
- contexto del briefing y del proyecto;
- límites de seguridad;
- compatibilidad con tareas numeradas abiertas;
- procedimientos `start`, `verify`, `review` y `prepare-pr`;
- salida Markdown segura para herramientas sin acceso al repositorio.

El modo OpenSpec del arnés invocará el CLI local y utilizará su salida JSON real. No reconstruirá el estado de los artefactos.

### Las integraciones generadas son adaptadores

OpenSpec genera skills y comandos para Codex, Copilot, Claude, Cursor y Gemini. Esos archivos pueden repetirse por herramienta porque son adaptadores gestionados por el CLI; no contienen requisitos de producto. `AGENTS.md`, `openspec/config.yaml`, `openspec/`, `docs/` y `ai-specs/` conservan las fuentes comunes.

### La privacidad prevalece sobre la telemetría opcional

El arnés y CI ejecutarán OpenSpec con `OPENSPEC_TELEMETRY=0`. La guía explicará cómo desactivarla también para comandos directos. Según la documentación oficial, la telemetría solo recoge comando y versión, pero el proyecto opta por minimizar conexiones no necesarias.

### CI validará OpenSpec como puerta de calidad

`repository-quality` instalará las dependencias raíz con `npm ci` y ejecutará:

```text
npm run openspec:doctor
npm run openspec:validate
```

La suite Python cubrirá resolución del CLI, errores, cambios inexistentes, bloqueos y composición del contexto.

## Risks / Trade-offs

- [Dos jerarquías durante la transición] → congelar `specs/` para nuevas iniciativas, documentar el límite y migrar cada entrega mediante OpenSpec.
- [Más archivos generados] → tratarlos como adaptadores oficiales actualizables, no como documentación manual.
- [Node.js para perfiles de datos o backend] → proporcionar un único `npm ci`, diagnóstico claro y versión mínima.
- [Cambios de formato al archivar] → validar de forma estricta antes del archive y revisar el diff resultante.
- [Dependencia externa] → fijar versión y conservar la posibilidad de retirar paquete, `openspec/` y adaptadores sin borrar contratos históricos.
- [Telemetría opcional] → desactivarla desde arnés y CI y documentar la preferencia del proyecto.

## Migration Plan

1. Instalar e inicializar OpenSpec de forma local y reproducible.
2. Registrar esta adopción como el primer cambio OpenSpec.
3. Configurar contexto y reglas del proyecto.
4. Extender el arnés y sus tests.
5. Añadir doctor y validación estricta a CI.
6. Actualizar la spec `004`, guías, README y fuentes de presentación.
7. Completar y archivar `adopt-openspec-harness`, creando la primera spec vigente.
8. Utilizar OpenSpec para Jira, seguridad, NotebookLM y todos los cambios posteriores.
9. Adaptar las entregas preexistentes de Víctor y Abel antes de integrarlas.

Rollback:

- revertir la Pull Request;
- eliminar la dependencia y los adaptadores generados;
- conservar `specs/`, `docs/`, `ai-specs/` y el historial Git;
- el arnés anterior seguirá siendo recuperable desde el commit previo.

## Open Questions

- La selección del proyecto y clave Jira se resolverá en un cambio OpenSpec posterior.
- La fecha de retirada definitiva de la jerarquía numerada dependerá del cierre de las tareas activas de Víctor y Abel.
