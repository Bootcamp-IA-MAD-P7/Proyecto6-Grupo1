# Plan histórico: primera iteración del arnés

- Expediente: [`spec.md`](spec.md)
- Estado: `superseded`

## Implementación conservada

La primera iteración creó:

- cuatro roles en `ai-specs/agents/`;
- cuatro procedimientos en `ai-specs/skills/`;
- `scripts/harness.py`;
- generación segura mediante `build_ai_handoff.py`;
- tests unitarios y validación en CI;
- un manual autoservicio.

## Evolución aprobada

La arquitectura definitiva añade OpenSpec sin duplicar esas piezas:

```text
OpenSpec
  -> propuesta + requisitos + diseño + tareas + estado
  -> arnés
  -> rol + procedimiento + contexto seguro
  -> implementación + verificación + revisión
  -> archivo + PR
```

Los detalles de implantación, riesgos y reversión están en el cambio OpenSpec `adopt-openspec-harness` y, tras su archivo, en `openspec/specs/openspec-governance/spec.md`.

## Compatibilidad

- `--change` es el modo normal.
- `--spec` y `--task` se mantienen temporalmente para `001/T-004` y `003/T-006`.
- No se crean expedientes numerados nuevos.
- Las entregas heredadas que alteren decisiones se adaptan mediante un cambio OpenSpec antes del merge.
