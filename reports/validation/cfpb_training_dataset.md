# Construcción local del corpus CFPB

## Alcance de esta evidencia

Este informe resume la construcción local ejecutada el 27 de julio de 2026 por el cambio OpenSpec `build-cfpb-training-dataset` para Jira `PG-2` y la tarea heredada `001/T-005`.

No contiene narrativas, identificadores de reclamación ni ejemplos de la fuente. El Parquet resultante permanece en `data/processed/` e ignorado por Git. Esta evidencia no entrena ni evalúa un modelo y no cierra las decisiones de idioma, duplicados no conflictivos, partición, desbalanceo o privacidad ampliada.

## Fuente y contrato

| Elemento | Valor verificable |
|---|---:|
| Fuente local | `complaints.csv.zip` oficial del CFPB |
| Huella SHA-256 de la fuente | `f1cb8b412f6af5039ae630b3d0a1e4b5eab93be900a247ae60ea33cea073b351` |
| Contrato | `config/cfpb_target_contract.json` |
| Huella SHA-256 del contrato | `58b7ada8e6decdf0378aae4c042a381884ddda39143cbf0d6a0062c1f10fb9bd` |
| Clases canónicas | 11 |
| Salida local | `data/processed/cfpb_training.parquet` (ignorada por Git) |

## Recuentos agregados

| Población | Filas |
|---|---:|
| Fuente | 17.270.511 |
| Dentro de la ventana contractual | 10.768.599 |
| Con fecha, narrativa y producto válidos | 2.272.512 |
| Etiqueta ambigua excluida | 111 |
| Corpus canónico antes de conflictos | 2.272.401 |
| Filas excluidas por grupos con targets contradictorios | 273.831 |
| **Corpus local resultante** | **1.998.570** |

Se excluyeron 1.744 grupos de huella con targets contradictorios. Permanecen 169.680 grupos duplicados no conflictivos, con 942.383 filas involucradas; conservarlos sin colapsar ni ponderar es deliberado y sigue pendiente de decisión en `T-006`.

## Distribución resultante

| Clase canónica | Filas |
|---|---:|
| Checking or savings account | 97.167 |
| Credit card | 92.691 |
| Credit reporting or other personal consumer reports | 1.463.148 |
| Debt collection | 165.895 |
| Debt or credit management | 5.006 |
| Money transfer, virtual currency, or money service | 65.447 |
| Mortgage | 34.072 |
| Payday loan, title loan, personal loan, or advance loan | 16.429 |
| Prepaid card | 9.573 |
| Student loan | 24.761 |
| Vehicle loan or lease | 24.381 |

## Relación con el EDA previo

`reports/validation/cfpb_eda.md` describe una instantánea anterior con 40.213.168 filas de origen y 2.272.802 filas canónicas. La fuente descargada para este constructor el 27 de julio contiene 17.270.511 filas. Ambas evidencias son válidas para su propia huella de fuente, pero no deben compararse como si procedieran de la misma instantánea.

Antes de entrenar, `T-006` deberá decidir y documentar la fuente de referencia, idioma, tratamiento intra-grupo, partición anti-leakage y estrategia de desbalanceo.

## Verificación realizada

- `python -m unittest tests.unit.test_cfpb_training_dataset tests.unit.test_cfpb_target_contract -v` — 14 pruebas superadas.
- `python scripts/quality/check_repository.py` — superado.
- `git diff --check` — superado.
- `npm exec -- openspec validate build-cfpb-training-dataset --type change --strict` — superado.

El manifiesto legible por máquina es `reports/validation/cfpb_training_dataset_manifest.json` y contiene los mismos recuentos agregados.
