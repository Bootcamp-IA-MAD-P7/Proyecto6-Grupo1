# Capa agéntica del proyecto

Esta carpeta convierte las reglas y specs del repositorio en instrucciones reutilizables para distintas herramientas de IA.

No contiene una segunda versión del proyecto. Las fuentes de verdad continúan siendo:

1. `AGENTS.md`, para las reglas comunes;
2. `.specify/intent.md`, para el propósito y los límites globales;
3. `specs/<spec>/`, para el alcance, el plan, las tareas y las decisiones;
4. los contratos y documentos enlazados desde la spec activa.

## Qué contiene

```text
ai-specs/
├── agents/       # Responsabilidad y límites de cada rol
└── skills/       # Procedimientos reutilizables para el ciclo de trabajo
```

Un agente es una ficha de responsabilidad para orientar a una IA. No es una persona autónoma, no concede permisos y no sustituye a quien revisa y firma el trabajo.

## Roles iniciales

| Rol | Cuándo utilizarlo |
|---|---|
| [`architect`](agents/architect.md) | Cambios transversales, contratos, estructura, seguridad y calidad |
| [`data-analyst`](agents/data-analyst.md) | Dataset, EDA, calidad, clases, partición y evidencias estadísticas |
| [`backend-developer`](agents/backend-developer.md) | API, validación, inferencia, persistencia y servicios |
| [`frontend-developer`](agents/frontend-developer.md) | React PWA, UX, accesibilidad, estados y consumo del contrato |

La asignación humana vigente se consulta en `docs/project_management/team.md`; no se duplica aquí.

## Procedimientos iniciales

| Procedimiento | Resultado |
|---|---|
| [`start-task`](skills/start-task/SKILL.md) | Resume alcance, archivos, checks y bloqueantes antes de editar |
| [`verify-task`](skills/verify-task/SKILL.md) | Contrasta el trabajo con criterios y evidencias |
| [`review-change`](skills/review-change/SKILL.md) | Busca defectos, riesgos e inconsistencias sin modificar |
| [`prepare-pr`](skills/prepare-pr/SKILL.md) | Completa la plantilla oficial con información comprobada |

## Regla de uso

El rol se combina siempre con una spec y una tarea concretas:

```text
rol + spec + tarea + reglas comunes
```

Si falta cualquiera de esas piezas, solo se puede analizar o pedir aclaraciones; no se debe implementar.

## Orden de prioridad

Si dos instrucciones parecen contradecirse, se aplica este orden:

1. seguridad, privacidad y autorización humana;
2. `AGENTS.md`;
3. spec, decisiones y tarea activas;
4. rol de esta carpeta;
5. sugerencias de la herramienta de IA.

## Límites comunes

- No inventar decisiones ni completar preguntas abiertas.
- No ampliar la tarea porque el rol cubra un área más amplia.
- No incluir narrativas CFPB, secretos ni datos brutos en prompts externos.
- No modificar archivos antes de explicar alcance, archivos previstos y bloqueantes.
- No declarar una tarea terminada sin comprobaciones y evidencias.
- No publicar, mergear ni sustituir la revisión humana.
