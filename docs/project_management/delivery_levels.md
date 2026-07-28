# Contrato de niveles de entrega

Este documento convierte el briefing en criterios verificables. Es la referencia común para specs, tareas, revisiones, Pull Requests, CI y presentaciones.

## Interpretación acordada

- Los objetivos de cada nivel son obligatorios para declarar ese nivel alcanzado.
- Las tecnologías citadas en el briefing son ejemplos. React PWA es una opción válida para productivizar el modelo.
- Elegir React no reduce el criterio: la aplicación deberá recibir una entrada válida, consumir inferencia real y devolver una predicción multiclase.
- Una capacidad solo cambia a `Verificado` cuando existe evidencia reproducible enlazada.
- Un mock, contrato, notebook aislado, carpeta o documento de intención no demuestra una capacidad implementada.

## Estados

| Estado | Significado |
|---|---|
| `No iniciado` | No existe implementación ni evidencia suficiente |
| `En curso` | Existe trabajo activo, pero aún no cumple el criterio |
| `Bloqueado` | Falta una decisión, dependencia o evidencia obligatoria |
| `Verificado` | El criterio se ha probado y la evidencia está versionada |

## Orden de entrega

```text
Esencial verificado
        ↓
Medio verificado
        ↓
Avanzado verificado
        ↓
Experto verificado
```

Las capas superiores pueden investigarse en paralelo, pero no deben retrasar ni desestabilizar el nivel esencial.

## Nivel esencial

| ID | Criterio obligatorio | Estado | Área | Evidencia mínima para verificar |
|---|---|---|---|---|
| `ESS-01` | Modelo de clasificación funcional con tres o más clases | `En curso` | Datos / ML | Pipeline reproducible, artefacto versionado y predicciones válidas sobre las once clases contratadas |
| `ESS-02` | EDA orientado a clasificación multiclase | `Verificado` | Datos / EDA | `notebooks/01_eda.py`, `reports/validation/cfpb_eda.md`, cuatro figuras agregadas y continuidad trazada con la política de preparación; la correlación numérica no aplica a la entrada textual y al target categórico |
| `ESS-03` | Overfitting inferior al 5 % | `Verificado` | Datos / ML | Macro F1 train/validation y gap `0.0482` documentados en `reports/validation/cfpb_baseline.md` |
| `ESS-04` | Aplicación que productiviza el modelo | `No iniciado` | Frontend / backend | React PWA conectada a inferencia real, con entrada validada, predicción multiclase, errores y revisión humana |
| `ESS-05` | Accuracy global | `Verificado` | Datos / ML | Accuracy en validation (`0.8484`) y test protegido (`0.8230`) con configuración y particiones registradas |
| `ESS-06` | Precision, recall y F1 por clase | `Verificado` | Datos / ML | Métricas por las once clases y agregados macro/weighted en los JSON de `reports/validation/cfpb_baseline_*` |
| `ESS-07` | Matriz de confusión | `En curso` | Datos / ML | Figuras generadas para RF y XGB (sample 50K); pendiente sobre split completo |
| `ESS-08` | Feature importance | `En curso` | Datos / ML | Figuras generadas para RF y XGB (sample 50K); pendiente sobre split completo |
| `ESS-09` | Análisis de errores | `No iniciado` | Datos / ML / producto | Patrones de falsos positivos y negativos por clase, casos límite sanitizados y acciones propuestas |
| `ESS-10` | Informe técnico y guía de ejecución | `No iniciado` | Equipo | Informe coherente con métricas, decisiones, limitaciones y pasos reproducibles |

### Puerta esencial

El nivel esencial solo se declara alcanzado cuando `ESS-01` a `ESS-10` están en `Verificado`. El test final permanece protegido hasta congelar el protocolo de evaluación y seleccionar el modelo.

## Nivel medio

