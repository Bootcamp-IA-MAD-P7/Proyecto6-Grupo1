# Evaluación de ideas de negocio

- Versión: `1.0`
- Fecha: `2026-07-22`
- Estado: `aprobada por el equipo activo`
- Spec relacionada: [`000-problem-discovery`](../../specs/000-problem-discovery/spec.md)

Esta matriz permite comparar problemas de negocio y datasets con las mismas reglas. La puntuación ordena evidencias, pero no sustituye la decisión del equipo ni permite superar una puerta crítica incumplida.

## Puertas críticas

Una alternativa queda `bloqueada` o `descartada` aunque obtenga una puntuación alta cuando incumple alguna puerta sin una mitigación aceptada.

| ID | Puerta | Condición mínima |
|---|---|---|
| G-01 | Problema y usuario | Existe un usuario identificable y una decisión concreta que la predicción puede mejorar. |
| G-02 | Multiclase real | El target contiene al menos tres clases significativas, mutuamente excluyentes y disponibles como etiqueta. |
| G-03 | Datos reproducibles | El dataset tiene fuente verificable, acceso reproducible y licencia compatible con el uso previsto. |
| G-04 | Inferencia válida | Las variables de entrada existirían en el momento de predecir y no incorporan información futura o posterior. |
| G-05 | Riesgo asumible | No existe un riesgo legal, ético, de privacidad, seguridad o daño que el equipo no pueda mitigar. |
| G-06 | Entrega viable | Es posible construir y verificar el nivel esencial antes del 30 de julio de 2026 con los recursos disponibles. |

Estados permitidos para cada puerta:

- `cumple`: existe evidencia suficiente;
- `condicional`: falta una validación concreta y tiene responsable y fecha límite;
- `bloqueada`: no puede evaluarse todavía;
- `no cumple`: la alternativa se descarta salvo que aparezca evidencia nueva.

## Escala de puntuación

Cada integrante puntúa de forma independiente antes de la puesta en común.

| Puntuación | Significado |
|---:|---|
| 0 | No existe evidencia o contradice el criterio. |
| 1 | Encaje muy débil y riesgos relevantes sin resolver. |
| 2 | Encaje parcial; necesita cambios o validaciones importantes. |
| 3 | Encaje suficiente para el proyecto con riesgos manejables. |
| 4 | Encaje sólido respaldado por evidencia clara. |
| 5 | Encaje excelente, verificable y con riesgos bien controlados. |

No se asignará una puntuación superior a `2` cuando la justificación se base únicamente en una suposición no validada.

## Criterios y pesos

| ID | Criterio | Peso | Qué debe evaluarse |
|---|---|---:|---|
| C-01 | Valor del problema | 15 % | Relevancia, frecuencia, impacto y alternativa actual sin el modelo. |
| C-02 | Usuario y decisión | 10 % | Claridad del usuario, momento de uso y acción que cambia con la predicción. |
| C-03 | Disponibilidad, licencia y reproducibilidad | 15 % | Fuente, condiciones de uso, descarga, documentación y posibilidad de repetir la obtención. |
| C-04 | Calidad y suficiencia de los datos | 10 % | Volumen, clases, desbalanceo preliminar, ausencias, duplicados y representatividad. |
| C-05 | Encaje multiclase y evaluabilidad | 10 % | Semántica de las clases, exclusividad, target y métricas útiles por clase. |
| C-06 | Viabilidad de entrega | 15 % | Complejidad, tiempo, recursos, dependencias y posibilidad de llegar a un producto integrado. |
| C-07 | UX y capacidad de demostración | 10 % | Entrada comprensible, salida accionable, explicación, feedback y claridad de la demo. |
| C-08 | Evolución hasta nivel experto | 10 % | Camino razonable hacia redes neuronales, A/B testing, drift y promoción gobernada. |
| C-09 | Riesgo y uso responsable | 5 % | Leakage, privacidad, sesgo, seguridad, impacto del error y supervisión humana. |
|  | **Total** | **100 %** |  |

La puntuación ponderada de cada criterio se calcula así:

