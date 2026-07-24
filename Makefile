NOTEBOOK_DIR := notebooks
TARGET ?=

ifeq ($(TARGET),)
PY_NOTEBOOKS := $(wildcard $(NOTEBOOK_DIR)/*.py)
IPYNB_NOTEBOOKS := $(patsubst %.py,%.ipynb,$(PY_NOTEBOOKS))
else
PY_NOTEBOOKS := $(TARGET)
IPYNB_NOTEBOOKS := $(patsubst %.py,%.ipynb,$(TARGET))
endif

.PHONY: check format sync run clean notebook

check:
	uv run ruff check $(PY_NOTEBOOKS)

format:
	uv run ruff format $(PY_NOTEBOOKS)

sync:
	uv run jupytext --sync $(PY_NOTEBOOKS)

run:
	uv run jupyter nbconvert --execute --inplace $(IPYNB_NOTEBOOKS)

clean:
	uv run nbstripout --keep-output $(IPYNB_NOTEBOOKS)

notebook: check sync run clean
