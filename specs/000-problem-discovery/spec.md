# SPEC: Selección del problema de negocio

- ID: `000`
- Estado: `active`
- Responsable: `Equipo`
- Fecha: `2026-07-21`

## Contexto y problema

El proyecto necesita seleccionar un problema real y un dataset adecuado para construir una solución de clasificación supervisada multiclase. Al iniciar esta spec no existía una idea de negocio aprobada y esa ausencia era deliberada: elegir por intuición, por disponibilidad inmediata de un dataset o por preferencia tecnológica podía producir una solución sin utilidad, con clases artificiales, leakage o riesgos no asumibles.

El equipo necesita un proceso común, comparable y trazable para proponer alternativas, contrastar sus datos y registrar una decisión antes de comenzar EDA, modelado o diseño funcional.

## Usuario y necesidad

El usuario inmediato de esta spec es el equipo activo formado por José, Abel, Víctor y Miguel. Necesita decidir qué problema abordar con evidencia suficiente para explicar:

- quién utilizaría la predicción;
- qué decisión mejoraría;
- por qué se necesitan tres o más clases;
- qué datos permitirían realizar la predicción en el momento correcto;
- qué riesgos y límites condicionan la solución;
- por qué la alternativa elegida es viable dentro del proyecto.

Docentes, personas evaluadoras y colaboradores posteriores necesitan poder auditar cómo se tomó la decisión.

## Objetivo observable

Concluir el descubrimiento con una decisión explícita y versionada que:

1. seleccione una combinación de problema, usuario, decisión y dataset candidato; o
2. rechace todas las alternativas cuando ninguna cumpla los criterios mínimos.

La salida deberá estar respaldada por evidencias comparables y proporcionar entradas suficientes para redactar la primera spec funcional, sin iniciar todavía su implementación.

## Alcance

### Incluido

- Recoger propuestas de problemas e ideas de negocio.
- Definir y aprobar la escala, pesos y umbrales de evaluación antes de puntuar.
- Describir usuario, necesidad y decisión asociada a cada candidato.
- Comprobar el encaje con clasificación multiclase.
- Identificar datasets candidatos, fuente, licencia y condiciones de acceso.
- Realizar una inspección preliminar de datos cuando el acceso y la licencia lo permitan.
- Evaluar calidad, volumen, clases, disponibilidad temporal, leakage, privacidad y sesgo.
- Valorar viabilidad de aplicación, UX, demo, despliegue y evolución hasta nivel experto.
- Comparar alternativas con la misma matriz y conservar evidencias.
- Registrar ideas descartadas, motivos, incertidumbres y decisión final.
- Preparar el traspaso hacia la primera spec funcional.

### Fuera de alcance

- Ejecutar un EDA completo.
- Entrenar, optimizar o seleccionar modelos.
- Fijar la métrica principal definitiva sin conocer el coste de los errores.
- Diseñar pantallas o formularios ligados a variables no aprobadas.
- Elegir framework de aplicación, base de datos o proveedor cloud.
- Construir pipelines de datos, Docker, despliegue o MLOps.
- Presentar una idea candidata como producto aprobado antes de registrar la decisión.

## Escenarios

### Principal

1. El equipo acuerda las reglas de evaluación.
2. Se registran las ideas candidatas con el mismo nivel mínimo de información.
3. Cada problema supera o falla las puertas de valor, encaje multiclase, datos y riesgo.
4. Los candidatos viables se comparan con una matriz común y evidencias enlazadas.
5. El equipo registra la alternativa elegida y por qué supera a las demás.
6. La decisión proporciona las entradas para crear una spec funcional independiente.

### Alternativos y errores

1. Si una idea no identifica usuario y decisión, permanece incompleta y no se puntúa como viable.
2. Si el target no contiene tres o más clases significativas y mutuamente excluyentes, la idea se descarta para este proyecto.
3. Si el dataset carece de licencia compatible, acceso reproducible o documentación suficiente, se bloquea o descarta.
4. Si las variables necesarias no existirían en el momento real de inferencia, se registra riesgo de leakage y la idea no avanza sin mitigación.
5. Si los datos implican riesgos legales, éticos o de privacidad no asumibles, la idea se descarta aunque su puntuación sea alta.
6. Si dos alternativas quedan próximas, el equipo revisa evidencias y sensibilidad de los pesos; no fuerza una decisión por decimales.
7. Si ninguna alternativa cumple los mínimos, se registra la no selección y se abre una nueva ronda de investigación.
8. Si aparece nueva evidencia antes del cierre, se actualizan todos los candidatos afectados y se conserva la trazabilidad del cambio.

## Requisitos

