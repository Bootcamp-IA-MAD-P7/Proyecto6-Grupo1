## ADDED Requirements

### Requirement: Protección proporcional de la API local

El servicio de predicción SHALL aplicar un límite configurable de tamaño de entrada, una frecuencia configurable en memoria y cabeceras de respuesta de seguridad compatibles con una API local. SHALL devolver errores contractuales y no revelar contenido, rutas internas ni detalles de implementación.

#### Scenario: Entrada fuera del límite

- **WHEN** una solicitud excede el límite configurado de narrativa
- **THEN** el servicio la rechaza con un error seguro conforme al contrato sin cargar el modelo ni registrar el cuerpo

#### Scenario: Frecuencia superada

- **WHEN** una fuente local supera el umbral de frecuencia configurado
- **THEN** el servicio devuelve una respuesta `429` segura y el cliente puede comunicar una recuperación sin mostrar detalles internos

#### Scenario: Respuesta de la API

- **WHEN** el servicio responde a una ruta de salud o predicción
- **THEN** incluye las cabeceras de seguridad aprobadas y mantiene CORS explícito sin comodines ni credenciales
