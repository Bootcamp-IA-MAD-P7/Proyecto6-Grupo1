## ADDED Requirements

### Requirement: OpenSpec reproducible en el repositorio

El repositorio MUST fijar una versión exacta de OpenSpec y una versión mínima de Node.js para que todas las personas y CI ejecuten el mismo motor SDD sin instalación global.

#### Scenario: Preparación de un clon nuevo

- **WHEN** una persona clona el repositorio y ejecuta `npm ci`
- **THEN** el CLI local de OpenSpec queda disponible con la versión fijada
- **AND** `npm run openspec:doctor` puede comprobar la raíz del proyecto

### Requirement: Ciclo OpenSpec para cambios nuevos

Todo cambio nuevo relevante MUST comenzar en `openspec/changes/` y completar los artefactos exigidos por su esquema antes de aplicar tareas.

#### Scenario: Propuesta antes de implementación

- **WHEN** se solicita una nueva funcionalidad, cambio arquitectónico, automatización o modificación de contrato
- **THEN** se crea un cambio OpenSpec con propuesta, delta de requisitos, diseño cuando corresponda y tareas
- **AND** no comienza la implementación mientras el estado de OpenSpec indique artefactos bloqueados

### Requirement: Estado vigente y propuestas separados

OpenSpec MUST mantener las capacidades vigentes en `openspec/specs/` y las modificaciones propuestas en `openspec/changes/`.

#### Scenario: Archivo de un cambio verificado

- **WHEN** todas las tareas y verificaciones de un cambio están completadas
- **THEN** el cambio se valida de forma estricta y se archiva
- **AND** su delta actualiza la spec vigente correspondiente

### Requirement: Compatibilidad controlada con expedientes numerados

El repositorio MUST conservar temporalmente las carpetas numeradas existentes de `specs/` para las tareas ya asignadas, pero MUST NOT crear nuevas iniciativas en esa jerarquía.

#### Scenario: Entrega basada en un manual anterior

- **WHEN** llega trabajo de una tarea numerada abierta antes de OpenSpec
- **THEN** se revisa contra su expediente original
- **AND** se crea o actualiza un cambio OpenSpec antes de integrar su nueva capacidad en `dev`

### Requirement: Contexto común y sin duplicación

OpenSpec MUST utilizar el contexto versionado de `AGENTS.md`, `.specify/intent.md`, `docs/`, contratos y `ai-specs/` sin copiar requisitos de producto dentro de los roles o skills.

#### Scenario: Generación de instrucciones

- **WHEN** OpenSpec genera instrucciones para un artefacto o para aplicar tareas
- **THEN** incluye las reglas de producto, entrega, seguridad y evidencia definidas en `openspec/config.yaml`
- **AND** mantiene `ai-specs/` limitado a roles y procedimientos

### Requirement: Arnés compuesto sobre el CLI real

El arnés MUST obtener el estado y las instrucciones de los cambios mediante la salida estructurada del CLI OpenSpec local en lugar de reconstruir su ciclo de vida.

#### Scenario: Inicio de un cambio OpenSpec

- **WHEN** una persona inicia trabajo mediante el arnés y proporciona un identificador de cambio
- **THEN** el arnés consulta `openspec status` e `openspec instructions`
- **AND** genera un paquete que conserva el estado, los artefactos y las restricciones reales

### Requirement: Validación local y en CI

La salud y la validación estricta de OpenSpec MUST formar parte de las comprobaciones locales y del workflow obligatorio del repositorio.

#### Scenario: Pull Request con un requisito inválido

- **WHEN** una Pull Request contiene una spec OpenSpec sin escenario válido o con estructura incorrecta
- **THEN** `repository-quality` falla
- **AND** el cambio no puede fusionarse hasta corregir la spec

### Requirement: Protección de datos y secretos

OpenSpec, el arnés y sus adaptadores MUST NOT incluir datasets, narrativas CFPB, secretos, credenciales, modelos, artefactos locales ni logs sensibles.

#### Scenario: Contexto permitido para una IA

- **WHEN** se genera un paquete de trabajo desde OpenSpec y el arnés
- **THEN** solo contiene documentación y contratos permitidos
- **AND** la telemetría se desactiva en las ejecuciones automatizadas del proyecto

### Requirement: Compatibilidad con múltiples asistentes

El repositorio MUST proporcionar adaptadores oficiales de OpenSpec para Codex, GitHub Copilot, Claude Code, Cursor y Gemini CLI sin convertirlos en fuentes de verdad independientes.

#### Scenario: Cambio de herramienta de IA

- **WHEN** una persona utiliza cualquiera de los asistentes configurados
- **THEN** dispone del flujo OpenSpec correspondiente
- **AND** todos los asistentes consumen el mismo cambio, configuración y contexto versionado

### Requirement: Diagnóstico comprensible

El proyecto MUST proporcionar una comprobación sencilla que informe si faltan Node.js, dependencias, OpenSpec, configuración o artefactos obligatorios.

#### Scenario: Entorno incompleto

- **WHEN** una persona ejecuta el diagnóstico en un clon sin dependencias instaladas
- **THEN** recibe una explicación concreta y una acción correctiva
- **AND** no se genera un paquete parcial que aparente ser válido
