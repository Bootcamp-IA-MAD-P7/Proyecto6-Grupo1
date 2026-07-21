# Trabajo basado en specs

Las conversaciones ayudan a explorar. Las specs conservan dentro del repositorio lo que el equipo ha decidido construir.

## Una carpeta por cambio

```text
specs/001-nombre-del-cambio/
├── spec.md
├── plan.md
├── tasks.md
└── decisions.md
```

Las plantillas están en `.specify/templates/`.

## Secuencia

1. **Spec:** problema, usuario, alcance, escenarios y criterios de aceptación.
2. **Plan:** solución técnica, contratos, archivos, pruebas, riesgos y reversión.
3. **Tasks:** unidades pequeñas con dependencias y verificación.
4. **Implementación:** únicamente tareas activas.
5. **Verificación:** tests, métricas, comandos o revisión manual.
6. **Cierre:** sincronizar tareas, decisiones, documentación y comportamiento real.

## Estados

- `[ ]` pendiente.
- `[~]` en curso.
- `[x]` completada y verificada.
- `[!]` bloqueada.
- `[-]` descartada con motivo.

## Puertas de avance

No se pasa a implementación si existen preguntas bloqueantes sobre el comportamiento. No se cierra una spec si sus criterios de aceptación carecen de evidencia.

## Primera spec futura

La primera spec se creará cuando el equipo empiece formalmente la selección de la idea de negocio. Esta estructura no anticipa esa decisión.
