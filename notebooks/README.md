# Notebooks

## Estado vigente

`01_eda.py` es la fuente narrativa reproducible del EDA que sustenta
`ESS-02`. Su evidencia agregada está en
`reports/validation/cfpb_eda.md`; las decisiones posteriores de preparación y
partición están en `config/cfpb_training_policy.json`. Los recuentos de ambos
cortes no se mezclan.

No existe un notebook de selección de Champion. La lógica reutilizable de
entrenamiento y evaluación vive en `src/ml/` y `scripts/ml/`; los notebooks no
son la fuente de verdad de métricas ni contratos.

## Formato

Los notebooks se editan como archivos Python con celdas en formato `percent`:

```text
notebooks/
├── 01_eda.py          # ← fuente de verdad (editar aquí)
├── 01_eda.ipynb       # ← generado por jupytext, en .gitignore
└── ...
```

La sintaxis `# %%` está soportada nativamente por VS Code (Python Interactive)
y otros editores. No necesitas Jupytext para ejecutar celdas en VS Code.

Jupytext permite sincronizar con `.ipynb` cuando se necesite Jupyter
Notebook/Lab o ejecución headless con `nbconvert`.

El `.py` es fuente de verdad; el `.ipynb` no se versiona.

Ver [ADR-003](../specs/001-cfpb-target-contract/decisions.md).

## Dependencias

```bash
uv add jupytext ruff nbstripout polars
```

Las dependencias también están declaradas en `pyproject.toml`. No es necesario
regenerar ni ejecutar el notebook para revisar la evidencia versionada.

## Comandos

```bash
# Sincronizar .py ↔ .ipynb (genera .ipynb desde .py)
uv run jupytext --sync notebooks/*.py

# Ejecutar notebooks headless
uv run jupyter nbconvert --execute --inplace notebooks/01_eda.ipynb

# Limpiar metadatos de .ipynb
uv run nbstripout --keep-output notebooks/*.ipynb

# Lint
uv run ruff check notebooks/*.py
```

## Makefile (opcional)

```bash
make check                  # ruff lint
make format                 # ruff format
make sync                   # jupytext --sync
make run                    # nbconvert --execute
make clean                  # nbstripout
make notebook               # pipeline completa: check → sync → run → clean
make notebook TARGET=notebooks/eda.py   # solo un archivo
```

## Convención de nombres

```text
01_eda.py
02_baseline.py
03_experiments.py
```

Los notebooks sirven para exploración y narrativa. La lógica necesaria para
reproducir el sistema debe trasladarse a `src/`. Ninguna ejecución puede
versionar narrativas CFPB, datasets, outputs por fila o `.ipynb` generado.
