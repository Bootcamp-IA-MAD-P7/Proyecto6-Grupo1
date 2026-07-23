---
name: verify-task
description: "Comprobar una tarea implementada contra su spec, criterios de aceptación, tests y estado real del repositorio. Usar antes de marcar T-XXX como completada o afirmar que un cambio está listo."
---

# Verificar una tarea

Buscar evidencia, no justificar el resultado.

## Entradas necesarias

- Spec y tarea verificadas.
- Cambio local o commit que se quiere comprobar.
- Rol responsable.

## Procedimiento

1. Leer los requisitos y criterios cubiertos por la tarea.
2. Revisar el diff y confirmar que no mezcla trabajo ajeno.
3. Ejecutar las comprobaciones indicadas en `tasks.md`.
4. Ejecutar como mínimo:

```bash
git diff --check
python scripts/quality/check_repository.py
git status --short --branch
```

5. Añadir los tests específicos del área modificada.
6. Revisar privacidad, seguridad, documentación y contratos afectados.
7. Comparar las afirmaciones documentales con el comportamiento real.
8. Clasificar el resultado:
   - `PASS`: criterios cubiertos y checks correctos;
   - `BLOCKED`: falta una dependencia o decisión;
   - `FAIL`: existe un incumplimiento reproducible.
9. Registrar únicamente evidencias observadas.

## Reglas

- No marcar una tarea `[x]` si una comprobación obligatoria falla.
- No ocultar warnings, tests omitidos ni verificaciones no ejecutadas.
- No cambiar criterios para hacer pasar el trabajo.
- No usar datos sensibles como evidencia.
- No corregir trabajo fuera de alcance durante una revisión.

## Resultado

```text
Resultado:
Criterios comprobados:
Comandos y resultados:
Revisión manual:
Incumplimientos:
Evidencias:
Trabajo pendiente:
```
