# Revisión del contrato para persistencia de feedback

Fecha de revisión: `2026-07-29`

Cambio OpenSpec: `add-governed-feedback-persistence`

Jira: `PG-14`

## Fuentes revisadas

- `openspec/specs/prediction-service/spec.md`
- `app/interface/src/contracts/prediction.ts`
- `openspec/changes/add-governed-feedback-persistence/design.md`

## Campos de procedencia permitidos

| Campo de feedback | Procedencia o regla | Finalidad |
| --- | --- | --- |
| `feedback_id` | Generado localmente | Trazabilidad técnica sin identidad |
| `prediction_id` | `PredictionResponse.prediction_id` | Relación con la recomendación revisada |
| `model_version` | `PredictionResponse.model_version` | Auditoría del candidato local |
| `taxonomy_version` | `PredictionResponse.taxonomy_version` | Compatibilidad de las clases |
| `suggested_class` | `PredictionResponse.predicted_class` | Contexto de la recomendación |
| `reviewed_class` | Nula o clase canónica | Corrección humana acotada |
| `decision` | Vocabulario cerrado nuevo | Resultado de la revisión |
| `purpose` | Vocabulario cerrado nuevo | Finalidad declarada |
| `created_at` | Generado localmente en UTC | Auditoría y retención |
| `expires_at` | Política local de retención | Borrado finito |

## Datos excluidos

No se persistirán `PredictionRequest.narrative`, `client_request_id`, audio,
transcripciones, alternativas, confianza, advertencias, IP, cabeceras, datos de
cuenta, identidad, texto libre ni ningún dato que permita reconstruir una
reclamación. La ruta de predicción mantiene su prohibición vigente de registrar
o persistir narrativas.

## Conclusión

El contrato vigente aporta los identificadores, versiones y clase sugerida
necesarios para una revisión mínima. El almacén posterior debe generar sus
propias marcas temporales y aplicar vocabularios cerrados; no necesita leer ni
duplicar la narrativa de entrada.