| ID | Criterio obligatorio | Estado | Área | Evidencia mínima para verificar |
|---|---|---|---|---|
| `MED-01` | Modelo ensemble comparado con el baseline | `Verificado` | Datos / ML | RF, XGBoost y LightGBM comparados con LR baseline: XGBoost líder (macro F1 0.6332), LightGBM (0.6175), RF (0.4704) sobre sample 50K; gaps >5% transferidos a MED-03 |
| `MED-02` | Validación cruzada estratificada | `No iniciado` | Datos / ML | `StratifiedKFold` o alternativa justificada, semillas, resultados por fold y variabilidad |
| `MED-03` | Optimización de hiperparámetros | `En curso` | Datos / ML | Optuna implementado en `src/ml/tuning.py`; pendiente ejecución con split completo |
| `MED-04` | Recogida y monitorización de feedback | `No iniciado` | Producto / aplicación | Feedback ligado a versión de modelo, métricas operativas y reglas de privacidad |
| `MED-05` | Recolección de nuevos datos para reentrenamiento | `No iniciado` | Datos / MLOps | Pipeline versionado, validación, trazabilidad, deduplicación y política de incorporación |

### Puerta media

El modelo Champion se elige mediante criterios definidos antes de comparar resultados. El feedback no puede persistir narrativas sin finalidad, retención y permisos aprobados.

## Nivel avanzado

| ID | Criterio obligatorio | Estado | Área | Evidencia mínima para verificar |
|---|---|---|---|---|
| `ADV-01` | Dockerización completa | `No iniciado` | Plataforma | Imágenes reproducibles, configuración por entorno, healthcheck y ejecución documentada |
| `ADV-02` | Base de datos integrada | `No iniciado` | Backend / plataforma | Esquema versionado, migraciones, mínimo privilegio, privacidad y pruebas |
| `ADV-03` | Despliegue en la nube | `No iniciado` | Plataforma | URL o entorno verificable, secretos protegidos, smoke test, observabilidad y reversión |
| `ADV-04` | Tests de integridad de datos | `No iniciado` | Datos / QA | Esquema, nulos, clases, duplicados, leakage y contratos críticos automatizados |
| `ADV-05` | Tests del modelo | `No iniciado` | ML / QA | Carga, preprocesamiento, forma de salida, clases, probabilidades e inferencia controladas |
| `ADV-06` | Tests de métricas mínimas | `No iniciado` | ML / QA | Umbrales aprobados, overfitting y rendimiento por clase convertidos en quality gates |

### Puerta avanzada

La solución debe poder construirse, desplegarse, comprobarse y revertirse sin depender del ordenador de una persona.

## Nivel experto

| ID | Criterio obligatorio | Estado | Área | Evidencia mínima para verificar |
|---|---|---|---|---|
| `EXP-01` | Red neuronal multiclase | `No iniciado` | Datos / ML | Modelo neuronal evaluado con los mismos splits, métricas y límites del Champion |
| `EXP-02` | A/B testing | `No iniciado` | Producto / MLOps | Experimento real o simulación offline reproducible, asignación, métricas y criterio de parada |
| `EXP-03` | Data Drift con alertas | `No iniciado` | Datos / MLOps | Referencia de entrenamiento, datos operativos comparables, umbrales, muestra mínima y alerta verificable |
| `EXP-04` | Sustitución automática gobernada | `No iniciado` | MLOps / plataforma | Champion/Challenger, criterios multiclase, compatibilidad, aprobación, backup, rollback y prueba con un Challenger inferior |

### Puerta experta

El drift genera una señal de revisión; no demuestra por sí solo pérdida de rendimiento. Ningún Challenger se promociona por una única métrica agregada ni si perjudica clases protegidas por mínimos de precision o recall.

## Evidencia transversal obligatoria

Cada criterio verificado debe registrar:

- spec y tareas relacionadas;
- versión o procedencia de los datos;
- código, configuración y artefacto relevantes;
- comandos y resultados;
- informe, tabla, figura o captura cuando corresponda;
- responsable de la revisión;
- riesgos, limitaciones y reversión.

## Estado global actual

| Nivel | Resultado |
|---|---|---|
| Esencial | `4 de 10 verificados`: `ESS-02`, `ESS-03`, `ESS-05` y `ESS-06`; `ESS-01`, `ESS-07` y `ESS-08` en curso; `ESS-04`, `ESS-09` y `ESS-10` pendientes |
| Medio | `1 de 5 verificado` (`MED-01`); `1 en curso` (`MED-03`); resto pendiente |
| Avanzado | `No iniciado` |
| Experto | `No iniciado` |

Este estado debe actualizarse cuando cambie la evidencia, no por calendario ni por intención.
