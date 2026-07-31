# Modelo de amenazas

> Estado: amenazas de predicción y feedback definidas. SQLite y retención están
> verificadas. JWT demo y PostgreSQL están integrados por configuración, pero
> identidad compartida, migraciones, despliegue verificado y operación
> productiva siguen pendientes.

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
| Texto excesivo o malicioso | Consumo de recursos o fallo | Máximo contractual de 5.000 caracteres, configuración local más restrictiva y error seguro | Validación semántica y límites de despliegue pendientes |
| Automatización abusiva | Coste o indisponibilidad | Bearer token demo, `429` y 20 predicciones/minuto por cliente temporal en memoria | Identidad, control distribuido y protección pública pendientes |
| Modelo no disponible o manipulado | Resultado incorrecto | Versión obligatoria, `503` y carga desde origen controlado | Registro y firma de artefactos pendientes |
| Falsa confianza | Decisión humana errónea | Confianza nula permitida y revisión obligatoria | Calibración y umbral pendientes |
| Uso como decisión financiera | Daño o incumplimiento | Lenguaje de apoyo, sin routing automático ni acciones financieras | Validación de usuario y gobernanza |
| Inferencia offline simulada | Resultado ficticio | PWA offline solo para shell y explicación | Estrategia de disponibilidad pendiente |
| Errores con detalles internos | Filtración técnica | `ErrorResponse` seguro sin body ni stack, con pruebas contractuales | Revisión por entorno y observabilidad de incidentes pendientes |
| Feedback con texto o identidad | Exposición de información sensible | Bearer token, esquema cerrado, campos prohibidos y errores que no reflejan valores | Autorización multiusuario para operación compartida pendiente |
| Credenciales embebidas | Acceso no autorizado | Compose exige secretos externos y el fallback JWT es efímero | Rotación y gestor de secretos del entorno pendiente |
| Token demo en `localStorage` | Robo del token si existe XSS en el navegador | CSP/Nginx, dependencias auditadas, sesión temporal y ausencia de narrativas persistidas | Sustituir por cookies `HttpOnly`, CSRF y proveedor de identidad antes de producción |
| Retención indefinida | Acumulación innecesaria | Expiración UTC, purga idempotente y política local de 30 días | Scheduler y verificación operativa pendientes |
| Exportación de registros | Reidentificación o uso no previsto | Solo resumen agregado; no existe endpoint de registros individuales | Gobierno de analítica futura pendiente |

## Decisiones todavía necesarias

- Proveedor de identidad y autorización para producción; el JWT demo no lo sustituye.
- CORS, cabeceras y rate limits de despliegue por entorno; los controles actuales son solo locales y en memoria.
- Límite de tamaño e idioma aceptado.
- Autorización por rol del feedback antes de cualquier operación compartida.
- Migraciones, backup y restauración para PostgreSQL.
- Proveedor, red, registro y observabilidad.
- Respuesta ante incidentes específica del servicio.

El contrato reduce el alcance inicial, pero no certifica seguridad de una implementación futura.
