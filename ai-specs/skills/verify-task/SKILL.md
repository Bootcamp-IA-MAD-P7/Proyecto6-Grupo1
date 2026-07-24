---
name: verify-task
description: "Verificar una implementación contra OpenSpec, contratos, tests y estado real."
---

# Verificar trabajo

## Procedimiento

1. Leer requisitos, escenarios y tareas del cambio OpenSpec; usar el expediente numerado solo para trabajo heredado.
2. Revisar el diff y confirmar que no mezcla trabajo ajeno.
3. Ejecutar las comprobaciones exactas de las tareas.
4. Ejecutar como mínimo:

```bash
npm run openspec:validate
python scripts/quality/check_repository.py
git diff --check
git status --short --branch
```

5. Añadir los tests del área.
6. Revisar privacidad, seguridad, contratos, documentación y briefing.
7. Comparar cada afirmación con evidencia real.
8. Clasificar `PASS`, `BLOCKED` o `FAIL`.
9. Marcar una tarea solo después de observar el resultado correcto.

## Reglas

- No ocultar warnings, omisiones ni checks no ejecutados.
- No cambiar criterios para hacer pasar el trabajo.
- No usar datos sensibles como evidencia.
- No corregir trabajo fuera de alcance durante una verificación.

## Resultado

```text
Resultado:
Requisitos y escenarios:
Comandos y resultados:
Revisión manual:
Incumplimientos:
Evidencias:
Trabajo pendiente:
```
