---
name: prepare-pr
description: "Preparar la plantilla completa de una PR con evidencias reales después de terminar OpenSpec."
---

# Preparar una Pull Request

## Entradas

- cambio OpenSpec archivado, o tarea heredada completada;
- diff o commits finales;
- resultados de verificación y revisión.

## Procedimiento

1. Leer `.github/pull_request_template.md` completa.
2. Confirmar rama, base `dev` y estado de Git.
3. Confirmar que no quedan tareas OpenSpec pendientes.
4. Resumir únicamente cambios del diff.
5. Enlazar cambio, requisitos, tareas y Jira cuando exista.
6. Copiar comandos y resultados reales.
7. Explicar impacto en documentación, NotebookLM, UX, seguridad y contratos.
8. Registrar riesgos y reversión.
9. Marcar solo casillas demostradas.
10. Entregar la plantilla completa en Markdown.

No eliminar secciones, inventar CI, evidencias o tests, ni publicar sin autorización humana. Conservar saltos y bloques de código.

## Resultado

1. título Conventional Commit;
2. cuerpo completo de PR;
3. campos todavía pendientes.
