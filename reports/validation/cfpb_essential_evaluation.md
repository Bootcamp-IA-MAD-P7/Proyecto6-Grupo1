# Evaluación esencial del modelo CFPB

Fecha de ejecución: `2026-07-28`
Cambio OpenSpec: `complete-essential-model-evaluation`
Split de diagnóstico: validation local actual
Uso de test protegido: no

## Candidato evaluado

Se selecciona para la entrega esencial local el baseline `LogisticRegression`
con TF-IDF de unigramas y bigramas, `class_weight="balanced"`, `C=0.1` y
semilla `42`. Es el único candidato con evaluación completa sobre las
particiones locales actuales y control de gap aprobado. Los ensembles siguen
siendo comparativas de muestra; no se usan para seleccionar este candidato.

El artefacto se guarda localmente como `models/cfpb_essential_baseline.pkl` y
está ignorado por Git. Su hash, configuración y contrato se registran en
`cfpb_essential_model_manifest.json`.

## Métricas de validation

| Métrica | Resultado |
|---|---:|
| Filas validation | 294.161 |
| Accuracy | 0,8684 |
| Macro F1 | 0,6390 |
| Weighted F1 | 0,8814 |
| Precision macro | 0,5899 |
| Recall macro | 0,7579 |
| Macro F1 train | 0,6468 |
| Gap train-validation | 0,0078 |
| Umbral de gap | `< 0,05` |

Las métricas protected-test históricas no se reutilizaron en esta ejecución. La
evaluación de test ya registrada conserva su carácter final y descriptivo; no se
usa aquí para seleccionar, ajustar ni diagnosticar el modelo.

## Matriz de confusión e importancia

- Matriz normalizada por clase: `figures/cfpb_baseline_validation_confusion_matrix.png`.
- Importancia por coeficiente absoluto medio de TF-IDF:
  `figures/cfpb_baseline_validation_feature_importance.png`.

Los coeficientes reflejan asociaciones aprendidas por el modelo lineal; no son
causalidad ni explicaciones individuales. Las figuras y el JSON contienen solo
etiquetas, configuraciones y cifras agregadas.

## Clases débiles y análisis de errores

| Clase | F1 | Soporte | Acción propuesta |
|---|---:|---:|---|
| Debt or credit management | 0,1036 | 682 | Mantener revisión humana prioritaria; estudiar cobertura y definición de clase antes de cambiar el modelo. |
| Payday loan, title loan, personal loan, or advance loan | 0,4964 | 2.468 | Revisar equilibrio y posibles señales lingüísticas en una futura experimentación gobernada. |
| Prepaid card | 0,4380 | 1.053 | Mantener revisión humana y evaluar alternativas de representación o datos adicionales. |

Las confusiones más frecuentes se concentran entre `Credit reporting or other
personal consumer reports`, `Debt collection`, `Credit card` y categorías de
gestión de deuda. Esta observación no permite tomar decisiones automáticas: la
respuesta de ClaimVox sigue marcando revisión humana obligatoria.

## Reproducción

```bash
python scripts/ml/train_essential_baseline.py
python -m unittest tests.unit.test_essential_model_evaluation -v
```

El primer comando carga solo `train.parquet` y `validation.parquet`; no acepta
ni carga `test.parquet`. No se versionan datos, narrativas, predicciones por
fila ni binarios del modelo.
