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

## ADR-002 Adoptar reglas comunes para comparar candidatos

- Fecha: `2026-07-22`
- Estado: `accepted`
- Relacionada con: `R-007, R-008, AC-001, T-001`

### Contexto

La evaluación no puede comenzar de forma comparable mientras no existan escala, pesos, puertas críticas, evidencia mínima y un mecanismo de aprobación acordados. El equipo también necesita distinguir el seguimiento operativo en Jira de los contratos y decisiones conservados en el repositorio.

### Opciones consideradas

1. Puntuar mediante conversación sin una escala versionada.
2. Utilizar una puntuación automática como decisión final.
3. Utilizar una matriz ponderada con puertas críticas, puntuación individual, consolidación por mediana y decisión humana registrada.

### Decisión

Adoptar la opción 3 mediante la versión `1.0` de `docs/product/idea_evaluation_template.md`.

La regla aprobada establece:

- seis puertas críticas que pueden bloquear una alternativa;
- una escala de `0` a `5` con anclajes comunes;
- nueve criterios con pesos que suman el `100 %`;
- evidencia mínima obligatoria antes de declarar viabilidad;
- consolidación mediante la mediana de puntuaciones individuales;
- selección por mayoría absoluta del equipo activo —actualmente, al menos tres votos de cuatro— y sin puertas críticas pendientes;
- desempate basado en riesgo, viabilidad de entrega y evidencia de usuario;
- Jira para el estado operativo y el repositorio para contratos y decisiones.

La decisión fue aprobada el 22 de julio de 2026 con los votos favorables de Abel, Víctor y Miguel. José estuvo ausente. Josué había comunicado su baja del Bootcamp y ya no formaba parte del equipo activo.

### Consecuencias

- Beneficios:
  - permite comparar alternativas con las mismas reglas;
  - reduce el sesgo de elegir primero un dataset atractivo;
  - conserva desacuerdos y evidencias;
  - evita que una puntuación o Jira sustituyan una decisión versionada.
- Costes o límites:
  - exige una breve puntuación individual y puesta en común;
  - los pesos siguen conteniendo juicio humano;
  - una candidata atractiva puede bloquearse por licencia, leakage, riesgo o plazo.
- Trabajo posterior:
  - registrar candidatos con la versión `1.0` de la matriz;
  - crear el proyecto de Jira y añadir su enlace;
  - revisar las reglas únicamente si nueva evidencia demuestra que producen resultados incoherentes.

### Evidencia

- `docs/product/idea_evaluation_template.md`.
- `specs/000-problem-discovery/spec.md`.
- `specs/000-problem-discovery/tasks.md`.

## PDR-001 Seleccionar problema, usuario y dataset candidato

- Fecha: `2026-07-22`
- Estado: `accepted-with-conditions`
- Relacionada con: `R-011, AC-008, AC-009, T-008`

### Contexto

El equipo redujo la ronda a dos candidatas: clasificación y enrutamiento de reclamaciones financieras con datos del CFPB y clasificación visual de residuos con RealWaste. Ambas recibieron una preevaluación documental con la versión `1.0` de la matriz y quedaron a menos de cinco puntos. No se han registrado cuatro hojas individuales, por lo que estos valores no se presentan como mediana del equipo ni sustituyen la deliberación.

`CAND-001` ofrece un baseline textual más rápido, una fuente que se actualiza normalmente a diario y un recorrido claro hacia feedback y drift. A cambio, presenta mayores riesgos de privacidad, representatividad, desbalanceo y calidad. `CAND-002` proporciona una demo visual más directa y menor exposición a datos personales, pero añade riesgo de cambio de dominio, cómputo, integración y control de overfitting dentro del plazo.

### Opciones consideradas

1. `CAND-001`: clasificación y enrutamiento de reclamaciones financieras mediante narrativas públicas del CFPB; preevaluación técnica de 75/100 y recomendada con validaciones obligatorias.
2. `CAND-002`: clasificación visual de residuos mediante RealWaste; preevaluación técnica de 73/100 y viable condicional.

### Decisión

Seleccionar `CAND-001` como dirección del proyecto, con la Consumer Complaint Database del CFPB como dataset candidato, `complaint_what_happened` como entrada inicial y `product` como target propuesto.

José, Abel, Víctor y Miguel aprobaron la decisión por unanimidad el 22 de julio de 2026: cuatro votos favorables, cero votos contrarios y cero abstenciones.

La aceptación es condicional porque las puertas de datos, inferencia, privacidad y entrega todavía necesitan evidencia reproducible. Esta decisión autoriza el spike de viabilidad y la preparación de la siguiente spec; no autoriza todavía el EDA completo, entrenamiento ni implementación funcional. Si el spike revela una puerta crítica incumplida, el equipo revisará la decisión y podrá recuperar `CAND-002`.

Para cerrar formalmente T-007 todavía deberán conservarse las puntuaciones individuales o una ratificación explícita del equipo de la matriz consolidada. Esta ausencia no altera el resultado de la votación, pero impide afirmar que se ejecutó por completo el mecanismo de mediana.

### Consecuencias

- Beneficios:
  - permite iniciar un baseline interpretable con TF-IDF y un clasificador lineal;
  - la actualización frecuente de la fuente favorece feedback, reentrenamiento y drift;
  - el flujo de texto, alternativas, confianza y revisión humana es demostrable;
  - la decisión conserva una alternativa visual ya investigada.
- Costes o límites:
  - las narrativas pueden contener información personal residual;
  - los datos no son una muestra representativa del mercado;
  - existe un desbalanceo potencialmente extremo y cambios recientes en el sistema de reclamaciones;
  - el producto predicho no equivale directamente a una cola operativa;
  - las condiciones de reutilización y el método de extracción deben quedar cerrados.
- Trabajo posterior:
  - ejecutar un spike reproducible de datos antes de entrenar;
  - fijar las clases definitivas y la estrategia de desbalanceo con evidencia;
  - comprobar ausencias, duplicados, idioma, leakage y privacidad;
  - definir el mapping configurable entre producto y cola;
  - crear una spec funcional independiente cuando las puertas críticas estén resueltas;
  - registrar en Jira responsables y fechas para las validaciones.

### Evidencia

- `docs/product/candidates/CAND-001-cfpb-complaint-routing.md`.
- `docs/product/candidates/CAND-002-realwaste-classification.md`.
- `docs/product/candidates/comparison-2026-07-22.md`.
- `docs/product/idea_evaluation_template.md`.
- <https://www.consumerfinance.gov/data-research/consumer-complaints/>.
- <https://archive-beta.ics.uci.edu/dataset/908/realwaste>.
