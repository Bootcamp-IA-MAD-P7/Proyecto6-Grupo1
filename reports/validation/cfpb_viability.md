# Spike de viabilidad de datos CFPB

- Fecha: `2026-07-22`
- Spec: [`000-problem-discovery`](../../specs/000-problem-discovery/spec.md)
- Tareas: `T-004`, `T-005`
- Estado: `verificado; viable con condiciones`

## Objetivo

Determinar si la Consumer Complaint Database permite construir un problema multiclase reproducible utilizando únicamente la narrativa disponible en el momento de inferencia y `product` como target.

Este spike no es un EDA, no descarga datos pesados por defecto y no entrena modelos.

## Contrato congelado

| Elemento | Valor |
|---|---|
| Ventana mínima inclusiva | `2023-08-24` |
| Ventana máxima exclusiva | `2026-07-23` |
| Filtro | Reclamaciones con narrativa publicada |
| Entrada permitida | `complaint_what_happened` |
| Target propuesto | `product` |
| Persistencia de narrativas | Prohibida en informes y Git |
| Configuración | `config/cfpb_viability.json` |

La ventana comienza con la taxonomía de producto vigente desde agosto de 2023 y queda congelada para que la comprobación sea repetible.

## Evidencia de acceso

### API documentada

La especificación OpenAPI oficial documenta un endpoint de búsqueda con filtros de fecha, narrativa, producto, agregaciones y un tamaño máximo de 100 resultados por petición.

Prueba local realizada:

```text
GET /data-research/consumer-complaints/search/api/v1/
date_received_min=2023-08-24
date_received_max=2026-07-23
has_narrative=true
size=1
no_highlight=true
```

Una primera consulta mediante PowerShell y `curl` recibió `HTTP 403 Access Denied`. El probe Python con límite de respuesta sí obtuvo posteriormente una respuesta válida. La diferencia de comportamiento del perímetro debe conservarse como riesgo operativo.

Resultado agregado del probe:

```text
Reclamaciones con narrativa en la ventana: 2.306.723
Relación del total: eq
Incidencia general de datos: false
Datos obsoletos: false
Licencia informada por la API: CC0
```

No se almacenó ninguna narrativa.

## Distribución global publicada por la API

| Etiqueta observada | Reclamaciones | Proporción |
|---|---:|---:|
| Credit reporting or other personal consumer reports | 1.671.242 | 72,4509 % |
| Debt collection | 214.880 | 9,3154 % |
| Checking or savings account | 106.440 | 4,6143 % |
| Credit card | 105.601 | 4,5780 % |
| Money transfer, virtual currency, or money service | 85.640 | 3,7126 % |
| Mortgage | 36.354 | 1,5760 % |
| Vehicle loan or lease | 26.196 | 1,1356 % |
| Student loan | 25.904 | 1,1230 % |
| Payday loan, title loan, personal loan, or advance loan | 17.627 | 0,7642 % |
| Prepaid card | 9.944 | 0,4311 % |
| Debt or credit management | 5.323 | 0,2308 % |
| Credit reporting, credit repair services, or other personal consumer reports | 1.449 | 0,0628 % |
| Credit card or prepaid card | 111 | 0,0048 % |
| Payday loan, title loan, or personal loan | 12 | 0,0005 % |
| **Total** | **2.306.723** | **100 %** |

La API devuelve catorce etiquetas, no once. Tres corresponden a formulaciones históricas o ambiguas:

- `Credit reporting, credit repair services, or other personal consumer reports` puede normalizarse semánticamente a la categoría vigente de informes de crédito.
- `Payday loan, title loan, or personal loan` puede normalizarse a la categoría vigente que añade `advance loan`.
- `Credit card or prepaid card` no puede dividirse de forma segura utilizando únicamente el nombre de producto; debe resolverse con una regla de target documentada o excluirse con justificación.

La clase mayoritaria representa el 72,45 % del total. Incluso tras normalizar etiquetas históricas, el problema seguirá teniendo un desbalanceo severo y requerirá macro F1, métricas por clase, partición estratificada y comparación de estrategias de ponderación.

## Muestra temporal acotada

El arnés inspeccionó 1.000 narrativas solo en memoria: las 500 más antiguas y las 500 más recientes devueltas por la API dentro de la ventana. Esta muestra no es aleatoria y no sustituye un EDA.

| Indicador | Resultado |
|---|---:|
| Registros elegibles | 1.000 |
| IDs duplicados | 0 |
| Narrativas exactamente duplicadas | 122 |
| Longitud mínima | 39 caracteres |
| Longitud mediana | 832 caracteres |
| Longitud máxima | 25.684 caracteres |
| Registros con señal heurística de PII | 4 |
| Tasa heurística | 0,4 % |

Las cuatro señales correspondieron a patrones de URL. No se detectaron patrones de correo, teléfono o SSN en esta muestra, pero el resultado no certifica anonimización.

### Extremo antiguo

