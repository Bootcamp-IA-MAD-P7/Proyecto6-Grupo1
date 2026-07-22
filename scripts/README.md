# Scripts

Automatizaciones reproducibles para descarga, entrenamiento, evaluación, validación, migraciones, despliegue y operaciones MLOps.

No se añadirán scripts que oculten pasos manuales no documentados.

## Disponibles desde la fundación

- `quality/check_repository.py`: comprueba estructura, enlaces, dailies y archivos sensibles.
- `documentation/new_daily.py`: crea una daily y su actualización editorial sin sobrescribir documentos.
- `documentation/build_notebooklm_pack.py`: genera un paquete curado para NotebookLM.
- `data/cfpb_viability.py`: prueba la API CFPB o inspecciona CSV/ZIP sin persistir narrativas en los informes.

## Spike CFPB

```bash
python scripts/data/cfpb_viability.py probe-api \
  --output reports/validation/cfpb_api_probe.json

python scripts/data/cfpb_viability.py sample-api \
  --output reports/validation/cfpb_api_sample.json
```

La configuración versionada está en `config/cfpb_viability.json`. Los datos originales permanecen fuera de Git.
