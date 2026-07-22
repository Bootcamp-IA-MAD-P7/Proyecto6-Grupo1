# Blueprint arquitectónico

## Objetivo

Preparar una base escalable y testeable con React PWA como frontend inicial, sin fijar prematuramente backend, persistencia o proveedor cloud.

## Vista lógica

```mermaid
flowchart LR
    UI[React PWA] --> APP[Casos de uso]
    API[API opcional] --> APP
    APP --> DOMAIN[Dominio]
    APP --> PORTS[Puertos]
    ADAPTERS[Adaptadores de infraestructura] --> PORTS
    ADAPTERS --> MODEL[Servicio de inferencia]
    ADAPTERS --> DB[(Persistencia)]
    ML[Pipeline ML] --> REGISTRY[Registro de modelos]
    REGISTRY --> MODEL
    MODEL --> EVENTS[Predicciones y feedback]
    EVENTS --> MONITOR[Monitorización]
    MONITOR --> PROMOTION[Evaluación de promoción]
```

La React PWA mock y el contrato OpenAPI de inferencia están implementados y versionados. Los casos de uso reales, servicio, modelo, persistencia, observabilidad y despliegue continúan como responsabilidades previstas que se concretarán mediante specs y decisiones.

React PWA debe cubrir primero el flujo web instalable y responsive. Una aplicación nativa no forma parte del alcance aprobado; se evaluará únicamente si requisitos de dispositivo, distribución o experiencia demuestran que la PWA no es suficiente.

## Estado de implementación y responsabilidad

| Componente | Estado al 22 de julio | Coordinación |
|---|---|---|
| Contrato de datos y target | Implementado para EDA; decisiones finales pendientes | Miguel / arquitectura, Víctor / evidencia EDA |
| EDA del CSV | En curso bajo `001/T-004` | Víctor |
| React PWA y mock | Implementados en PR #14; endurecimiento pendiente | Abel |
| OpenAPI de predicción | Versionado como `contract-only` | Miguel / arquitectura, José / revisión backend |
| Servicio backend | No implementado; integración bloqueada | José |
| Pipeline y modelo | No implementados | Pendiente de resultados de datos/ML |
| Persistencia, despliegue y MLOps | No implementados | Arquitectura futura sujeta a specs |

La responsabilidad identifica quién coordina el área. No convierte un componente pendiente en una capacidad disponible.

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
