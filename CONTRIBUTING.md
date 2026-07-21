# Guía de contribución

## Flujo Git

1. Actualizar `dev`.
2. Crear una rama de trabajo desde `dev`.
3. Implementar únicamente las tareas acordadas.
4. Verificar el cambio localmente.
5. Abrir Pull Request hacia `dev`.
6. Mergear solo con revisión y comprobaciones correctas.

Nombres recomendados:

```text
feature/<descripcion>
fix/<descripcion>
docs/<descripcion>
test/<descripcion>
ci/<descripcion>
chore/<descripcion>
refactor/<descripcion>
```

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
- enlazar la spec y tareas que cubre;
- mantener un alcance coherente;
- explicar cómo se verificó;
- actualizar documentación y decisiones afectadas;
- evitar secretos, datos pesados y artefactos locales.
- revisar impacto en UX, seguridad y fuentes para NotebookLM.

## Definition of Done

Una tarea está terminada cuando:

- cumple sus criterios de aceptación;
- las comprobaciones acordadas pasan;
- la evidencia queda registrada;
- la documentación coincide con el comportamiento real;
- no introduce cambios no acordados.
- los quality gates relevantes pasan;
- la comunicación externa no promete más de lo implementado.
