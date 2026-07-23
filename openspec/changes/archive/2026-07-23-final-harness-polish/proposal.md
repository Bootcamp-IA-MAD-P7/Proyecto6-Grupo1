## Why

El cierre documental del 23 de julio necesita una última revisión reproducible: el diagrama principal debe conservar márgenes correctos y los identificadores de los niveles de entrega no deben partirse en columnas estrechas. El mismo cambio debe demostrar que la presentación profesional del repositorio también queda sometida a OpenSpec, pruebas y evidencia, no a una corrección manual aislada.

## What Changes

- Corregir la geometría y el centrado de las etiquetas del diagrama principal del README.
- Evitar que los identificadores `ESS`, `MED`, `ADV` y `EXP` se dividan al renderizar las tablas.
- Verificar automáticamente la integridad y accesibilidad básica de los SVG documentales.
- Restringir los archivos placeholder a las etapas de datos que todavía necesitan conservar directorios vacíos.
- Ejecutar una auditoría final de estructura, documentación, OpenSpec, dependencias, tests y estado Git.
- Registrar resultados reales sin cambiar el estado de ningún criterio del briefing.

No se modifica el producto, el contrato de datos, la PWA, el backend, el modelo ni el despliegue. Ningún criterio `ESS`, `MED`, `ADV` o `EXP` cambia a `Verificado`.

## Capabilities

### New Capabilities

- `repository-presentation-quality`: presentación documental adaptable, accesible, veraz y protegida por comprobaciones reproducibles.

### Modified Capabilities

- Ninguna.

## Impact

- Documentación raíz y activos SVG del README.
- Comprobaciones de calidad del repositorio y sus tests unitarios.
- Evidencia de validación, changelog y daily del equipo.
- Sin datos CFPB, narrativas, secretos, nuevas dependencias ni cambios de API.
- IDs del briefing afectados: todos se revisan visualmente, pero ninguno cambia de estado.