- R-001: Cada candidato debe declarar problema, usuario, necesidad y decisión que la predicción pretende mejorar.
- R-002: Cada candidato debe justificar un target categórico con al menos tres clases significativas y mutuamente excluyentes.
- R-003: Cada dataset candidato debe registrar fuente, licencia, acceso, responsable y fecha de consulta.
- R-004: La evaluación de datos debe revisar, como mínimo, volumen, variables, target, distribución preliminar de clases, valores ausentes, duplicados y documentación disponible.
- R-005: Debe comprobarse que las variables de entrada estarían disponibles en el momento real de inferencia y señalar posibles fuentes de leakage.
- R-006: Deben identificarse datos personales o sensibles, riesgos de sesgo, población afectada y posibles usos indebidos.
- R-007: Todos los candidatos deben evaluarse con la misma versión de la matriz, escala y pesos, acordados antes de la puntuación comparativa.
- R-008: La puntuación debe acompañarse de evidencia y razonamiento; no puede sustituir la decisión del equipo.
- R-009: La evaluación debe incluir viabilidad de una aplicación comprensible, potencial de demo y camino incremental hasta nivel experto.
- R-010: Las ideas descartadas deben conservar su motivo y evidencia para evitar repetir investigación.
- R-011: La decisión final debe identificar problema, usuario, decisión, dataset candidato, target propuesto, clases, riesgos, supuestos y validaciones posteriores.
- R-012: No se iniciará implementación funcional hasta que la decisión esté aceptada y no existan preguntas bloqueantes sobre problema, datos y clases.
- R-013: El resultado debe sincronizarse con `decisions.md`, README, hechos de proyecto, estado técnico, daily y fuentes de NotebookLM.

## Criterios de aceptación

- AC-001: Dado el inicio de la evaluación, cuando se puntúe el primer candidato, entonces la escala, pesos, umbrales y mecanismo de aprobación ya están registrados.
- AC-002: Dada una idea candidata, cuando se revise su ficha, entonces contiene problema, usuario, decisión y justificación multiclase o figura explícitamente como incompleta.
- AC-003: Dado un dataset candidato, cuando se evalúe su viabilidad, entonces constan fuente, licencia, acceso, target potencial, clases y riesgos de calidad.
- AC-004: Dada una variable sospechosa, cuando pueda contener información futura o posterior a la decisión, entonces queda marcada como riesgo de leakage y no se considera válida sin mitigación documentada.
- AC-005: Dadas varias alternativas, cuando se comparen, entonces utilizan la misma matriz y enlazan evidencias verificables para cada puntuación.
- AC-006: Dado un riesgo legal, ético, de privacidad o sesgo, cuando no exista una mitigación proporcionada, entonces la alternativa queda bloqueada o descartada con motivo.
- AC-007: Dada una puntuación cuantitativa, cuando se tome la decisión, entonces el equipo registra también razonamiento cualitativo y sensibilidad a los criterios relevantes.
- AC-008: Dado que ninguna idea cumple los mínimos, cuando finalice la ronda, entonces se registra una decisión de no selección sin inventar un ganador.
- AC-009: Dada una idea seleccionada, cuando se cierre la spec, entonces `decisions.md` contiene la decisión, alternativas, consecuencias, riesgos y evidencia.
- AC-010: Dada la decisión aceptada, cuando se prepare el siguiente trabajo, entonces se crea una nueva spec funcional y esta spec no contiene implementación de producto.

## Requisitos no funcionales

- Trazabilidad: toda afirmación relevante debe enlazar una fuente, inspección o decisión.
- Comparabilidad: todos los candidatos deben utilizar la misma versión de criterios durante una ronda.
- Reproducibilidad: las consultas y comprobaciones de datos deben registrar fecha, fuente y método.
- Seguridad: no se incorporarán secretos, credenciales ni muestras sensibles al repositorio.
- Privacidad: se aplicará minimización de datos desde la evaluación inicial.
- Claridad: una persona ajena a la decisión debe poder comprender por qué se eligió o descartó cada alternativa.
- Reversibilidad: seleccionar una idea no elimina el historial de candidatos ni impide revisar la decisión ante evidencia nueva.

## Preguntas abiertas

- [x] Q-001: La versión `1.0` de `docs/product/idea_evaluation_template.md` fija escala, pesos y umbrales.
- [x] Q-002: La versión `1.0` fija la evidencia mínima obligatoria antes de declarar viable un candidato.
- [x] Q-003: La selección requiere mayoría absoluta del equipo activo y aplica un desempate basado en riesgo, plazo y evidencia de usuario.
- [x] Q-004: Jira será el tablero operativo y el repositorio conservará los contratos y decisiones; el enlace del proyecto se registrará cuando se cree.

Estas preguntas deben resolverse antes de puntuar o seleccionar alternativas, pero no requieren una idea de negocio previa.

## Evidencia de cierre esperada

- Matriz de evaluación con versión, escala, pesos y responsables.
- Ficha y evidencias de cada alternativa considerada.
- Comprobación preliminar de cada dataset viable.
- Registro de riesgos de leakage, privacidad, sesgo y licencia.
- Comparativa final y análisis de sensibilidad cuando sea relevante.
- Decisión aceptada o decisión explícita de no selección.
- Motivos de descarte conservados.
- Documentación y fuentes de NotebookLM sincronizadas.
- Enlace a la nueva spec funcional cuando exista una selección.
