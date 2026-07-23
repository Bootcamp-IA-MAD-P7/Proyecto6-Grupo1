## 1. OpenSpec reproducible

- [x] 1.1 Fijar `@fission-ai/openspec` `1.6.0`, Node.js `>=20.19.0` y scripts npm; verificar con `npm ci`, `npm audit` y `npx openspec --version`.
- [x] 1.2 Inicializar adaptadores oficiales para Codex, GitHub Copilot, Claude Code, Cursor y Gemini CLI; revisar el árbol generado.
- [x] 1.3 Configurar contexto y reglas de artefactos en `openspec/config.yaml`; comprobar que `openspec instructions` los incorpora.
- [x] 1.4 Validar estrictamente la propuesta, diseño, delta y tareas de `adopt-openspec-harness`.

## 2. Integración con el arnés

- [x] 2.1 Añadir diagnóstico de Node.js, dependencia local, raíz OpenSpec y configuración al punto de entrada del arnés.
- [x] 2.2 Añadir un modo de cambio OpenSpec que consuma `status` e `instructions --json` sin reconstruir su estado.
- [x] 2.3 Mantener compatibilidad con `--spec` y `--task` para las tareas numeradas ya asignadas.
- [x] 2.4 Desactivar la telemetría en invocaciones del arnés y evitar paquetes parciales ante cualquier fallo.
- [x] 2.5 Añadir tests unitarios para diagnóstico, cambio válido, cambio inexistente, bloqueo y contenido seguro.

## 3. Calidad automática

- [x] 3.1 Integrar `npm ci`, `openspec doctor` y `openspec validate --all --strict` en `repository-quality`.
- [x] 3.2 Extender `check_repository.py` para exigir archivos, versión y configuración de OpenSpec.
- [x] 3.3 Ejecutar las suites Python, validación OpenSpec, auditoría npm y control de whitespace.

## 4. Migración y uso del equipo

- [x] 4.1 Actualizar `AGENTS.md`, spec `004`, guías y catálogo de specs con el límite entre OpenSpec y los expedientes numerados.
- [x] 4.2 Documentar instalación de una sola vez, comandos por herramienta, flujo OpenSpec y adaptación de entregas existentes.
- [x] 4.3 Actualizar changelog, daily y fuentes técnicas de NotebookLM sin presentar producto o modelo como implementados.
- [x] 4.4 Crear recursos visuales y rehacer el README con OpenSpec, arnés, arquitectura, estado y los 25 criterios de entrega.

## 5. Verificación y cierre

- [x] 5.1 Ejecutar un ciclo real de OpenSpec sobre este cambio y generar contexto mediante el arnés.
- [x] 5.2 Completar revisión adversarial, comprobaciones de seguridad, documentación y reversión.
- [x] 5.3 Marcar las tareas verificadas, validar estrictamente y archivar el cambio para crear `openspec/specs/openspec-governance/spec.md`.
- [x] 5.4 Preparar la Pull Request con evidencias reales; la publicación, CI y fusión permanecen bajo confirmación humana.
