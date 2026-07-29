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
| `ESS-01` | Modelo de clasificación funcional con tres o más clases | `Verificado` | Datos / ML | Baseline local reproducible, artefacto ignorado con manifiesto y predicciones válidas sobre las once clases; `reports/validation/cfpb_essential_evaluation.md` |
| `ESS-02` | EDA orientado a clasificación multiclase | `Verificado` | Datos / EDA | `notebooks/01_eda.py`, `reports/validation/cfpb_eda.md`, cuatro figuras agregadas y continuidad trazada con la política de preparación; la correlación numérica no aplica a la entrada textual y al target categórico |
| `ESS-03` | Overfitting inferior al 5 % | `Verificado` | Datos / ML | Macro F1 train/validation y gap `0.0482` documentados en `reports/validation/cfpb_baseline.md` |
| `ESS-04` | Aplicación que productiviza el modelo | `Verificado` | Frontend / backend | ClaimVox envía solo la narrativa al servicio local configurado, valida la respuesta contractual, maneja errores de forma segura y mantiene revisión humana. Evidencia: `reports/validation/claimvox_local_inference_smoke.md` y PR `#40` fusionada |
| `ESS-05` | Accuracy global | `Verificado` | Datos / ML | Accuracy en validation (`0.8484`) y test protegido (`0.8230`) con configuración y particiones registradas |
| `ESS-06` | Precision, recall y F1 por clase | `Verificado` | Datos / ML | Métricas por las once clases y agregados macro/weighted en los JSON de `reports/validation/cfpb_baseline_*` |
| `ESS-07` | Matriz de confusión | `Verificado` | Datos / ML | Matriz normalizada sobre validation completo en `reports/validation/figures/cfpb_baseline_validation_confusion_matrix.png` |
| `ESS-08` | Feature importance | `Verificado` | Datos / ML | Coeficientes TF-IDF agregados y limitaciones en `reports/validation/cfpb_essential_evaluation.md` |
| `ESS-09` | Análisis de errores | `Verificado` | Datos / ML / producto | Clases débiles, confusiones agregadas y acciones de revisión humana en `reports/validation/cfpb_essential_evaluation.md` |
| `ESS-10` | Informe técnico y guía de ejecución | `Verificado` | Equipo | Informe de evaluación y `docs/project_management/essential_delivery_guide.md` |

### Puerta esencial

El nivel esencial solo se declara alcanzado cuando `ESS-01` a `ESS-10` están en `Verificado`. El test final permanece protegido hasta congelar el protocolo de evaluación y seleccionar el modelo.

## Nivel medio

| ID | Criterio obligatorio | Estado | Área | Evidencia mínima para verificar |
|---|---|---|---|---|
| `MED-01` | Modelo ensemble comparado con el baseline | `Verificado` | Datos / ML | RF, XGBoost y LightGBM comparados con LR baseline: XGBoost líder (macro F1 0.6332), LightGBM (0.6175), RF (0.4704) sobre sample 50K; gaps >5% transferidos a MED-03 |
| `MED-02` | Validación cruzada estratificada | `No iniciado` | Datos / ML | `StratifiedKFold` o alternativa justificada, semillas, resultados por fold y variabilidad |
| `MED-03` | Optimización de hiperparámetros | `En curso` | Datos / ML | Optuna implementado en `src/ml/tuning.py`; pendiente ejecución con split completo |
| `MED-04` | Recogida y monitorización de feedback | `En curso` | Producto / aplicación | Persistencia local minimizada ligada a versión y privacidad; faltan interfaz, métricas operativas y operación compartida |
| `MED-05` | Recolección de nuevos datos para reentrenamiento | `En curso` | Datos / MLOps | Registro local trazable con finalidad acotada; faltan pipeline, validación, deduplicación y política de incorporación |

### Puerta media

El modelo Champion se elige mediante criterios definidos antes de comparar resultados. El feedback no puede persistir narrativas sin finalidad, retención y permisos aprobados.

## Nivel avanzado

| ID | Criterio obligatorio | Estado | Área | Evidencia mínima para verificar |
|---|---|---|---|---|
| `ADV-01` | Dockerización completa | `No iniciado` | Plataforma | Imágenes reproducibles, configuración por entorno, healthcheck y ejecución documentada |
| `ADV-02` | Base de datos integrada | `No iniciado` | Backend / plataforma | Esquema versionado, migraciones, mínimo privilegio, privacidad y pruebas |
| `ADV-03` | Despliegue en la nube | `No iniciado` | Plataforma | URL o entorno verificable, secretos protegidos, smoke test, observabilidad y reversión |
| `ADV-04` | Tests de integridad de datos | `Verificado` | Datos / QA | Puerta local con columnas, once clases, nulos, conflictos y fuga por `narrative_hash`; 6 pruebas sintéticas |
| `ADV-05` | Tests del modelo | `Verificado` | ML / QA | Puerta local de carga controlada, feature permitida, clases, probabilidades e inferencia sintética; 5 pruebas |
| `ADV-06` | Tests de métricas mínimas | `Verificado` | ML / QA | Puerta local para métricas agregadas, clases, gap estricto y prohibición de selección con test; 5 pruebas |

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
| Esencial | `10 de 10 verificados`: evidencia enlazada para `ESS-01` a `ESS-10`; la ejecución sigue siendo local y no acredita despliegue |
| Medio | `1 de 5 verificado` (`MED-01`); `1 en curso` (`MED-03`); resto pendiente |
| Avanzado | `No iniciado` |
| Experto | `No iniciado` |

Este estado debe actualizarse cuando cambie la evidencia, no por calendario ni por intención.
