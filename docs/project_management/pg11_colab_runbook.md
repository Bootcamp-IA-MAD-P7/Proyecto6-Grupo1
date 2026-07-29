# Ejecución de PG-11 en Google Colab

Este guion ejecuta la selección gobernada sobre una copia local de
`train.parquet`. No sube datos al repositorio, no carga validación ni test y no
debe mostrar narrativas CFPB.

## 1. Preparar el entorno

En una celda nueva de Colab:

```python
!git clone https://github.com/Bootcamp-IA-MAD-P7/Proyecto6-Grupo1.git
%cd Proyecto6-Grupo1
!pip install -e .
```

## 2. Montar la copia local de datos

Guarda previamente fuera de Git el fichero aprobado
`cfpb_baseline_en/train.parquet` en Google Drive. Después ejecuta:

```python
from google.colab import drive
drive.mount('/content/drive')

train_path = "/content/drive/MyDrive/claimvox-data/cfpb_baseline_en/train.parquet"
```

No abras el Parquet, no imprimas filas y no uses `validation.parquet`,
`test.parquet` ni `cfpb_training.parquet`.

## 3. Ejecutar un candidato aprobado

Ejecuta una sola vez por candidato, empezando por el acordado en la revisión
humana. El piloto vigente usa 20.000 filas, 5 trials y 3 folds agrupados.

```python
!python scripts/ml/evaluate_model_selection.py \
  --train-input "$train_path" \
  --candidate xgb \
  --execute | tee /content/pg11-xgb-output.txt
```

## 4. Conservar solo evidencia agregada

Comparte para revisión únicamente la salida agregada de
`/content/pg11-xgb-output.txt`. No subas a Git el Parquet, modelos, cachés,
carpetas de Colab ni logs que incluyan datos de reclamaciones. La validación
reservada, el test protegido y la decisión humana se abordan después de esta
ejecución.
