# Diseño: usabilidad de clasificación local

## Principios de presentación

La pantalla de clasificación es la superficie funcional de ClaimVox. Debe
mostrar el resultado contractual sin convertirlo en una decisión automática:
la clase sugerida, la confianza disponible y la versión del modelo informan la
revisión humana, no enrutan una reclamación.

La interfaz no inferirá el origen de una respuesta. El cliente utilizará la
señal contractual de fuente para distinguir `local_api` de `mock`; cuando la
respuesta no tenga una puntuación calibrada, lo indicará sin fabricar un valor.

## Formulario y ciclo de petición

- Antes de enviar, el formulario mantiene los límites y advertencias de
  privacidad existentes.
- Durante la petición, el control de clasificación comunicará carga y evitará
  dobles envíos.
- Ante configuración inválida, indisponibilidad de la API o error contractual,
  el mensaje explicará la recuperación local sin revelar entradas ni detalles
  internos.
- El inicio de una clasificación nueva restablecerá el estado visual anterior.

## Resultado

- Encabezado: etiqueta de predicción local o de respuesta mock, clase sugerida
  y estado obligatorio de revisión humana.
- Resumen: confianza solo cuando exista, versión/taxonomía como metadato
  secundario y motivo de revisión contractual o seguro por defecto.
- Alternativas: mostrar como máximo tres, en el orden recibido por el contrato;
  si no hay alternativas, explicitarlo en vez de renderizar una lista vacía.
- La respuesta mock conservará una advertencia visible de que no procede de un
  modelo ni puede utilizarse para enrutar.

## Textos seguros aprobados

| Estado | Texto de interfaz |
| --- | --- |
| Respuesta desde API local | `Local prediction response. Human review remains required before any routing or final decision.` |
| Respuesta mock | `Mock response. This synthetic response was not produced by a model and cannot route a complaint.` |
| Revisión sin motivo contractual | `Human review is required before any routing or final decision.` |
| Solicitud en curso | `Creating a classification. Please wait.` |
| Error recuperable | `The prediction service is unavailable. Your narrative was not stored. Try again after checking the local service.` |
| Reinicio | `Start a new classification` devuelve al formulario sin conservar el resultado mostrado. |

El texto de API local describe el transporte configurado; la interfaz seguirá
mostrando la versión contractual y no afirmará que existe un modelo desplegado
ni que una respuesta local constituye una decisión automática.

## Límite administrativo

Las rutas administrativas conceptuales no se enlazarán desde el recorrido de
clasificación ni se usarán como evidencia del servicio local. Esta tarea no
añade permisos, datos operativos, trabajos de entrenamiento ni indicadores de
salud a dichas rutas.

## Verificación

Las pruebas de componentes usarán contratos sintéticos para cubrir respuesta
local, mock, carga, error, alternativas limitadas y motivo de revisión. La
revisión manual local usará un texto sintético contra la API configurada y
registrará solo el estado agregado del recorrido; no incluirá narrativas CFPB.
