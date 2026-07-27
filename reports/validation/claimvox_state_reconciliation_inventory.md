# Inventario de reconciliación de estado — 2026-07-27

## Alcance revisado

| Fuente | Hecho confirmado | Uso documental |
| --- | --- | --- |
| PR #28 `Feature/improved frontend design` | Fusionada en `dev` el 27 de julio; autoría de Abel | ClaimVox, preferencia de tema, ajustes visuales y de accesibilidad de la interfaz |
| PR #25 `integrate complaint routing PWA foundation` | Fusionada y asociada al cambio archivado `integrate-frontend-foundation` | Base de la PWA, mock, dictado, offline y límites de producto |
| PR #27 `prepare CFPB baseline dataset` | Fusionada; constructor y política de preparación | `PG-2` completada; corpus local preparado, sin modelo |
| PR #29 `archive CFPB data preparation changes` | Fusionada; cambios de datos archivados en OpenSpec | Capacidades vigentes de dataset y política de entrenamiento |
| Jira `PG-2` | Estado confirmado por coordinación: `Listo` | El siguiente hito de datos es `PG-3` |

## Estado operativo resultante

| Elemento | Estado verificable | Límite que no cambia |
| --- | --- | --- |
| `PG-2` | Preparación de datos cerrada con evidencia agregada y particiones locales | No hay entrenamiento ni métricas de modelo |
| `PG-3` | Puede iniciar su cambio OpenSpec para entrenar el baseline reproducible | No se ha creado ni evaluado ningún baseline aún |
| `PG-4` | Prototipo React PWA integrado; la identidad visible es ClaimVox | No existe inferencia, backend, autenticación o administración reales |
| `PG-5` | Backend pendiente | Sigue bloqueado hasta disponer de un baseline evaluado y un contrato de integración aprobado |

## Límites de evidencia

- La PR #28 contiene cambios de presentación y test relacionados, pero su
  plantilla de Pull Request quedó sin completar. Esta reconciliación documenta
  únicamente el diff fusionado y no reconstruye comprobaciones no registradas.
- Ninguna fuente revisada contiene narrativas reales del CFPB, datos brutos,
  secretos ni métricas de un modelo.
- No se crea tag ni release: la reconciliación documental no representa una
  versión de producto entregable.
