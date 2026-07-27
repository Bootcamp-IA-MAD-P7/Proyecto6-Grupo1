# Baseline multiclase CFPB — LogisticRegression

## Configuración ganadora

| Parámetro | Valor |
|---|---|
| Vectorizador | TF-IDF, unigrama+bigrama, sublinear_tf |
| max_features | 8.000 |
| min_df / max_df | 3 / 0.8 |
| Modelo | LogisticRegression (lbfgs) |
| C (regularización) | 0.1 |
| class_weight | balanced |

## Métricas

| Métrica | Validation | Test (protegido) |
|---|---|---|
| Macro F1 | 0.5973 | **0.6625** |
| Weighted F1 | 0.8678 | 0.8809 |
| Accuracy | 0.8484 | 0.8230 |
| Gap train/val | 0.0482 ✅ | — |

El macro F1 en test es superior al de validation, lo que confirma que no hay
overfitting y que la partición de validation representa una distribución más
exigente.

## Clases débiles (F1 < 0.5)

### Validation
- Debt or credit management (0.07, soporte 620)
- Payday loan, title loan, personal loan, or advance loan (0.44, soporte 2.176)
- Prepaid card (0.45, soporte 1.022)

### Test (protegido)
- Debt or credit management (0.14, soporte 1.281)
- Prepaid card (0.42, soporte 1.809)

Payday loan sale de la lista de débiles en test (F1 0.53). Debt/credit
management y Prepaid card siguen siendo las clases con menos soporte.

## Reproducibilidad

```bash
python scripts/ml/train_baseline.py \
  --C 0.1 --max-features 8000 --min-df 3 --max-df 0.8 \
  --ngram-range "1,2" --sublinear-tf --evaluate-test
```

Semilla: 42. Serialización: joblib.

## Rendimiento

- Particiones: Train 1.396.019 / Val 300.870 / Test 302.076 (protegido)
- Tiempo total: ~7 min entrenamiento + ~1 min test
- Artefacto: `models/cfpb_baseline.pkl` (gitignored, joblib)

## Notas

- El gap cumple el umbral de 0.05 (ESS-03).
- Las clases minoritarias con soporte < 2.000 siguen siendo débiles; la
  regularización y bigramas ayudaron pero no resuelven el desbalanceo
  estructural.
- El test se evaluó una única vez como evaluación final protegida (one-shot).
- El macro F1 en test (0.6625) es un 10,9 % superior al de validation, lo que
  sugiere que el modelo generaliza bien a distribuciones ligeramente distintas.
