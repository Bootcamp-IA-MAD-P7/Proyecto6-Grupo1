# Diseño: persistencia gobernada de feedback

## Decisión de arquitectura

La primera implementación será un almacén local aislado detrás de un puerto de
aplicación. La ruta de predicción no escribirá narrativas ni dependerá de que el
almacén esté disponible para devolver una recomendación. La creación de
feedback será una operación explícita y posterior a la revisión humana.

La selección concreta del motor local se fijará en la implementación, siempre
que permita un archivo bajo una raíz controlada, esquema versionado,
migraciones reproducibles y pruebas sin red. No se adoptará una base compartida
ni una dependencia cloud en este cambio.

## Límite de datos

El registro de feedback admitirá solo estos campos de dominio:

| Campo | Finalidad | Regla |
| --- | --- | --- |
| `feedback_id` | Trazabilidad técnica | Identificador generado por el servicio; no representa identidad humana |
| `prediction_id` | Asociar revisión a una predicción | UUID contractual; no contiene narrativa |
| `model_version` | Auditoría del candidato | Obligatorio y no vacío |
| `taxonomy_version` | Compatibilidad de clase | Obligatorio y no vacío |
| `suggested_class` | Contexto de la recomendación | Una de las once clases canónicas |
| `reviewed_class` | Corrección humana opcional | Nula o una de las once clases canónicas |
| `decision` | Resultado de revisión | Vocabulario cerrado aprobado |
| `purpose` | Finalidad de la recogida | Vocabulario cerrado aprobado |
| `created_at` | Auditoría y retención | Marca temporal UTC válida |
| `expires_at` | Retención | Marca temporal UTC posterior a `created_at` |

Quedan prohibidos por contrato campos de texto libre, narrativa, audio,
transcripción, nombre, correo, IP, cuenta, dirección, identificador de sesión,
cabeceras HTTP y cualquier atributo que permita reconstruir la reclamación o
identificar a una persona.

## Operaciones y mínimo privilegio

La interfaz de persistencia separará:

1. `record_feedback`: valida el contrato completo y escribe un registro mínimo.
2. `list_feedback_summary`: devuelve únicamente contadores y agregados por
   versión, clase y decisión; no devuelve registros individuales por defecto.
3. `purge_expired_feedback`: elimina exclusivamente registros vencidos y
   devuelve un contador agregado.

La ruta de predicción no invocará estas operaciones. La futura interfaz de
feedback deberá enviar únicamente campos permitidos y no podrá usar el registro
como sustituto de autenticación o autorización.

## Esquema, migraciones y ubicación

- El esquema incluirá versión de migración y restricciones de tipo, presencia,
  vocabulario y clases canónicas.
- El archivo local se resolverá bajo una raíz configurada y controlada; se
  rechazarán rutas externas o enlaces que escapen de ella.
- La inicialización y migración serán idempotentes y no modificarán datos fuera
  de la raíz controlada.
- Los artefactos locales y cualquier base creada para pruebas permanecerán
  ignorados por Git.

## Retención y exportación

- La retención será finita y configurada explícitamente; no habrá conservación
  indefinida por defecto.
- La purga será invocable de forma segura e idempotente.
- La exportación permitida será agregada y no incluirá identificadores de
  predicción ni registros individuales salvo que una futura decisión aprobada
  defina finalidad, permisos y controles adicionales.

## Estrategia de verificación

Las pruebas usarán un almacén temporal y registros sintéticos. Verificarán:

- aceptación de un feedback conforme;
- rechazo de campos prohibidos, clase no canónica, versiones o fechas inválidas;
- persistencia bajo raíz controlada y rechazo de rutas externas;
- migración e inicialización repetibles;
- retención y purga sin revelar contenido;
- resumen agregado sin narrativas ni identificadores individuales.

La evidencia versionada registrará solo esquema, política, comandos, contadores
y resultados agregados. No se procesarán datos CFPB reales ni se ejecutará
reentrenamiento.

## Riesgos y dependencias

- La persistencia local no proporciona identidad, permisos multiusuario,
  disponibilidad, backup ni recuperación ante desastre.
- `PG-13` no podrá presentarse como recogida operativa de feedback hasta que
  esta base y su interfaz validada estén disponibles.
- `MED-05` requiere además una política posterior de incorporación, validación,
  deduplicación y trazabilidad de conjuntos de reentrenamiento.
