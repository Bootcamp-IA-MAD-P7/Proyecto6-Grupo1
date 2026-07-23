---
name: review-change
description: "Revisar un diff, commit o rama frente a la spec y las reglas del proyecto. Usar para una revisión independiente antes de preparar la Pull Request o cuando se solicite buscar riesgos, regresiones e inconsistencias."
---

# Revisar un cambio

Realizar una revisión de solo lectura antes de proponer correcciones.

## Entradas necesarias

- Spec y tareas relacionadas.
- Diff, commit o rama que se revisará.
- Evidencias de verificación disponibles.

## Procedimiento

1. Confirmar la base y el alcance del cambio.
2. Leer requisitos, decisiones y límites aplicables.
3. Revisar primero:
   - errores funcionales;
   - seguridad y privacidad;
   - contratos y compatibilidad;
   - pérdida o fuga de datos;
   - tests ausentes o insuficientes.
4. Revisar después mantenibilidad, duplicidad, UX y documentación.
5. Comprobar que no se presenta un mock, contrato o carpeta como capacidad real.
6. Ordenar hallazgos por gravedad:
   - `blocking`;
   - `high`;
   - `medium`;
   - `low`.
7. Indicar archivo, ubicación, impacto y corrección esperada.
8. Si no hay hallazgos, explicar qué se revisó y qué riesgo residual permanece.

## Reglas

- No modificar archivos durante la revisión.
- No confundir preferencias de estilo con defectos.
- No afirmar que todo está correcto si no se ejecutaron las comprobaciones.
- No aprobar cambios fuera de la spec.
- No inventar fallos sin una forma concreta de reproducirlos.

## Resultado

```text
Alcance revisado:
Hallazgos:
Comprobaciones consideradas:
Preguntas o bloqueantes:
Riesgo residual:
Conclusión:
```
