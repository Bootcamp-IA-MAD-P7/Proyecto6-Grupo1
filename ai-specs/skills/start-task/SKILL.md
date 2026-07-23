---
name: start-task
description: "Preparar el inicio de una tarea asignada a partir de un rol, una spec y un identificador T-XXX. Usar cuando una persona pida comenzar, retomar o explicar una tarea antes de modificar archivos."
---

# Iniciar una tarea

Preparar el trabajo antes de editar.

## Entradas necesarias

- Rol de `ai-specs/agents/`.
- Carpeta de la spec.
- Identificador `T-XXX`.

Si falta una entrada, pedirla o limitarse a explicar el flujo.

## Procedimiento

1. Leer `AGENTS.md`, `README.md` y `CONTRIBUTING.md`.
2. Comprobar rama y estado de Git.
3. Leer `spec.md`, `plan.md`, `tasks.md` y `decisions.md` de la spec.
4. Localizar la tarea exacta y comprobar estado, responsable y dependencias.
5. Leer el rol y únicamente los contratos enlazados necesarios.
6. Distinguir hechos confirmados, decisiones abiertas y bloqueantes.
7. Presentar antes de editar:
   - objetivo de la tarea;
   - alcance incluido y excluido;
   - archivos previstos;
   - comprobaciones exigidas;
   - bloqueantes y riesgos.
8. Trabajar solo si la tarea existe, no está bloqueada y el cambio está autorizado.

## Reglas

- No interpretar el rol como permiso para ampliar el alcance.
- No comenzar una tarea `[!]`, descartada o con dependencias incumplidas.
- No reabrir una tarea `[x]` sin una corrección o decisión explícita.
- No inventar Jira, evidencias, decisiones ni requisitos.
- No incluir datos sensibles en el contexto.

## Resultado

Entregar un resumen de inicio con:

```text
Rol:
Spec y tarea:
Objetivo:
Incluido:
Fuera de alcance:
Archivos previstos:
Comprobaciones:
Bloqueantes:
```
