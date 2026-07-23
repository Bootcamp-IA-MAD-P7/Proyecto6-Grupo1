# Roles y procedimientos del arnés

Esta carpeta amplía OpenSpec con instrucciones propias del proyecto. No es otra herramienta de requisitos.

| Capa | Responsabilidad |
|---|---|
| `openspec/` | Propuestas, requisitos, diseño, tareas, estado y archivo |
| `ai-specs/agents/` | Responsabilidad y límites de cada rol |
| `ai-specs/skills/` | Procedimientos de inicio, verificación, revisión y PR |
| `scripts/harness.py` | Diagnóstico y composición segura del contexto |
| Adaptadores `.codex/`, `.github/`, `.claude/`, `.cursor/`, `.gemini/` | Comandos oficiales de OpenSpec para cada herramienta |

## Roles

| Rol | Uso |
|---|---|
| [`architect`](agents/architect.md) | Cambios transversales, contratos, seguridad y calidad |
| [`data-analyst`](agents/data-analyst.md) | Dataset, EDA, calidad, clases, partición y métricas |
| [`backend-developer`](agents/backend-developer.md) | API, inferencia, persistencia y servicios |
| [`frontend-developer`](agents/frontend-developer.md) | React PWA, UX, accesibilidad y consumo del contrato |

## Procedimientos

| Procedimiento | Resultado |
|---|---|
| [`start-task`](skills/start-task/SKILL.md) | Aclara alcance, archivos, bloqueantes y checks |
| [`verify-task`](skills/verify-task/SKILL.md) | Contrasta implementación, requisitos y evidencias |
| [`review-change`](skills/review-change/SKILL.md) | Busca defectos, riesgos e inconsistencias |
| [`prepare-pr`](skills/prepare-pr/SKILL.md) | Prepara una PR sin inventar evidencias |

## Prioridad

1. Seguridad, privacidad y autorización humana.
2. `AGENTS.md` y `openspec/config.yaml`.
3. Artefactos del cambio OpenSpec y contratos enlazados.
4. Rol y procedimiento de esta carpeta.
5. Sugerencias de la herramienta utilizada.

Ningún rol concede permisos adicionales. La revisión humana sigue siendo obligatoria antes de publicar, archivar o fusionar.
