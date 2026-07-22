# Plan técnico: Flujo de trabajo del equipo con IA

- Spec: [`spec.md`](spec.md)
- Estado: `verified`

## Solución propuesta

Mantener `AGENTS.md` como entrada automática para agentes con acceso al repositorio y ampliar `docs/project_management/workflow.md` como guía humana. Para herramientas sin acceso, `build_ai_handoff.py` generará un único Markdown efímero desde fuentes versionadas.

```text
Jira → spec/tarea → AGENTS o paquete generado → cambio → checks → PR → evidencias
```

## Contrato del generador

- Entrada obligatoria: spec y tarea.
- Fuentes comunes: `AGENTS.md`, `README.md`, `CONTRIBUTING.md`, `.specify/README.md`.
- Fuentes específicas: `spec.md`, `plan.md`, `tasks.md`, `decisions.md`.
- Configuraciones: JSON de `config/` referenciados por el bundle.
- Inclusiones opcionales: únicamente `.md`, `.json`, `.yml`, `.yaml` y `.txt` ya seguidos por Git.
- Salida: `exports/ai-handoffs/<spec>-<tarea>.md`.

## Estrategia de pruebas

- Generación correcta para una tarea real.
- Inclusión automática del contrato CFPB referenciado.
- Rechazo de tarea inexistente.
- Rechazo de archivo no documental o fuera del repositorio.
- Comprobación del repositorio y enlaces Markdown.

## Riesgos

| Riesgo | Mitigación |
|---|---|
| Paquete desactualizado | Generarlo de nuevo desde `dev` antes de cada tarea |
| Exceso de contexto | Bundle limitado a fuentes comunes y spec activa |
| Fuga de datos | Solo archivos versionados y extensiones documentales |
| Delegación ciega | La persona conserva revisión, verificación y PR |
| Dependencia de una IA | Flujo y artefactos independientes del proveedor |

## Reversión

La automatización solo genera archivos ignorados por Git. Puede revertirse sin migraciones ni impacto en datos, aplicación o modelos.