```text
(puntuación / 5) × peso
```

La puntuación consolidada de un criterio será la mediana de las puntuaciones individuales disponibles. Los desacuerdos de dos o más puntos deben comentarse y quedar registrados.

## Interpretación del resultado

| Resultado | Interpretación |
|---:|---|
| 75-100 | Candidata recomendada para la decisión final. |
| 65-74,99 | Viable de forma condicional; requiere resolver riesgos concretos. |
| Menos de 65 | No recomendada para esta entrega. |

Una puntuación no convierte una alternativa en viable cuando una puerta crítica está `bloqueada` o `no cumple`.

## Evidencia mínima por candidato

Antes de declarar una alternativa viable deberá existir:

- problema, usuario, necesidad y decisión descritos;
- target potencial y lista de tres o más clases;
- momento de inferencia y entradas realmente disponibles;
- enlace a la fuente oficial o primaria del dataset;
- licencia y condiciones de acceso comprobadas;
- fecha y método de consulta;
- número de observaciones y variables o formato de los archivos;
- distribución preliminar de clases;
- revisión inicial de ausencias, duplicados y posibles errores;
- análisis preliminar de leakage;
- riesgos de privacidad, sesgo, seguridad e impacto del error;
- flujo de aplicación comprensible;
- estimación de complejidad y recursos;
- camino incremental hasta el nivel experto;
- hechos, inferencias y supuestos claramente separados.

La inspección preliminar no sustituye al EDA completo posterior.

## Mecanismo de aprobación

1. Cada integrante revisa las puertas y puntúa de forma independiente.
2. Se consolida cada criterio mediante la mediana.
3. El equipo revisa puertas, evidencias, desacuerdos y sensibilidad de los pesos.
4. La selección requiere mayoría absoluta del equipo activo —actualmente, al menos tres votos favorables de cuatro integrantes— y ninguna puerta crítica sin resolver.
5. Abstenciones y desacuerdos se registran con su motivo.

La versión `1.0` fue aprobada el 22 de julio de 2026 por Abel, Víctor y Miguel. José estuvo ausente y Josué ya no formaba parte del equipo activo en el momento de la aprobación.

## Desempate

Si dos alternativas quedan a menos de cinco puntos o reciben el mismo número de votos:

1. se revisa primero si alguna presenta menor riesgo en licencia, leakage o privacidad;
2. después se prioriza la mayor viabilidad de entrega antes del 30 de julio;
3. después se compara la evidencia de usuario y decisión;
4. si persiste el empate, se solicita el voto pendiente de cualquier integrante ausente o se registra que todavía no existe selección.

No habrá una persona con voto de calidad ni se elegirá por diferencias decimales.

## Relación con Jira y el repositorio

- Jira mantiene responsables, estado operativo, bloqueos y fechas.
- `specs/000-problem-discovery/` conserva el contrato y la decisión auditable.
- `docs/product/` conserva fichas, comparativas y evidencias de los candidatos.
- Una actualización en Jira no sustituye la modificación versionada de una spec o decisión.
- Cada elemento de Jira relacionado debe enlazar la spec y la tarea correspondiente.

## Plantilla de comparación

| Criterio | Peso | Idea A | Idea B | Idea C |
|---|---:|---:|---:|---:|
| Valor del problema | 15 % |  |  |  |
| Usuario y decisión | 10 % |  |  |  |
| Disponibilidad, licencia y reproducibilidad | 15 % |  |  |  |
| Calidad y suficiencia de los datos | 10 % |  |  |  |
| Encaje multiclase y evaluabilidad | 10 % |  |  |  |
| Viabilidad de entrega | 15 % |  |  |  |
| UX y capacidad de demostración | 10 % |  |  |  |
| Evolución hasta nivel experto | 10 % |  |  |  |
| Riesgo y uso responsable | 5 % |  |  |  |
| **Resultado ponderado** | **100 %** |  |  |  |

## Decisión

Reglas de evaluación aprobadas. La selección de una idea continúa pendiente de evaluación y decisión independiente.

## Evidencias consultadas

- Pendiente de registrar por cada candidato.
