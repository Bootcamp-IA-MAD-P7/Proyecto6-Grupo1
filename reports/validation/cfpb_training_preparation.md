# Preparación local del corpus CFPB para baseline

Fecha de ejecución: `2026-07-27`
Cambio OpenSpec: `decide-cfpb-training-policy`
Jira: `PG-2` / legado `001/T-006`

## Alcance y privacidad

Esta evidencia documenta una preparación local; no entrena ni evalúa ningún modelo. Las narrativas, sus huellas y los ficheros Parquet de train, validation y test permanecen bajo `data/processed/` e ignorados por Git. Este informe y su manifiesto asociado contienen exclusivamente recuentos, fechas y huellas.

## Política aplicada

| Regla | Valor aplicado |
|---|---|
| Fuente de referencia | SHA-256 `f1cb8b412f6af5039ae630b3d0a1e4b5eab93be900a247ae60ea33cea073b351` |
| Contrato de target | SHA-256 `58b7ada8e6decdf0378aae4c042a381884ddda39143cbf0d6a0062c1f10fb9bd` |
| Idioma del baseline | Inglés, `langdetect 1.0.9`, semilla `0`, hasta 500 caracteres |
| Duplicados con targets distintos | Excluidos por el constructor contractual |
| Duplicados no conflictivos | Conservados completos en una sola partición |
| Partición | Temporal por fecha máxima de grupo, objetivo 70/15/15 |
| Soporte mínimo | 100 filas por clase en validation y test |
| Métrica futura | Macro F1; pesos de clase balanceados; sin re-muestreo |

## Resultado agregado

| Etapa | Filas |
|---|---:|
| Corpus contractual local de entrada | 1.998.570 |
| Aceptadas como inglés | 1.961.073 |
| Excluidas por idioma no inglés o no clasificable | 37.497 |
| Train | 1.372.751 |
| Validation | 294.161 |
| Test protegido | 294.161 |

Las once clases superan el soporte mínimo. La clase con menor soporte es `Debt or credit management`: 682 filas en validation y 795 en test.

| Partición | Rango efectivo por fecha máxima de grupo |
|---|---|
| Train | 2023-08-24 a 2025-08-07 |
| Validation | 2025-08-07 a 2025-11-21 |
| Test | 2025-11-21 a 2026-06-02 |

Los límites pueden compartir fecha de calendario porque la unidad de asignación es el grupo completo, ordenado por su fecha máxima y huella. La comprobación automática confirmó que ninguna huella aparece en más de una partición.

## Evidencia reproducible

- Política: `config/cfpb_training_policy.json`.
- Puerta de huellas: `scripts/data/cfpb_training_policy.py`.
- Preparación local: `scripts/data/cfpb_training_preparation.py`.
- Manifiesto agregado: `reports/validation/cfpb_training_preparation_manifest.json`.
- Pruebas sintéticas: `tests/unit/test_cfpb_training_policy.py` y `tests/unit/test_cfpb_training_preparation.py`.

## Comprobaciones de cierre

Ejecutadas el `2026-07-27` sobre la rama de preparación, sin volver a procesar la fuente:

- 25 pruebas sintéticas de constructor, política, preparación y contrato: correctas.
- `python scripts/quality/check_repository.py`: correcto.
- `git diff --check`: correcto, sin errores de whitespace.
- Validación estricta de los cambios OpenSpec `build-cfpb-training-dataset` y `decide-cfpb-training-policy`: correcta.
- `python scripts/harness.py doctor`: Node.js, OpenSpec, raíz y validación estricta correctos.

## Límites que permanecen

- No existe baseline entrenado, modelo seleccionado, métrica calculada ni control de overfitting.
- El test permanece protegido y no debe usarse para seleccionar modelo o hiperparámetros.
- La política inglesa es inicial y deberá revisarse si la evidencia de producto exige cubrir otros idiomas.
- Esta preparación no verifica todavía `ESS-01`, `ESS-03` ni `ESS-05` a `ESS-09`.
