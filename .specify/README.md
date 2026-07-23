# Intención y compatibilidad del método de specs

[`intent.md`](intent.md) define el propósito, las restricciones globales y los principios estables del proyecto. Sigue siendo una fuente vigente.

Desde el 23 de julio de 2026, los cambios nuevos se gestionan con OpenSpec:

```text
intent
  -> openspec/changes/<change>/
  -> propuesta + requisitos + diseño + tareas
  -> implementación + verificación
  -> openspec/specs/ + archivo histórico
```

Las plantillas de `.specify/templates/` y las carpetas numeradas de `specs/` se conservan para interpretar y terminar el trabajo creado antes de la adopción. No deben utilizarse para iniciar cambios nuevos.

## Empezar un cambio nuevo

```bash
npm ci
python scripts/harness.py doctor
npm exec openspec new change <nombre-en-kebab-case>
```

Después se completan los artefactos que indique OpenSpec y se genera el contexto de trabajo:

```bash
python scripts/harness.py start --role <rol> --change <nombre>
```

La guía completa está en [`docs/project_management/harness_quickstart.md`](../docs/project_management/harness_quickstart.md).

## Trabajo anterior aún asignado

- Víctor puede terminar `001/T-004`.
- Abel puede terminar `003/T-006`.
- Si esas entregas incorporan decisiones nuevas o contradicen los contratos vigentes, se abre un cambio OpenSpec antes de integrarlas.

Jira registra quién hace el trabajo y su estado. OpenSpec conserva qué se acuerda construir y cómo se demuestra.
