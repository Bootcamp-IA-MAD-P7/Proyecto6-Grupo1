# Guía de contribución

## Flujo Git

1. Actualizar `dev`.
2. Ejecutar `npm ci` y `python scripts/harness.py doctor`.
3. Crear una rama de trabajo desde `dev`, incluyendo la clave Jira cuando exista.
4. Crear o continuar el cambio OpenSpec correspondiente.
5. Implementar únicamente sus tareas acordadas.
6. Verificar y archivar el cambio.
7. Abrir Pull Request hacia `dev`.
8. Mergear solo con revisión y comprobaciones correctas.

Las tareas `001/T-004` y `003/T-006` pueden terminarse con el flujo numerado anterior. Cualquier cambio nuevo de alcance o contrato se adapta mediante OpenSpec.

La protección actual exige Pull Request y checks, pero todavía no exige una aprobación humana en GitHub. Antes de marcar una PR como lista, la persona responsable debe solicitar revisión funcional al área afectada cuando exista: Miguel para arquitectura y contratos, Abel para frontend/UX, José para backend y Víctor para datos/EDA. Esta revisión operativa no sustituye los checks ni amplía el alcance de la spec.

Nombres recomendados:

```text
feature/PG-N-<descripcion>
fix/PG-N-<descripcion>
docs/PG-N-<descripcion>
test/PG-N-<descripcion>
ci/PG-N-<descripcion>
chore/PG-N-<descripcion>
refactor/PG-N-<descripcion>
```

Las automatizaciones gestionadas, como Dependabot, conservan su convención. Las
ramas anteriores a Jira no se renombran únicamente por formato.

## Commits

Usar mensajes breves y descriptivos, preferiblemente con estilo Conventional Commits:

```text
feat: add multiclass evaluation report
fix: preserve class labels during preprocessing
docs: define dataset selection criteria
test: cover model inference contract
```

## Pull Requests

Cada PR debe:

- apuntar a `dev`, salvo un release aprobado;
- enlazar Jira `PG-N` o explicar una excepción aprobada de bootstrap, emergencia o automatización;
- enlazar el cambio OpenSpec y las tareas que cubre, o el expediente heredado aplicable;
- mantener un alcance coherente;
- explicar cómo se verificó;
- actualizar documentación y decisiones afectadas;
- evitar secretos, datos pesados y artefactos locales.
- revisar impacto en UX, seguridad y fuentes para NotebookLM.
- identificar responsable de área, tarea activa y bloqueos todavía abiertos;
- distinguir claramente entre comportamiento real, mock, propuesta y trabajo futuro.

## Definition of Done

Una tarea está terminada cuando:

- cumple sus criterios de aceptación;
- las comprobaciones acordadas pasan;
- la evidencia queda registrada;
- la documentación coincide con el comportamiento real;
- no introduce cambios no acordados.
- los quality gates relevantes pasan;
- la comunicación externa no promete más de lo implementado.
- el cambio OpenSpec está archivado o la tarea heredada está cerrada con evidencia.
