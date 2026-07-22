# Datos

```text
raw/        datos originales e inmutables
external/   fuentes auxiliares
interim/    transformaciones intermedias reproducibles
processed/  datos preparados para modelado
```

Los datos pesados no se versionan por defecto. La spec de dataset decidirá descarga, licencia, checksums y estrategia de versionado.

## Candidata CFPB

- No descargar el ZIP completo sin aprobación explícita.
- Guardar cualquier exportación oficial únicamente en `data/raw/`.
- No copiar narrativas en informes, fixtures, logs ni Pull Requests.
- Utilizar `config/cfpb_viability.json` y `scripts/data/cfpb_viability.py` para obtener resultados agregados reproducibles.
