# Modelo de amenazas

> Estado: amenazas iniciales de la experiencia de predicción definidas; autenticación, persistencia y despliegue siguen pendientes.

## Activos

- Datos de entrenamiento.
- Datos introducidos por usuarios.
- Feedback y resultados reales.
- Artefactos y metadatos de modelos.
- Credenciales y configuración.
- Servicio de predicción.
- Taxonomía y versión del contrato de inferencia.

## Límites de confianza

- Usuario e interfaz.
- Aplicación e inferencia.
- Aplicación y persistencia.
- CI/CD y cloud.
- Pipeline de entrenamiento y registro.

## Amenazas por analizar

- Entradas maliciosas o fuera de dominio.
- Exposición de secretos.
- Dependencias comprometidas.
- Manipulación de datos o artefactos.
- Acceso no autorizado a feedback.
- Logs con información sensible.
- Promoción incorrecta de modelos.
- Abuso o indisponibilidad del servicio.

## Experiencia de predicción v1

| Amenaza | Impacto | Control inicial | Riesgo pendiente |
|---|---|---|---|
| Información personal en la narrativa | Exposición en logs o terceros | Aviso de minimización, body logging prohibido y no persistencia por defecto | Redacción adicional y revisión de privacidad |
| Texto excesivo o malicioso | Consumo de recursos o fallo | Validación estricta y error seguro reservado en contrato | Longitud máxima pendiente del EDA y operación |
| Automatización abusiva | Coste o indisponibilidad | Respuesta `429` y política de frecuencia antes de despliegue | Umbral y autenticación pendientes |
| Modelo no disponible o manipulado | Resultado incorrecto | Versión obligatoria, `503` y carga desde origen controlado | Registro y firma de artefactos pendientes |
| Falsa confianza | Decisión humana errónea | Confianza nula permitida y revisión obligatoria | Calibración y umbral pendientes |
| Uso como decisión financiera | Daño o incumplimiento | Lenguaje de apoyo, sin routing automático ni acciones financieras | Validación de usuario y gobernanza |
| Inferencia offline simulada | Resultado ficticio | PWA offline solo para shell y explicación | Estrategia de disponibilidad pendiente |
| Errores con detalles internos | Filtración técnica | `ErrorResponse` seguro sin body ni stack | Implementación y pruebas pendientes |

## Decisiones todavía necesarias

- Autenticación y autorización para demo y producción.
- CORS, cabeceras y rate limits por entorno.
- Límite de tamaño e idioma aceptado.
- Política de retención si se incorpora feedback.
- Proveedor, red, registro y observabilidad.
- Respuesta ante incidentes específica del servicio.

El contrato reduce el alcance inicial, pero no certifica seguridad de una implementación futura.
