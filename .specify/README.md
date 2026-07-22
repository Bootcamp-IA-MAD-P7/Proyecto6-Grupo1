# Trabajo basado en specs

Las conversaciones ayudan a explorar. Las specs conservan dentro del repositorio lo que el equipo ha decidido construir.

## Jerarquía documental

```text
intent -> spec -> plan -> tasks -> implementation -> verification -> closure
```

- [`intent.md`](intent.md) define el propósito, las restricciones globales y los principios estables del proyecto.
- `specs/` contiene un contrato independiente por descubrimiento, funcionalidad o cambio relevante.
- `templates/` proporciona la estructura mínima para redactar esos contratos.

El intent no selecciona una idea de negocio ni sustituye las specs. Solo cambia cuando cambia el propósito global del proyecto.

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

## Specs activas

- [`000-problem-discovery`](../specs/000-problem-discovery/spec.md) gobierna el cierre del descubrimiento.
- [`001-cfpb-target-contract`](../specs/001-cfpb-target-contract/spec.md) fija las reglas compartidas de clases y datos mientras el EDA avanza en paralelo.

No se crea una spec por cada notebook o tarea pequeña. Se crea cuando varias personas o componentes necesitan compartir un comportamiento, una decisión o una evidencia verificable.
