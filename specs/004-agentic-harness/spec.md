# SPEC: Arnés agéntico de trabajo

- ID: `004`
- Estado: `in_progress`
- Responsable: `Miguel / arquitectura y coordinación`
- Fecha: `2026-07-23`

## Contexto y problema

El repositorio ya conserva instrucciones, specs, tareas, decisiones, comprobaciones y un generador de contexto independiente de la herramienta de IA. Sin embargo, una persona todavía debe localizar varias piezas, redactar instrucciones y recordar manualmente cómo iniciar, verificar, revisar y publicar cada tarea.

El equipo necesita una capa agéntica ligera que conecte esas piezas sin sustituirlas ni duplicarlas. Debe ayudar a que distintas IA trabajen con el mismo rol, alcance y ciclo de retroalimentación, manteniendo siempre la revisión humana.

## Usuario y necesidad

Como integrante del equipo, quiero seleccionar mi rol, spec y tarea y obtener unas instrucciones completas y verificables para mi IA, de modo que pueda avanzar con un método común sin aprender toda la arquitectura documental ni depender de una herramienta concreta.

## Objetivo observable

Convertir el flujo actual en un ciclo guiado y repetible:

```text
repositorio clonado o actualizado
    -> tarea elegida
    -> contexto y rol preparados
    -> trabajo limitado por la spec
    -> verificaciones ejecutadas
    -> revisión del cambio
    -> descripción de PR preparada
    -> evidencias registradas
```

## Alcance

### Incluido

- Definir roles agénticos para arquitectura, datos, backend y frontend.
- Definir procedimientos reutilizables para iniciar, verificar, revisar y preparar una Pull Request.
- Generar un único paquete Markdown con rol, spec, tarea, límites y verificaciones.
- Reutilizar `AGENTS.md`, las specs y `build_ai_handoff.py` como fuentes de verdad.
- Permitir que cada integrante obtenga todo el contexto desde su propio clon sin depender de otra persona.
- Incluir el contrato de niveles de entrega en todo contexto generado.
- Añadir validaciones automáticas para evitar referencias rotas, tareas inexistentes y contenido inseguro.
- Probar el flujo con una tarea real y activa del EDA, sin modificar su resultado científico.
- Documentar un manual breve, independiente de la IA utilizada.

### Fuera de alcance

- Adoptar Specboot u OpenSpec sin una evaluación posterior.
- Crear una segunda jerarquía de specs o reemplazar `.specify/` y `specs/`.
- Implementar frontend, backend, modelos, EDA o infraestructura de producción.
- Permitir que una IA haga merge, publique o cierre decisiones sin revisión humana.
- Enviar narrativas CFPB, secretos, datos brutos o artefactos sensibles a herramientas externas.
- Añadir agentes autónomos que trabajen sin una tarea aprobada.

## Escenarios

### Principal

1. Una persona clona o actualiza `dev` y crea una rama.
2. Consulta en el repositorio su rol, la spec y la tarea asignada.
3. Si su IA accede al repositorio, abre la raíz y utiliza las fuentes directamente.
4. Si no accede, ejecuta por sí misma un único comando del arnés y genera un Markdown local.
5. La IA explica alcance, archivos, requisitos del briefing y bloqueantes antes de modificar nada.
6. Tras el trabajo, la persona ejecuta la verificación y revisa el diff.
7. El arnés ayuda a preparar la descripción de la Pull Request y las evidencias de cierre.

### Alternativos y errores

1. Si el rol, la spec o la tarea no existen, el proceso falla con un mensaje claro y no genera un paquete parcial.
2. Si la tarea está bloqueada, el paquete lo indica y no autoriza su implementación.
3. Si una fuente contiene rutas prohibidas o datos no aptos para una IA externa, la generación se detiene.
4. Si una comprobación falla, la tarea no se presenta como terminada ni se prepara como lista para merge.
5. Si la IA tiene acceso directo al repositorio, puede usar las mismas instrucciones sin depender de un proveedor concreto.

## Requisitos