- Cobertura: `2023-08-24`.
- 428 de 500 registros —85,6 %— utilizan la etiqueta histórica de informes de crédito.
- 118 de 500 narrativas —23,6 %— son duplicados exactos dentro del extremo.
- Cuatro registros contienen un patrón de URL.

### Extremo reciente

- Cobertura: `2026-06-25` a `2026-07-02`.
- Aparecen once etiquetas actuales.
- La clase con mayor soporte es `Debt collection`, con 139 de 500 registros —27,8 %—.
- Cuatro de 500 narrativas —0,8 %— son duplicados exactos.
- No se detectaron los patrones de PII configurados.

La diferencia entre extremos confirma drift de taxonomía, composición y duplicación. También evidencia el retraso de publicación de narrativas recientes: el extremo más nuevo finaliza el 2 de julio aunque el probe se ejecutó el 22 de julio.

### Descarga completa

La cabecera de la descarga oficial respondió correctamente mediante `curl`:

```text
HTTP/1.1 200 OK
Last-Modified: Tue, 21 Jul 2026 09:31:56 GMT
Accept-Ranges: bytes
Content-Length: 1422352348
```

La descarga comprimida ocupa aproximadamente 1,42 GB. No se descargará completa sin aprobación explícita y espacio suficiente.

## Procedimiento reproducible

### Opción preferida: API

```bash
python scripts/data/cfpb_viability.py probe-api \
  --output reports/validation/cfpb_api_probe.json
```

El probe limita la respuesta, descarta las narrativas y conserva únicamente estado, metadatos y agregados por producto.

Para inspeccionar una muestra acotada de los extremos temporales sin persistir textos:

```bash
python scripts/data/cfpb_viability.py sample-api \
  --output reports/validation/cfpb_api_sample.json
```

### Alternativa: exportación oficial filtrada

1. Abrir la herramienta oficial de la Consumer Complaint Database.
2. Filtrar desde el 24 de agosto de 2023 hasta el 22 de julio de 2026.
3. Mantener únicamente reclamaciones con narrativa.
4. Exportar CSV dentro de `data/raw/`; esta carpeta está excluida de Git.
5. Ejecutar:

```bash
python scripts/data/cfpb_viability.py inspect-csv \
  --input data/raw/<exportacion-cfpb>.csv \
  --output reports/validation/cfpb_viability.json
```

El inspector también acepta el ZIP oficial y genera el hash SHA-256 de la fuente sin copiar narrativas al informe.

## Comprobaciones automatizadas

- Esquema y campos obligatorios.
- Ventana temporal congelada.
- Número de filas elegibles.
- Distribución y soporte por clase.
- Valores ausentes en ID, narrativa y target.
- IDs y narrativas duplicadas.
- Longitud mínima, mediana y máxima de narrativa.
- Señales heurísticas de correo, teléfono, SSN o URL.
- Advertencias de desbalanceo, soporte, privacidad y truncado.

Las señales de PII son heurísticas: una coincidencia no demuestra que exista información personal y una ausencia no garantiza anonimización.

## Resultados pendientes

- [x] Recuento reproducible de narrativas elegibles: 2.306.723.
- [x] Distribución de las catorce etiquetas observadas.
- [x] Soporte global preliminar por clase.
- [x] Ausencias y duplicados en una muestra temporal acotada.
- [x] Longitudes de texto en la muestra.
- [x] Señales heurísticas de PII residual en la muestra.
- [ ] Confirmación del idioma o estrategia para detectarlo.
- [x] Mapping entre etiquetas históricas y taxonomía vigente versionado en `config/cfpb_target_contract.json`.
- [ ] Revisión de privacidad más amplia antes de persistir textos.

## Decisión provisional

El dataset se considera `viable con condiciones` para continuar el descubrimiento:

- G-02 supera el mínimo multiclase, pero requiere normalización explícita de target.
- G-03 dispone de API, descarga, documentación y licencia declarada por la API.
- G-04 mantiene la narrativa como única entrada y separa variables de target o posteriores.
- G-05 sigue condicional hasta ampliar la revisión de privacidad.
- G-06 es viable mediante extracción acotada; no requiere descargar el ZIP completo para el primer ciclo.

No se autoriza entrenamiento hasta incorporar la evidencia del EDA y aprobar idioma, tratamiento final de duplicados, partición y estrategia inicial de privacidad.

## Fuentes

- [Consumer Complaint Database](https://www.consumerfinance.gov/data-research/consumer-complaints/).
- [Especificación OpenAPI](https://raw.githubusercontent.com/cfpb/ccdb5-api/main/swagger-config.yaml).
- [Documentación interactiva de la API](https://cfpb.github.io/ccdb5-api/documentation/).
- [Referencia de campos](https://cfpb.github.io/api/ccdb/fields.html).
- [Incidencia oficial sobre el parámetro de paginación](https://github.com/cfpb/cfpb.github.io/issues/292).
