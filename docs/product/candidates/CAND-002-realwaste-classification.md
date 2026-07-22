# CAND-002: Clasificación visual de residuos

| Campo | Valor |
|---|---|
| Estado | No seleccionada |
| Fecha de evaluación | 2026-07-22 |
| Proponente | Equipo |
| Spec | [`000-problem-discovery`](../../../specs/000-problem-discovery/spec.md) |
| Dataset candidato | RealWaste |

## Resumen

Construir una aplicación que reciba una fotografía de un residuo y prediga su tipo de material para apoyar su clasificación. La predicción podría orientar a una persona usuaria u operadora, pero no sustituiría los protocolos locales de separación ni garantizaría por sí sola que un residuo sea reciclable.

## Problema, usuario y decisión

- Problema: clasificar visualmente residuos puede ser confuso cuando existen materiales parecidos, contaminados o mezclados.
- Usuario propuesto: persona u operadora que necesita identificar el tipo de material. El contexto de uso exacto no se validó durante esta ronda.
- Decisión: asignar el residuo a una categoría de material y, mediante reglas externas al modelo, mostrar la actuación recomendada.
- Alternativa actual asumida: inspección visual, cartelería y reglas de separación.
- Momento de inferencia: después de fotografiar el residuo y antes de decidir su clasificación.

El dataset representa residuos fotografiados en un entorno real de vertedero. No demuestra por sí solo que el mismo modelo sea adecuado para fotografías domésticas, puntos limpios o cintas industriales.

## Entrada y salida propuestas

### Entrada inicial

- Una fotografía con un residuo principal visible.
- Sin metadatos de ubicación ni identificadores personales.

### Salida inicial

- Tipo de material predicho.
- Confianza y alternativas principales.
- Solicitud de una nueva fotografía o revisión manual cuando la confianza sea baja.
- Orientación posterior mediante reglas independientes del modelo y adaptadas al contexto de uso.

## Dataset y procedencia

- Nombre: RealWaste.
- Responsable: Sam Single, Saeid Iranmanesh y Raad Raad.
- Repositorio oficial: <https://archive-beta.ics.uci.edu/dataset/908/realwaste>.
- Artículo de referencia: <https://www.mdpi.com/2078-2489/14/12/633>.
- DOI del dataset: <https://doi.org/10.24432/C5SS4G>.
- Licencia indicada por UCI: CC BY 4.0.
- Fecha de consulta: 2026-07-22.

UCI describe RealWaste como un dataset de clasificación de imágenes recogidas en un entorno auténtico de vertedero. La descarga ocupa aproximadamente 656,6 MB y contiene 4.752 imágenes distribuidas en nueve clases.

## Distribución publicada

| Clase | Imágenes | Porcentaje aproximado |
|---|---:|---:|
| Cardboard | 461 | 9,7 % |
| Food Organics | 411 | 8,6 % |
| Glass | 420 | 8,8 % |
| Metal | 790 | 16,6 % |
| Miscellaneous Trash | 495 | 10,4 % |
| Paper | 500 | 10,5 % |
| Plastic | 921 | 19,4 % |
| Textile Trash | 318 | 6,7 % |
| Vegetation | 436 | 9,2 % |
| **Total** | **4.752** | **100 %** |

La relación entre la clase mayoritaria y la minoritaria es aproximadamente 2,9 a 1. Es un desbalanceo relevante pero medible; deberá tratarse mediante particiones estratificadas, métricas macro y técnicas de entrenamiento justificadas.

## Puertas críticas

| Puerta | Estado | Evidencia o condición pendiente |
|---|---|---|
| G-01 Problema y usuario | Condicional | Problema comprensible; contexto y usuario exactos sin validación. |
| G-02 Multiclase real | Cumple | Nueve clases de material mutuamente excluyentes publicadas por UCI. |
| G-03 Datos reproducibles | Cumple | Fuente, descarga, tamaño, DOI y licencia CC BY 4.0 documentados. |
| G-04 Inferencia válida | Condicional | La imagen existe al predecir; falta validar el cambio de dominio entre vertedero y uso propuesto. |
| G-05 Riesgo asumible | Condicional | Riesgo personal bajo; quedan errores de clasificación y recomendaciones locales por gobernar. |
| G-06 Entrega viable | Condicional | Dataset manejable, pero el flujo visual y la red neuronal añaden riesgo de tiempo, cómputo y overfitting. |

