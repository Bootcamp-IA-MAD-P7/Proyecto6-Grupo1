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

Todos los elementos salvo la estructura de carpetas y la dirección React PWA son responsabilidades previstas. Los contratos de producto, inferencia, persistencia y despliegue se concretarán mediante specs y decisiones.

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
