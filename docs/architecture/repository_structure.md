# Estructura del repositorio

## Principio

La estructura permite crecer hasta nivel experto, pero mantiene desacoplado el núcleo esencial. Las carpetas raíz documentan límites estables; las subcarpetas se crean cuando contienen código, configuración o evidencia real.

No se versionan árboles vacíos para representar capacidades futuras. El mapa siguiente define destinos previstos, no una obligación de materializarlos antes de necesitarlos.

## Capas

| Ruta | Responsabilidad |
|---|---|
| `openspec/` | Cambios, requisitos vigentes y reglas del ciclo de vida. |
| `ai-specs/` | Roles y procedimientos propios que amplían OpenSpec. |
| `.codex/`, `.github/`, `.claude/`, `.cursor/`, `.gemini/` | Adaptadores oficiales por herramienta; no son fuentes de requisitos. |
| `specs/` | Expedientes anteriores conservados para trabajo ya asignado. |
| `data/` | Datos originales, intermedios, procesados y externos. |
| `notebooks/` | Exploración, EDA y experimentos narrativos. |
| `src/domain/` | Reglas, entidades y contratos independientes de frameworks. |
| `src/application/` | Casos de uso y orquestación del dominio. |
| `src/infrastructure/` | Persistencia, artefactos y adaptadores externos. |
| `src/ml/` | Datos, features, entrenamiento y evaluación multiclase. |
| `app/` | Adaptadores de entrega: React PWA, FastAPI y servicios locales. |
| `src/mlops/` | Experimentos, monitorización, registro y promoción. |
| `models/` | Artefactos versionados o metadatos de modelos. |
| `reports/` | Evidencias generadas para evaluación y defensa. |
| `tests/` | Pruebas unitarias, integración, contrato y end-to-end. |
| `infra/` | Contenedores y definición del despliegue. |

## Flujo previsto de datos y modelos

```text
data/raw
   ↓
src/ml/data + src/ml/features
   ↓
data/processed
   ↓
src/ml/training + src/ml/evaluation
   ↓
models/baseline | challengers | champion
   ↓
src/domain ← src/application ← app
   ↑                  ↓
src/infrastructure   feedback y nuevas observaciones
                          ↓
src/mlops/monitoring + experiments + promotion
```

Este flujo es una capacidad estructural prevista, no una afirmación de implementación.

## Evolución sin reorganizaciones

- El nivel esencial usará datos, notebooks, `src/`, un modelo, la app, informes y tests mínimos.
- El nivel medio completa selección, tuning y recolección; el feedback local ya
  está verificado.
- El nivel avanzado completa contenedores, base compartida y despliegue; los
  quality gates locales de datos, modelo y métricas ya están verificados.
- El nivel experto activará experimentos, monitorización, registro y promoción controlada.

Cada ruta aparecerá de forma incremental en la Pull Request que implemente su primera capacidad. Un README puede conservar el contrato futuro sin acompañarse de `.gitkeep` ni subcarpetas vacías.

Los cambios nuevos no crean carpetas numeradas en `specs/`: utilizan `openspec/changes/` y actualizan `openspec/specs/` al archivarse.

## Regla de dependencias

```text
interfaces -> application -> domain
                    ↑
             infrastructure

mlops -> ml + infrastructure
```

El dominio no debe importar frameworks web, librerías de persistencia, proveedores cloud ni detalles de interfaz. Las dependencias externas se conectarán mediante adaptadores.
