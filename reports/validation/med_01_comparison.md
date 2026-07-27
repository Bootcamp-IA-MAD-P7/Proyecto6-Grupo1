# MED-01: Comparativa de modelos ensemble

## Configuración

| Parámetro | Valor |
|---|---|
| Vectorizador | TF-IDF, unigrama+bigrama, sublinear_tf, 8K features |
| Partición | Train 200,000 / Val 40,000 / Test 302,076 |
| Trials Optuna | 30 |

## Resultados sobre validation

| Modelo | Macro F1 | Weighted F1 | Accuracy | Gap train/val |
|---|---|---|---|---|
| LogisticRegression (baseline) | 0.5973 | 0.8678 | 0.8484 | 0.0482 ✅ |
| Random Forest | 0.4661 | 0.8227 | 0.7992 | 0.0859 ❌ |
| XGBoost | 0.6437 | 0.8985 | 0.9046 | 0.1883 ❌ |

## Clases débiles (F1 < 0.5)

- **Random Forest**: Debt or credit management, Money transfer, virtual currency, or money service, Payday loan, title loan, personal loan, or advance loan, Prepaid card, Student loan
- **XGBoost**: Debt or credit management, Prepaid card

## Figuras

Las figuras se encuentran en `reports/validation/figures/`:
- `confusion_matrix_random_forest.png`
- `confusion_matrix_xgboost.png`
- `feature_importance_random_forest.png`
- `feature_importance_xgboost.png`
- `model_comparison.png`

## Reproducibilidad

```bash
python scripts/ml/train_ensemble.py --n-trials 30
```
