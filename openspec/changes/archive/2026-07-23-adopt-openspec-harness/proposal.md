## Why

El repositorio dispone de un arnés agéntico propio y operativo, pero todavía no utiliza el ciclo de vida OpenSpec recomendado por la referencia Specboot elegida. OpenSpec debe convertirse ahora en el motor SDD real para que cada cambio futuro disponga de propuesta, delta de requisitos, diseño, tareas, instrucciones de implementación, validación y archivo antes de que el proyecto avance más.

## What Changes

- Incorporar OpenSpec `1.6.0` como dependencia local exacta del repositorio.
- Inicializar los flujos oficiales de OpenSpec para Codex, GitHub Copilot, Claude Code, Cursor y Gemini CLI.
- Configurar OpenSpec con el contexto de producto, entrega, privacidad, documentación y roles del proyecto.
- Extender el arnés para incluir el estado y las instrucciones reales de un cambio OpenSpec.
- Añadir salud y validación estricta de OpenSpec a los controles locales y GitHub Actions.
- Mantener las carpetas numeradas existentes de `specs/` como expedientes compatibles para el trabajo ya asignado, mientras todos los cambios nuevos comienzan en `openspec/changes/`.
- Documentar instalación, límites de migración, flujo del equipo, reversión y evidencias.

## Capabilities

### New Capabilities

- `openspec-governance`: ciclo de vida OpenSpec local al repositorio, validación, compatibilidad y uso por el equipo.

### Modified Capabilities

- Ninguna. Todavía no existen capacidades OpenSpec de referencia.

## Impact

- Herramientas Node.js de raíz: `package.json` y `package-lock.json`.
- Configuración OpenSpec e integraciones generadas para cinco herramientas de IA.
- `scripts/harness.py`, documentación, tests y workflow de calidad.
- Gobierno del arnés, incorporación al equipo, README, changelog, daily y fuentes técnicas para NotebookLM.
- Las personas colaboradoras necesitarán Node.js `20.19.0` o superior y ejecutar una vez `npm ci`; no será necesaria una instalación global de OpenSpec.
