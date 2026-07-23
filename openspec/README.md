# OpenSpec en este proyecto

OpenSpec `1.6.0` es el sistema versionado de requisitos y cambios del proyecto.

```text
openspec/
├── config.yaml      # contexto y reglas compartidas
├── changes/         # cambios activos o archivados
└── specs/           # capacidades vigentes creadas al archivar
```

## Comandos universales

```bash
npm ci
python scripts/harness.py doctor
npm exec -- openspec new change <nombre>
npm exec -- openspec status --change <nombre>
npm exec -- openspec validate <nombre> --type change --strict
python scripts/harness.py start --role <rol> --change <nombre>
npm exec -- openspec archive <nombre> --yes
```

Los adaptadores oficiales para Codex, GitHub Copilot, Claude Code, Cursor y Gemini CLI están versionados en sus carpetas correspondientes. No se requiere una instalación global.

Las normas completas están en [`config.yaml`](config.yaml), [`AGENTS.md`](../AGENTS.md) y el [manual del equipo](../docs/project_management/harness_quickstart.md).
