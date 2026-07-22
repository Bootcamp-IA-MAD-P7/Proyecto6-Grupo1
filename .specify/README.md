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
- [`002-team-ai-workflow`](../specs/002-team-ai-workflow/spec.md) conserva el flujo independiente de proveedor y está cerrada.
- [`003-complaint-routing-experience`](../specs/003-complaint-routing-experience/spec.md) define la experiencia React PWA y el contrato de inferencia para mocks.

## Asignaciones actuales

- Miguel mantiene arquitectura, contratos compartidos y coherencia documental.
- Víctor trabaja en `001/T-004`, análisis del CSV y EDA agregado.
- Abel trabaja en `003/T-008`, validación y endurecimiento de la PWA mock.
- José tiene asignada `003/T-007`, futura integración backend, todavía bloqueada para implementación real.
- Josué está fuera del equipo.

Jira se incorpora el 23 de julio de 2026 como tablero operativo. No sustituye a las specs: una tarjeta indica quién y cuándo; la spec define qué debe cumplirse y con qué evidencia.

No se crea una spec por cada notebook o tarea pequeña. Se crea cuando varias personas o componentes necesitan compartir un comportamiento, una decisión o una evidencia verificable.

## Empezar una tarea

El [flujo operativo del equipo](../docs/project_management/workflow.md) conecta Jira, spec, rama, IA, verificaciones y Pull Request. Si una IA no puede leer el repositorio, puede recibir un paquete generado desde fuentes versionadas:

```bash
python scripts/documentation/build_ai_handoff.py \
  --spec 001-cfpb-target-contract \
  --task T-004
```
