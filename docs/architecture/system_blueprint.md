# Blueprint arquitectónico

## Objetivo

Mantener una base escalable y testeable con ClaimVox React PWA, FastAPI,
baseline y feedback gobernado como recorrido verificado, sin confundir las
definiciones Docker/PostgreSQL con una entrega cloud ya probada.

## Vista lógica

```mermaid
flowchart LR
    UI[ClaimVox React PWA] --> AUTH[JWT demo por entorno]
    UI --> API[FastAPI]
    API --> APP[PredictionService]
    APP --> PORTS[PredictorInterface]
    PORTS --> MODEL[Baseline local]
    PORTS --> MOCK[Mock seguro]
    ML[Pipeline ML] --> MODEL
    UI --> FEEDBACK[FeedbackService]
    FEEDBACK --> SQLITE[(SQLite local)]
    FEEDBACK --> PG[(PostgreSQL configurado)]
    SQLITE --> SUMMARY[Resumen agregado]
    PG --> SUMMARY
    MODEL -. futuro .-> REGISTRY[Registro de modelos]
    SUMMARY -. futuro .-> CORPUS[Corpus gobernado]
    CORPUS -. futuro .-> MONITOR[Monitorización]
    MONITOR -. futuro .-> PROMOTION[Promoción]
```

La PWA, FastAPI local, `PredictionService`, la interfaz de predictor, el
baseline, el fallback mock y el flujo minimizado de feedback están
implementados y probados. SQLite es el fallback local; Compose puede conectar
PostgreSQL inicializado por un administrador y un usuario de aplicación sin
DDL. Las imágenes, migraciones, operación PostgreSQL y cloud necesitan aún
verificación reproducible. Registro de modelos, corpus, monitorización y
promoción siguen previstos.

React PWA debe cubrir primero el flujo web instalable y responsive. Una aplicación nativa no forma parte del alcance aprobado; se evaluará únicamente si requisitos de dispositivo, distribución o experiencia demuestran que la PWA no es suficiente.

## Límites

### Dominio

Contiene lenguaje y reglas del problema. No conoce Streamlit, Dash, Gradio, HTTP, SQL, Docker ni proveedores cloud.

### Aplicación

Orquesta casos de uso como predecir, registrar feedback o consultar el estado del modelo mediante puertos.

### Infraestructura

Implementa persistencia, carga de artefactos, observabilidad y servicios externos. Es reemplazable sin modificar el dominio.

### ML

Construye artefactos reproducibles y metadatos compatibles con el contrato de inferencia.

### MLOps

Observa, compara y propone cambios de versión. La promoción debe estar gobernada, auditada y ser reversible.

## Reglas de escalabilidad

- Procesos de entrenamiento separados de la inferencia online.
- Artefactos inmutables y versionados.
- Configuración externa al código.
- Contratos estables entre aplicación y modelo.
- Persistencia detrás de interfaces.
- Operaciones idempotentes cuando sea posible.
- Observabilidad sin registrar datos sensibles.
