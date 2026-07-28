# Revisión del runbook local de ClaimVox

Fecha de revisión: `2026-07-28`

## Alcance

Se revisó la documentación de ejecución local de ClaimVox. No se modificaron
React, FastAPI, el contrato, dependencias, modelos, datos, infraestructura ni
estados de Jira.

## Hechos contrastados

| Elemento | Fuente contrastada | Resultado documentado |
|---|---|---|
| API local | `app/api/main.py` y `app/api/routes/health.py` | Predicción en `/api/v1/predictions` y health en `/api/v1/health`. |
| Artefacto por defecto | `app/api/config.py` | FastAPI busca `models/cfpb_baseline.pkl`; sin él utiliza fallback mock. |
| Selección de cliente frontend | `app/interface/src/services/configured-prediction-client.ts` | Sin `VITE_PREDICTION_API_BASE_URL` se conserva mock; con origen local válido se usa transporte HTTP. |
| Endpoint frontend | `app/interface/src/services/http-prediction-transport.ts` | El cliente añade `/api/v1/predictions` al origen configurado. |
| Privacidad local | `app/api/security.py` y documentación de frontend | Límite de texto, frecuencia efímera y ausencia de persistencia de narrativa. |

## Decisiones documentales

- `docs/project_management/essential_delivery_guide.md` es la guía canónica de
  arranque Git Bash.
- El README y los manuales de frontend/backend enlazan a la guía en lugar de
  duplicar secuencias contradictorias.
- `GET /api/v1/health` diferencia predictor disponible (`ok`) y fallback mock
  (`degraded`) sin revelar datos ni artefactos.
- Una ventana de incógnito es el primer paso de recuperación ante recursos PWA
  antiguos; no se requiere borrar archivos del proyecto.

## Límites

La guía no acredita despliegue, autenticación, persistencia, cuentas reales,
analítica de usuarios, Docker, cloud ni MLOps. Toda prueba de interfaz debe usar
el ejemplo sintético incluido y no narrativas reales del CFPB.
