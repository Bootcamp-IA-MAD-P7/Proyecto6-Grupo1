# MED-01: Comparativa de modelos ensemble

## Configuración

| Parámetro | Valor |
|---|---|
| Vectorizador | TF-IDF, unigrama+bigrama, sublinear_tf, 8K features |
| Partición | Train 50,000 / Val 10,000 / Test 302,076 |
| Tuning XGBoost | Defaults |

## Resultados sobre validation

| Modelo | Macro F1 | Weighted F1 | Accuracy | Precision | Recall | ROC AUC | Gap train/val |
|---|---|---|---|---|---|---|---|
| LogisticRegression (baseline) | 0.5973 | 0.8678 | 0.8484 | 0.5363 | 0.742 | — | 0.0482 ✅ |
| Random Forest | 0.4704 | 0.8270 | 0.8082 | 0.4690 | 0.5965 | 0.9309 | 0.1073 ❌ |
| XGBoost | 0.6332 | 0.8963 | 0.9026 | 0.7563 | 0.5781 | 0.9663 | 0.2868 ❌ |
| LightGBM | 0.6175 | 0.8956 | 0.9017 | 0.7709 | 0.5669 | 0.9650 | 0.3067 ❌ |

## Clases débiles (F1 < 0.5)

- **Random Forest**: Debt or credit management, Money transfer, virtual currency, or money service, Payday loan, title loan, personal loan, or advance loan, Prepaid card, Student loan
- **XGBoost**: Debt or credit management, Payday loan, title loan, personal loan, or advance loan
- **LightGBM**: Debt or credit management, Payday loan, title loan, personal loan, or advance loan, Prepaid card

## Figuras

Las figuras se encuentran en `reports/validation/figures/`:
- `confusion_matrix_lightgbm.png`
- `confusion_matrix_random_forest.png`
- `confusion_matrix_xgboost.png`
- `feature_importance_lightgbm.png`
- `feature_importance_random_forest.png`
- `feature_importance_xgboost.png`
- `model_comparison.png`

## Reproducibilidad

```bash
python scripts/ml/train_ensemble.py --n-trials 0 --tune-sample 0
```
