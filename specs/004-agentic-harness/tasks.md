# Tareas: Arnés agéntico de trabajo

- Spec: [`spec.md`](spec.md)
- Plan: [`plan.md`](plan.md)

## T-001 Definir el contrato del arnés

- Estado: `[~]`
- Responsable: `Miguel / arquitectura`
- Dependencias: `ninguna`
- Requisitos cubiertos: `R-001 a R-012`
- Archivos previstos:
  - `specs/004-agentic-harness/`
- Trabajo:
  - Definir objetivo, límites, flujo, criterios y estrategia sin implementar automatizaciones.
- Criterio de cierre:
  - Los cuatro documentos de la spec son coherentes con `AGENTS.md` y con la spec `002`.
- Verificación:
  - Comando o revisión: `git diff --check` y revisión manual.
  - Resultado esperado: sin errores de formato ni duplicación de fuentes de verdad.
- Evidencia obtenida:
  - Pendiente de verificación.

## T-002 Definir roles agénticos mínimos

- Estado: `[ ]`
- Responsable: `Miguel / arquitectura`
- Dependencias: `T-001`
- Requisitos cubiertos: `R-002, R-003, R-005, R-011`
- Archivos previstos:
  - `ai-specs/README.md`
  - `ai-specs/agents/`
- Trabajo:
  - Definir arquitectura, datos, backend y frontend con responsabilidades, entradas, salidas y límites.
- Criterio de cierre:
  - Cada rol ayuda a acotar una tarea sin conceder permisos adicionales.
- Verificación:
  - Comando o revisión: validación de estructura y revisión cruzada.
  - Resultado esperado: cuatro roles válidos, sin contradicciones con `AGENTS.md`.
- Evidencia obtenida:
  - Pendiente.

## T-003 Definir procedimientos reutilizables

- Estado: `[ ]`
- Responsable: `Miguel / arquitectura`
- Dependencias: `T-001`
- Requisitos cubiertos: `R-004, R-006, R-011`
- Archivos previstos:
  - `ai-specs/skills/`
- Trabajo:
  - Crear procedimientos para iniciar, verificar, revisar y preparar una Pull Request.
- Criterio de cierre:
  - Cada procedimiento tiene una sola finalidad, entradas claras y resultado comprobable.
- Verificación:
  - Comando o revisión: validación de secciones y enlaces.
  - Resultado esperado: cuatro procedimientos componibles y legibles.
- Evidencia obtenida:
  - Pendiente.

## T-004 Implementar la entrada única

- Estado: `[ ]`
- Responsable: `Miguel / arquitectura`
- Dependencias: `T-002, T-003`
- Requisitos cubiertos: `R-002 a R-009`
- Archivos previstos:
  - `scripts/harness.py`
  - `scripts/documentation/build_ai_handoff.py`, si es necesario
  - `tests/unit/`
- Trabajo:
  - Validar rol, spec y tarea y generar un único Markdown desde fuentes versionadas.
- Criterio de cierre:
  - Una orden válida genera el paquete y las entradas inválidas fallan sin salida parcial.
- Verificación:
  - Comando o revisión: tests unitarios y generación de ejemplo.
  - Resultado esperado: paquete seguro en `exports/`.
- Evidencia obtenida:
  - Pendiente.

## T-005 Pilotar con la tarea real de datos

- Estado: `[ ]`
- Responsable: `Miguel y Víctor`
- Dependencias: `T-004`
- Requisitos cubiertos: `R-012, AC-004, AC-007, AC-009`
- Archivos previstos:
  - `exports/`, no versionado
  - documentación de evidencia, si procede
- Trabajo:
  - Generar el contexto para `data-analyst`, `001-cfpb-target-contract` y `T-004`.
  - Confirmar que permite entender el trabajo sin cambiar el EDA ni su estado.
- Criterio de cierre:
  - Víctor puede explicar alcance, límites y verificaciones usando el paquete.
- Verificación:
  - Comando o revisión: demostración manual y revisión del Markdown generado.
  - Resultado esperado: flujo comprensible y sin datos sensibles.
- Evidencia obtenida:
  - Pendiente.

## T-006 Integrar comprobaciones y manual breve

- Estado: `[ ]`
- Responsable: `Miguel / arquitectura y QA`
- Dependencias: `T-005`
- Requisitos cubiertos: `R-010, R-011, AC-005, AC-006, AC-008, AC-009`
- Archivos previstos:
  - `.github/workflows/repository-quality.yml`
  - `docs/project_management/harness_quickstart.md`
  - documentación viva afectada
- Trabajo:
  - Integrar los tests validados en CI.
  - Explicar el flujo en lenguaje corriente con comandos copiables.
- Criterio de cierre:
  - El quality gate detecta definiciones rotas y el equipo puede usar el manual.
- Verificación:
  - Comando o revisión: suite local, `check_repository.py`, CI y prueba manual.
  - Resultado esperado: comprobaciones correctas y manual utilizable.
- Evidencia obtenida:
  - Pendiente.

## Checklist de cierre

- [ ] Todos los criterios de aceptación están cubiertos.
- [ ] Las pruebas acordadas pasan.
- [ ] El piloto se ha completado sin modificar el trabajo de datos.
- [ ] Las decisiones relevantes están registradas.
- [ ] La documentación coincide con el comportamiento real.
- [ ] No quedan preguntas bloqueantes para la primera versión.
