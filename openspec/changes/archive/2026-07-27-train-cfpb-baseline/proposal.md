## Why

PG-2 ha cerrado la preparación de datos con un corpus contractual de 1.96M filas en inglés, particionado (70/15/15) y una política que fija macro F1, pesos balanceados y control de overfitting. Sin un baseline evaluable no es posible comparar modelos, medir progreso ni desbloquear ESS-01, ESS-03, ESS-05 y ESS-06 del nivel esencial.

## What Changes

- Crear un pipeline reproducible de preprocesamiento (vectorización TF-IDF) y entrenamiento baseline (regresión logística multinomial) para once clases.
- Evaluar sobre validation con macro F1, accuracy, precision y recall por clase.
- Verificar gap train/validation < 0.05 en macro F1.
- Registrar semillas, configuración y versiones de dependencias.
- Añadir scikit-learn como dependencia.
- Generar artefacto modelo local ignorado por Git y reporte de métricas agregado sin narrativas.

## Capabilities

### New Capabilities
- `cfpb-baseline`: entrenar, evaluar y versionar un baseline reproducible de clasificación multiclase CFPB con once clases, control de overfitting, artefacto local y reporte de métricas agregado.

### Modified Capabilities
- Ninguna.

## Impact

- Dependencias: se añade scikit-learn a `pyproject.toml`.
- Código: scripts de entrenamiento, evaluación y tests en `scripts/ml/` y `tests/unit/`.
- Privacidad: el artefacto modelo y las predicciones se generan localmente; el reporte versionado solo contiene métricas agregadas, no narrativas.
- Seguridad: no se exponen datos, rutas ni configuraciones sensibles.

## Tracking

- Jira: `PG-3`.
