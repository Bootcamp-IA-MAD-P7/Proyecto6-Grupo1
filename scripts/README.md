# Automatizaciones

## Flujo OpenSpec y arnés

- `harness.py`: diagnostica la instalación y genera contexto seguro a partir del estado real de OpenSpec.
- `documentation/build_ai_handoff.py`: motor de composición segura utilizado también por las tareas heredadas.

Diagnóstico:

```bash
npm ci
python scripts/harness.py doctor
```

Cambio OpenSpec:

```bash
python scripts/harness.py start \
  --role architect \
  --change nombre-del-cambio
```

Acciones: `start`, `verify`, `review` y `prepare-pr`.

Compatibilidad para tareas ya asignadas:

```bash
python scripts/harness.py start \
  --role data-analyst \
  --spec 001 \
  --task T-004
```

Las salidas se guardan en `exports/`, fuera de Git. El generador solo admite fuentes documentales versionadas y no autoriza adjuntar datasets, secretos, narrativas reales, modelos ni logs.

## Calidad y documentación

- `quality/check_repository.py`: estructura, enlaces, dailies, archivos sensibles y contrato OpenSpec.
- `documentation/new_daily.py`: crea una daily sin sobrescribir documentos existentes.
- `documentation/build_notebooklm_pack.py`: genera un paquete curado para NotebookLM.

## Datos CFPB

- `data/cfpb_viability.py`: comprueba la API o inspecciona CSV/ZIP sin persistir narrativas en informes.

```bash
python scripts/data/cfpb_viability.py probe-api \
  --output reports/validation/cfpb_api_probe.json

python scripts/data/cfpb_viability.py sample-api \
  --output reports/validation/cfpb_api_sample.json
```

La configuración está en `config/cfpb_viability.json`. Los datos originales permanecen fuera de Git.

## Preparación local para baseline

- `data/convert_cfpb_to_parquet.py`: construye el corpus contractual local y genera evidencia agregada.
- `data/cfpb_training_policy.py`: comprueba que la fuente y el contrato coinciden con la política aprobada antes de preparar datos.
- `data/cfpb_training_preparation.py`: filtra el baseline inicial en inglés y crea particiones temporales por grupo para train, validation y test.

La preparación se ejecuta solo cuando se quiere reconstruir el corpus local; puede tardar varios minutos y genera Parquet ignorado por Git:

```bash
python -m scripts.data.cfpb_training_preparation --workers 12
```

El resultado compartible es únicamente `reports/validation/cfpb_training_preparation.md` y su manifiesto agregado. No se ejecuta para entrenar ni evalúa un modelo.