## Puntuación técnica preliminar

| Criterio | Peso | Puntuación | Resultado | Justificación resumida |
|---|---:|---:|---:|---|
| Valor del problema | 15 % | 3/5 | 9 | Problema relevante, sin evidencia de usuario o contexto concreto. |
| Usuario y decisión | 10 % | 3/5 | 6 | Decisión comprensible, pero el destino real depende de reglas locales. |
| Disponibilidad, licencia y reproducibilidad | 15 % | 4/5 | 12 | Fuente oficial, descarga y licencia abiertas y documentadas. |
| Calidad y suficiencia de datos | 10 % | 3/5 | 6 | Volumen moderado y distribución conocida; falta revisar imágenes, duplicados y calidad. |
| Encaje multiclase y evaluabilidad | 10 % | 5/5 | 10 | Nueve clases explícitas y métricas por clase aplicables. |
| Viabilidad de entrega | 15 % | 2/5 | 6 | Entrenamiento visual, aplicación y overfitting inferior al 5 % elevan el riesgo dentro del plazo. |
| UX y demostración | 10 % | 5/5 | 10 | La entrada visual y la salida por material permiten una demo inmediata y comprensible. |
| Evolución hasta nivel experto | 10 % | 5/5 | 10 | Encaja de forma natural con CNN, feedback, A/B testing y drift visual. |
| Riesgo y uso responsable | 5 % | 4/5 | 4 | Riesgo personal bajo; deben limitarse recomendaciones erróneas y diferencias locales. |
| **Total** | **100 %** |  | **73/100** | **Viable condicional** |

Esta puntuación es una preevaluación documental y no representa la mediana de puntuaciones individuales del equipo.

## Fortalezas

- Dataset abierto, de tamaño manejable y con distribución publicada.
- Experiencia visual fácil de explicar y demostrar.
- Camino directo hacia una red neuronal y monitorización de drift visual.
- Menor exposición a datos personales que la alternativa de reclamaciones.

## Riesgos y mitigaciones iniciales

| Riesgo | Mitigación propuesta |
|---|---|
| Cambio de dominio | Definir el contexto real y comprobar rendimiento con imágenes similares antes de prometer uso fuera del vertedero. |
| Desbalanceo | Partición estratificada, macro F1, recall por clase y comparación de ponderación o muestreo. |
| Overfitting | Separación protegida de datos, aumentos solo en training, regularización y seguimiento de la brecha train-validation. |
| Fondo y atajos visuales | Auditar errores y comprobar si el modelo aprende escenarios, manos o contenedores en lugar del material. |
| Reglas locales | Separar la predicción de material de la recomendación de reciclaje. |
| Coste de cómputo | Baseline con transfer learning ligero y límites explícitos de experimentación. |

## Motivo de no selección

La alternativa fue considerada viable y obtuvo 73/100. El equipo eligió por unanimidad `CAND-001` porque permite un baseline esencial más rápido con técnicas de texto, dispone de una fuente que evoluciona de forma continua y ofrece un recorrido especialmente claro para feedback y drift. En el plazo disponible, `CAND-002` presentaba mayor riesgo de integración, cómputo y control de overfitting.

La decisión no invalida RealWaste: se conserva como alternativa razonada y reversible si la candidata seleccionada no supera su validación de datos.

## Evidencias

- [RealWaste en UCI Machine Learning Repository](https://archive-beta.ics.uci.edu/dataset/908/realwaste).
- [Artículo introductorio del dataset](https://www.mdpi.com/2078-2489/14/12/633).
- [Licencia CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
