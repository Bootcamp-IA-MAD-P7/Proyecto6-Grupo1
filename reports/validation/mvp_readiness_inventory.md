# Inventario de preparación MVP

> Fecha de revisión: 28 de julio de 2026
> Cambio OpenSpec: `mvp-readiness-and-presentation`
> Alcance: inventario técnico; no se modifica el comportamiento de la aplicación.

## Resultado ejecutivo

ClaimVox dispone de un recorrido de inferencia **local** con un artefacto de
baseline cuando éste existe en la máquina. El navegador no accede al CSV del
CFPB, al artefacto del modelo ni a las narrativas de entrenamiento. La interfaz
usa un contrato tipado y puede seguir mostrando una respuesta sintética cuando
el servicio local o el artefacto no están disponibles.

No es un servicio desplegado ni una aplicación con cuentas reales. La identidad
visual y la autenticación guardadas en el navegador son propuestas mock
claramente separadas del recorrido de clasificación.

## API local

| Área | Estado confirmado | Evidencia revisada |
|---|---|---|
| Rutas | `POST /api/v1/predictions` y `GET /api/v1/health` | `app/api/routes/` |
| Encapsulamiento | La ruta delega en `PredictionService`, que usa una interfaz de predictor con implementaciones baseline y mock | `app/api/services/`, `app/api/predictors/` |
| Predicción real | Se carga `models/cfpb_baseline.pkl` local cuando existe; si no, se usa mock y salud degradada | `app/api/main.py`, `app/api/predictors/baseline.py` |
| Contrato | La solicitud solo admite narrativa y un identificador técnico opcional; se prohíben campos extra | `app/api/schemas/request.py` |
| CORS y cabeceras | Orígenes locales explícitos, sin comodines ni credenciales; respuestas sin caché, sin referrer, sin sniffing y sin framing | `app/api/config.py`, `app/api/main.py`, `tests/contract/test_backend_cors.py` |
| Errores y límites | Respuestas seguras para validación y frecuencia; narrativa máxima de 5.000 caracteres y 20 predicciones/minuto por cliente temporal en memoria | `app/api/config.py`, `app/api/errors.py`, `app/api/security.py`, `tests/unit/test_api_local_controls.py` |
| Eventos técnicos | Un evento de finalización sin contenido, identidad, IP, predicción individual ni alternativas | `app/api/observability.py`, `tests/unit/test_api_local_controls.py` |
| Persistencia | No hay base de datos ni almacenamiento de solicitudes | `app/api/README.md`, `app/api/services/prediction_service.py` |

## PWA e interfaz

| Área | Estado confirmado | Evidencia revisada |
|---|---|---|
| Transporte | Cliente HTTP tipado, timeout y tratamiento de `429` | `app/interface/src/services/http-prediction-transport.ts` |
| Datos de reclamación | La narrativa no se guarda en `localStorage`, `sessionStorage`, IndexedDB, caché, URL ni consola | `app/interface/README.md`, PWA y servicios de interfaz |
| Offline | La PWA conserva la interfaz; una predicción requiere el servicio local disponible | `app/interface/README.md`, política PWA |
| Preferencia visual | Solo el tema se guarda localmente | `app/interface/src/providers/ThemeProvider.tsx` |
| Login | La identidad mock se guarda solo para la propuesta visual y no proporciona autenticación ni autorización reales | `app/interface/src/services/auth-client.ts` |

## Controles locales aplicados y límites reales

| Control | Estado | Próxima acción dentro del cambio |
|---|---|---|
| Prohibición de logs de narrativa | Aplicada por diseño, contrato y prueba de eventos | Mantener la lista explícita de campos prohibidos en cambios futuros |
| CORS local estricto | Implementado y cubierto por contrato | Conservar orígenes explícitos al cambiar el entorno local |
| Errores seguros | Implementados para validación, límite y frecuencia | Revisar por entorno antes de un despliegue público |
| Tamaño máximo de narrativa | Máximo contractual de 5.000 caracteres; configuración local solo más restrictiva | Validación semántica posterior, si la evidencia la justifica |
| Frecuencia de peticiones | 20/minuto por cliente temporal, en memoria, con `429` seguro | Diseñar un control distribuido antes de varias instancias o exposición pública |
| Cabeceras de seguridad | `no-store`, `no-referrer`, `nosniff` y `DENY` aplicadas a la API local | Añadir políticas HTTPS/de despliegue solo cuando exista ese entorno |
| Observabilidad | Evento técnico local sin identidad ni contenido | Definir propósito, retención y acceso antes de persistir eventos |
| Autenticación, base de datos y despliegue | No implementados | Fuera de alcance de este cambio |

## Incoherencias documentales detectadas

- El primer párrafo de `app/api/README.md` afirma que la evidencia local no
  implica que ClaimVox consuma el servicio, mientras que sus secciones de
  integración local y limitaciones sí documentan ese recorrido. Debe aclararse
  que ClaimVox puede consumirlo **solo localmente y bajo configuración
  explícita**.
- El modelo de amenazas identificaba límites, cabeceras, frecuencia y
  observabilidad como pendientes. Este cambio los aplica de forma local y los
  cubre con pruebas; las protecciones de despliegue siguen pendientes.

## Límites de la revisión

No se han ejecutado llamadas CFPB, pruebas de carga ni despliegue. Las
conclusiones se basan en código, contrato, documentación y pruebas versionadas.
La prueba local posterior usa únicamente texto sintético; no se han revisado ni
almacenado narrativas reales.

## Auditoría estructural y prueba local posterior

La revisión de fronteras confirma que el backend mantiene una separación
proporcional para el MVP: rutas HTTP, servicio de predicción, interfaz de
predictor, implementaciones de predictor, configuración, control local y
observabilidad. La interfaz separa contrato, transporte HTTP, selector de modo,
PWA, dictado y componentes de presentación. No se detectó una dependencia
circular, acceso del navegador a datos de entrenamiento ni duplicación que
justifique una reescritura.

Como mejora de bajo riesgo se han aislado los controles nuevos en
`app/api/security.py` y `app/api/observability.py`; las rutas conservan la
orquestación y no cambian OpenAPI, las once clases ni la revisión humana.

Tras incorporar los controles se ejecutó una llamada local con artefacto real y
texto sintético. Resultado agregado: salud `200` en estado `ok`, predicción
`200`, modo real, revisión humana obligatoria, ausencia de eco de entrada y
recorrido HTTP de `9 ms`. No se guardó la narrativa sintética, el cuerpo de la
respuesta ni el artefacto.
