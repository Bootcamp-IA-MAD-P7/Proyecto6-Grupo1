# Verificación local de backend con baseline real

Fecha de ejecución: `2026-07-28`
Jira: `PG-5`
OpenSpec relacionado: `backend-foundation` y `fix-baseline-vectorizer-config`

## Alcance

Esta evidencia verifica la carga local de un artefacto de baseline y el recorrido
HTTP del backend. No conecta ClaimVox, no despliega el servicio, no selecciona un
Champion y no sustituye las métricas oficiales de `PG-3`.

## Artefacto local reproducido

- Entrada: particiones locales ignoradas por Git de
  `data/processed/cfpb_baseline_en/`.
- Filas: 1.372.751 train, 294.161 validation y 294.161 test protegido.
- Configuración: TF-IDF con 8.000 características, `min_df=3`, `max_df=0.8`,
  unigramas y bigramas, `sublinear_tf=true`; Logistic Regression con `C=0.1`,
  `class_weight="balanced"` y semilla 42.
- Salida: `models/cfpb_baseline.pkl`, ignorada por Git. No se versionan
  narrativas, datos, binarios de modelo ni logs locales.
- Validación local de esta reproducción: macro F1 train `0.6468`, macro F1
  validation `0.6390`, gap `0.0078`. Estas cifras corresponden a las
  particiones aprobadas actuales y no reemplazan las métricas históricas de
  `reports/validation/cfpb_baseline_metrics.json`.

## Smoke test HTTP

Con el artefacto local en la ruta por defecto, una petición sintética produjo:

| Comprobación | Resultado |
|---|---|
| `GET /api/v1/health` | `200`, estado `ok` |
| `POST /api/v1/predictions` | `200` |
| Versión devuelta | `baseline-lr-C0.1-f8000` |
| Confianza | Numérica |
| Clase y alternativas | Clase canónica y 10 alternativas |
| Privacidad | La narrativa sintética no aparece en la respuesta |

## Pruebas automatizadas

`python -m unittest tests.unit.test_cfpb_baseline tests.contract.test_backend_contract -v`
superó 33 pruebas locales: configuración, particiones aprobadas, serialización,
predictor real sintético, fallback mock, salud, contrato, errores y ausencia de
eco de narrativa.

## Límites

- El artefacto permanece local e ignorado; no hay registro de modelos ni
  despliegue.
- ClaimVox continúa utilizando su cliente mock: `ESS-04` no está verificado.
- No se ha vuelto a evaluar el test protegido ni se ha seleccionado un modelo
  para producción.
