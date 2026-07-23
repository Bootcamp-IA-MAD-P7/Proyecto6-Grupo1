---
name: prepare-pr
description: "Preparar el Markdown completo de una Pull Request usando la plantilla oficial y evidencias reales. Usar después de verificar y revisar una tarea, antes de abrir o actualizar una PR hacia dev."
---

# Preparar una Pull Request

Completar la plantilla sin publicar nada automáticamente.

## Entradas necesarias

- Spec y tareas relacionadas.
- Diff o commits finales.
- Resultado de verificación.
- Resultado de revisión.

## Procedimiento

1. Leer `.github/pull_request_template.md` completa.
2. Confirmar rama de trabajo, base `dev` y estado de Git.
3. Resumir únicamente cambios presentes en el diff.
4. Enlazar spec, tareas y, cuando exista, Jira.
5. Copiar comandos y resultados reales de verificación.
6. Explicar impacto en documentación, NotebookLM, UX, seguridad y contratos.
7. Registrar riesgos y una reversión concreta.
8. Marcar solo las casillas demostradas.
9. Entregar la plantilla completa dentro de un único bloque Markdown.

## Reglas

- No eliminar secciones de la plantilla.
- No escribir `No aplica` sin explicar por qué.
- No marcar checks no ejecutados.
- No afirmar que CI pasa antes de que exista ese resultado.
- No abrir, publicar, pushear ni mergear sin petición humana explícita.
- Conservar saltos de línea y bloques de código para no romper el formato.

## Resultado

Devolver:

1. título Conventional Commit propuesto;
2. cuerpo completo de la PR en Markdown;
3. comprobaciones o campos todavía pendientes fuera del bloque.
