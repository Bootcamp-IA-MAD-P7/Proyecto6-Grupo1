---
name: start-task
description: "Preparar un cambio OpenSpec o una tarea heredada antes de modificar archivos."
---

# Iniciar trabajo

## Entradas

- rol de `ai-specs/agents/`;
- cambio OpenSpec con planificación completa;
- o, solo en compatibilidad, spec numerada y tarea `T-XXX`.

## Procedimiento

1. Leer `AGENTS.md`, `README.md`, `CONTRIBUTING.md` y `openspec/config.yaml`.
2. Comprobar rama y estado de Git.
3. Para OpenSpec, consumir propuesta, requisitos, diseño, tareas y estado indicados por `openspec instructions apply`.
4. Para compatibilidad, leer los cuatro documentos del expediente numerado y localizar la tarea exacta.
5. Leer el rol y únicamente los contratos enlazados necesarios.
6. Separar hechos, decisiones abiertas, dependencias y bloqueantes.
7. Presentar objetivo, alcance, archivos, checks, riesgos y fuera de alcance.
8. Editar solo si el trabajo existe, está autorizado y no está bloqueado.

## Reglas

- El rol no amplía el alcance.
- No implementar con planificación OpenSpec incompleta.
- No reabrir tareas terminadas sin una corrección aprobada.
- No inventar Jira, evidencia, decisiones ni requisitos.
- No incorporar datos sensibles al contexto.

## Resultado

```text
Rol:
Cambio OpenSpec o tarea heredada:
Objetivo:
Incluido:
Fuera de alcance:
Archivos previstos:
Comprobaciones:
Bloqueantes:
```
