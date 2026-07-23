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