- R-001: El arnés debe reutilizar la jerarquía documental actual y evitar una segunda fuente de verdad.
- R-002: El uso debe ser independiente del proveedor, editor y modelo de IA.
- R-003: Cada ejecución debe identificar un rol, una spec y una tarea existentes.
- R-004: El paquete debe distinguir objetivo, alcance, prohibiciones, bloqueantes, archivos previstos y comprobaciones.
- R-005: Los roles deben aportar límites de responsabilidad, no permisos para ignorar dependencias o decisiones.
- R-006: Los procedimientos de inicio, verificación, revisión y PR deben ser pequeños, componibles y legibles.
- R-007: La salida compartible debe ser un único Markdown generado en `exports/`, fuera del control de versiones.
- R-008: Ninguna salida debe incluir datos brutos, narrativas CFPB, secretos, modelos ni artefactos locales.
- R-009: Una tarea bloqueada o inexistente no debe producir instrucciones de implementación válidas.
- R-010: Las comprobaciones del arnés deben poder ejecutarse localmente y en CI.
- R-011: La persona responsable debe conservar el control sobre decisiones, diff, publicación y merge.
- R-012: El piloto debe usar una tarea real sin alterar su contenido, estado ni resultado esperado.
- R-013: Todo contexto debe incluir la intención y el contrato verificable de niveles de entrega.
- R-014: El flujo debe poder iniciarse desde un clon actualizado sin recibir archivos preparados por otra persona.

## Criterios de aceptación

- AC-001: Dado un rol, una spec y una tarea válidos, cuando se inicia el flujo, entonces se genera un único Markdown con el contexto necesario para trabajar.
- AC-002: Dada una tarea bloqueada, inexistente o ajena a la spec, cuando se intenta iniciar, entonces el comando falla de forma explícita.
- AC-003: Dado un paquete generado, cuando se revisa, entonces sus instrucciones coinciden con `AGENTS.md`, la spec, el plan, las tareas y las decisiones vigentes.
- AC-004: Dada cualquier IA capaz de leer Markdown, cuando recibe el paquete, entonces puede explicar qué debe hacer, qué no debe hacer y cómo comprobarlo.
- AC-005: Dado un cambio local, cuando se ejecuta la verificación, entonces se informa de cada comprobación y no se ocultan fallos.
- AC-006: Dado un cambio verificado, cuando se prepara la Pull Request, entonces se obtiene contenido compatible con la plantilla oficial sin inventar evidencias.
- AC-007: Dado el piloto sobre `001/T-004`, cuando se completa la demostración, entonces el flujo queda probado sin modificar el EDA ni marcar la tarea como completada.
- AC-008: Dado el repositorio en CI, cuando se altera una definición del arnés, entonces se validan referencias, seguridad y tests.
- AC-009: Dada una persona nueva, cuando lee el manual breve, entonces puede completar el flujo sin conocer Specboot, OpenSpec ni terminología agéntica.
- AC-010: Dado un paquete generado, cuando se inspeccionan sus fuentes, entonces incluye `.specify/intent.md` y `docs/project_management/delivery_levels.md`.
- AC-011: Dado un integrante con acceso a Git, cuando clona o actualiza el repositorio, entonces puede localizar su asignación y preparar el contexto sin intermediarios.

## Requisitos no funcionales

- Ejecución reproducible en Windows y en GitHub Actions.
- Mensajes de error breves y accionables.
- Sin dependencia obligatoria de servicios de pago ni credenciales.
- Configuración legible y versionada.
- Compatibilidad con el flujo Git y los quality gates existentes.
- Diseño mínimo: cada archivo nuevo debe tener una responsabilidad clara.

## Preguntas abiertas

- [x] Q-001: Se crea `scripts/harness.py` como entrada y se reutiliza `build_ai_handoff.py` mediante parámetros opcionales compatibles con su contrato anterior.
- [x] Q-002: Se adopta una acción posicional y opciones explícitas, compatibles con PowerShell y Git Bash.
- [ ] Q-003: ¿La adaptación futura a Specboot u OpenSpec aportará valor suficiente para justificar una migración?

Estas preguntas afectan a la implementación interna, pero no bloquean la definición ni el piloto del flujo.

## Evidencia de cierre esperada

- Roles y procedimientos versionados, validados y documentados.
- Tests unitarios de referencias, estados y límites de seguridad.
- Paquete de demostración generado para `data-analyst`, `001-cfpb-target-contract` y `T-004`.
- Ejecución correcta de los quality gates locales y de CI.
- Manual breve probado por al menos una persona distinta de quien lo implementa.
- Pull Request con evidencias reales y decisiones registradas.
