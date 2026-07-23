# Código fuente

## Núcleo encapsulado

- `domain/`: entidades, políticas y puertos sin dependencias de frameworks.
- `application/`: casos de uso y contratos de entrada/salida.
- `infrastructure/`: adaptadores de persistencia, modelos y servicios externos.

## Machine Learning

- `ml/data/`: ingesta, validación y partición.
- `ml/features/`: preprocessing y feature engineering.
- `ml/training/`: entrenamiento y comparación.
- `ml/evaluation/`: métricas multiclase y análisis de errores.

## MLOps

- `mlops/experiments/`: comparaciones reproducibles y A/B.
- `mlops/monitoring/`: calidad, drift y alertas.
- `mlops/registry/`: versiones y compatibilidad.
- `mlops/promotion/`: políticas y reemplazo reversible.

La lógica reutilizable saldrá de los notebooks y se probará desde `tests/`. El dominio no dependerá de la interfaz, la base de datos ni el proveedor de despliegue.

Las capas se materializarán de forma incremental con código real. Este mapa no requiere subcarpetas vacías antes de implementar la primera tarea de cada área.
