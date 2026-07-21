# Decisiones: Selección del problema de negocio

## ADR-001 Utilizar un proceso de descubrimiento basado en evidencia

- Fecha: `2026-07-21`
- Estado: `accepted`
- Relacionada con: `R-007, R-008, R-010, AC-001, T-001`

### Contexto

El proyecto todavía no tiene una idea de negocio ni un dataset seleccionados. Elegir únicamente por intuición o por la disponibilidad de datos podría producir un problema sin valor, un target multiclase artificial o una solución inviable.

### Opciones consideradas

1. Elegir primero un dataset atractivo y construir un relato de negocio alrededor.
2. Seleccionar una idea mediante conversación informal y comenzar a implementar.
3. Comparar alternativas con puertas críticas, una matriz común, evidencias y una decisión versionada.

### Decisión

Se adopta la opción 3. La selección utilizará criterios acordados antes de puntuar, puertas críticas para multiclase, datos, licencia, leakage y riesgos, y razonamiento cualitativo además de puntuaciones.

La matriz apoyará la decisión, pero no elegirá automáticamente. No seleccionar ninguna idea será una salida válida cuando no exista evidencia suficiente.

### Consecuencias

- Beneficios:
  - reduce decisiones basadas en preferencias o disponibilidad inmediata;
  - hace comparables las alternativas;
  - conserva razones de descarte;
  - proporciona trazabilidad para specs y presentaciones posteriores.
- Costes o límites:
  - requiere trabajo de investigación antes de implementar;
  - los pesos y puntuaciones contienen juicio humano y deben justificarse;
  - una idea puede bloquearse aunque resulte atractiva.
- Trabajo posterior:
  - resolver Q-001 a Q-004;
  - versionar la matriz;
  - registrar y evaluar candidatos;
  - documentar la decisión final en este archivo.

### Evidencia

- `.specify/intent.md`.
- `docs/product/idea_evaluation_template.md`.
- `specs/000-problem-discovery/spec.md`.

## PDR-001 Seleccionar problema, usuario y dataset candidato

- Fecha: `pendiente`
- Estado: `proposed`
- Relacionada con: `R-011, AC-008, AC-009, T-008`

### Contexto

La evaluación de alternativas todavía no ha comenzado. Esta entrada se completará únicamente después de ejecutar las tareas T-001 a T-007.

### Opciones consideradas

1. Pendiente de registrar candidatos.

### Decisión

Pendiente. No existe una idea preseleccionada.

### Consecuencias

- Beneficios: pendientes de la decisión.
- Costes o límites: pendientes de la decisión.
- Trabajo posterior: pendiente de la decisión.

### Evidencia

- Pendiente.
