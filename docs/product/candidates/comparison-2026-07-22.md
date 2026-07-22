# Comparación de candidatas — 2026-07-22

- Matriz aplicada: versión `1.0` de [`idea_evaluation_template.md`](../idea_evaluation_template.md).
- Equipo activo: José, Abel, Víctor y Miguel.
- Resultado de la votación: cuatro votos favorables a `CAND-001`; cero votos a `CAND-002`; cero abstenciones.

## Alternativas de la ronda

| ID | Alternativa | Dataset | Estado de la ronda |
|---|---|---|---|
| CAND-001 | Clasificación y enrutamiento de reclamaciones financieras | Consumer Complaint Database del CFPB | Seleccionada con validaciones obligatorias |
| CAND-002 | Clasificación visual de residuos | RealWaste | No seleccionada; alternativa conservada |

## Matriz técnica provisional

Los valores siguientes ordenan la evidencia disponible, pero no representan la mediana de cuatro puntuaciones individuales. La votación unánime se registra por separado y no se ha utilizado para inventar puntuaciones ausentes.

| Criterio | Peso | CAND-001 | Resultado | CAND-002 | Resultado |
|---|---:|---:|---:|---:|---:|
| Valor del problema | 15 % | 4/5 | 12 | 3/5 | 9 |
| Usuario y decisión | 10 % | 4/5 | 8 | 3/5 | 6 |
| Disponibilidad, licencia y reproducibilidad | 15 % | 4/5 | 12 | 4/5 | 12 |
| Calidad y suficiencia de los datos | 10 % | 3/5 | 6 | 3/5 | 6 |
| Encaje multiclase y evaluabilidad | 10 % | 4/5 | 8 | 5/5 | 10 |
| Viabilidad de entrega | 15 % | 3/5 | 9 | 2/5 | 6 |
| UX y capacidad de demostración | 10 % | 4/5 | 8 | 5/5 | 10 |
| Evolución hasta nivel experto | 10 % | 5/5 | 10 | 5/5 | 10 |
| Riesgo y uso responsable | 5 % | 2/5 | 2 | 4/5 | 4 |
| **Resultado ponderado** | **100 %** |  | **75/100** |  | **73/100** |

## Lectura cualitativa

En la preevaluación, las dos candidatas quedaron a menos de cinco puntos, por lo que la diferencia numérica no decidió la selección. La elección se apoya en el voto unánime y en el razonamiento cualitativo documentado; la consolidación formal de puntuaciones sigue pendiente dentro de T-007.

### CAND-001

- Permite comenzar con un baseline reproducible de TF-IDF y clasificación lineal.
- La fuente se actualiza normalmente a diario y permite plantear recolección, feedback y drift lingüístico.
- El flujo de texto, confianza, alternativas y revisión humana es comprensible.
- Presenta mayores riesgos de privacidad, representatividad y desbalanceo; no puede avanzar a entrenamiento sin un spike de viabilidad de datos.

### CAND-002

- Tiene mejor impacto visual y una licencia abierta claramente indicada.
- Encaja de forma directa con redes neuronales y tiene menor exposición a datos personales.
- Su contexto de vertedero no coincide necesariamente con el uso doméstico o industrial que se pudiera plantear.
- En el plazo disponible añade más riesgo de cómputo, integración visual y control del overfitting.

## Decisión

El 22 de julio de 2026, José, Abel, Víctor y Miguel aprobaron por unanimidad seleccionar `CAND-001` como dirección del proyecto.

La aprobación cubre el problema y la candidata de datos; no certifica todavía la calidad del subconjunto de narrativas. Antes de implementar la solución deberán verificarse:

1. extracción filtrada y reproducible;
2. distribución por clase y estrategia frente al fuerte desbalanceo;
3. ausencias, duplicados, idioma y longitud de los textos;
4. riesgo de información personal residual y condiciones de uso;
5. clases definitivas y mapping entre producto y cola;
6. capacidad de alcanzar el nivel esencial antes del 30 de julio.

Si el spike de datos detecta una puerta crítica incumplida, el equipo revisará la decisión y podrá recuperar `CAND-002` sin repetir su investigación.

## Evidencias

- [`CAND-001`](CAND-001-cfpb-complaint-routing.md).
- [`CAND-002`](CAND-002-realwaste-classification.md).
- [Consumer Complaint Database del CFPB](https://www.consumerfinance.gov/data-research/consumer-complaints/).
- [RealWaste en UCI](https://archive-beta.ics.uci.edu/dataset/908/realwaste).
