# Niveles de entrega y evidencias

Este mapa evita que el nivel experto bloquee una entrega esencial funcional.

## Dependencia general

```text
Esencial estable
    ↓
Medio medido
    ↓
Avanzado operable
    ↓
Experto controlado
```

## Nivel esencial

Debe dejar una solución completa de extremo a extremo.

Evidencias mínimas:

- dataset y licencia/fuente documentados;
- target con tres o más clases y distribución analizada;
- split reproducible sin leakage;
- baseline y pipeline reutilizable;
- métricas globales, macro, weighted y por clase cuando proceda;
- matriz de confusión y análisis de errores;
- comparación train-validation con definición explícita del gap inferior al 5 %;
- aplicación conectada al artefacto real;
- informe y guía de ejecución.

## Nivel medio

Mejora el rendimiento y cierra el ciclo de aprendizaje.

Evidencias mínimas:

- ensemble comparado contra baseline con el mismo protocolo;
- StratifiedKFold y variabilidad entre folds;
- tuning reproducible sin usar el test como conjunto de ajuste;
- modelo Champion elegido mediante reglas previas;
- predicciones y feedback identificables por versión de modelo;
- dataset de nuevas observaciones compatible con reentrenamiento.

## Nivel avanzado

Convierte el experimento en un sistema operable.

Evidencias mínimas:

- contenedores reproducibles;
- persistencia con esquema versionado;
- despliegue documentado;
- configuración y secretos separados;
- tests de datos, pipeline, inferencia, métricas y flujo integrado;
- health/readiness checks y smoke test.

## Nivel experto

Añade experimentación y gobierno de modelos sin poner en riesgo el Champion.

Evidencias mínimas:

- red neuronal evaluada con los mismos splits y métricas;
- Champion/Challenger versionados;
- A/B testing real o simulación offline reproducible;
- referencia de entrenamiento y datos operativos comparables para drift;
- alertas con umbrales y tamaño mínimo de muestra;
- política de promoción con métricas multiclase, overfitting y compatibilidad;
- promoción auditable, reversible y probada con un Challenger inferior;
- documentación de limitaciones: drift no equivale automáticamente a degradación.

## Puertas de seguridad

- El test final se reserva hasta congelar la selección del modelo.
- Un Challenger no se promociona por una única métrica agregada.
- Las clases minoritarias deben respetar mínimos definidos de precision y recall.
- Data Drift genera una señal de revisión; por sí solo no demuestra pérdida de rendimiento.
- La promoción automática requiere artefacto compatible, backup, rollback y evidencia suficiente.
