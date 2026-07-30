# Revisión funcional del rediseño local de ClaimVox

Fecha: `2026-07-30`

Jira: `PG-16`

Cambio OpenSpec: `ui-redesign`

Implementación revisada: PR `#66`, commit integrado `545875c`

## Alcance

Se revisó el rediseño fusionado en `dev` sobre la PWA real, su contrato de
predicción y el recorrido local PWA → FastAPI → baseline. No se evaluaron
Docker, despliegue, autenticación, permisos reales, base compartida, Champion
ni MLOps.

## Hallazgos y correcciones

La verificación posterior a la integración detectó:

- errores de TypeScript y lint en `ClassificationPage`;
- nueve archivos fuera del formato configurado;
- tres pruebas de error seguro fallidas;
- un fallback que, tras fallar el servicio, mostraba una categoría sintética;
- una segunda frontera en la que el modo sin API o un backend degradado podía
  presentar un resultado mock.
- literales visibles en español dentro de una aplicación definida en inglés y
  ausencia del enlace de entrada a las identidades demo user/admin.
- estados estáticos del Dashboard que no consultaban health ni el resumen
  agregado local y podían resultar engañosos.

La corrección conserva la narrativa únicamente en memoria y en el paso Review,
muestra un error recuperable con foco accesible y no avanza a Guidance. Solo
una respuesta contractual de `local_api` con un modelo no mock puede producir
una clasificación visible. Los textos quedan en inglés y la cabecera vuelve a
ofrecer `Sign in` cuando no hay sesión; el acceso continúa siendo una
demostración y no autenticación real.

El Dashboard consulta ahora la misma base local configurada para representar
`Healthy`, `Degraded`, `Unavailable` o `Not configured`, y muestra únicamente
el conteo y una tabla del resumen agregado de feedback, en el orden contractual,
con versión de modelo, clase sugerida, decisión y conteo. `Operational data`
permanece `Not connected` porque no existe base compartida; `Human review`
permanece `Required`. No se muestran identificadores, narrativas, registros
individuales, Champion, despliegue ni métricas inventadas.

## Evidencia automática

Desde `app/interface/`:

```text
npm run typecheck
npm run lint
npm run format:check
npm test -- --run
npm run build
```

Resultado: type-check, lint y formato correctos; `10` archivos de prueba y `63`
pruebas superadas; build PWA generado correctamente.

Desde la raíz:

```text
python scripts/quality/check_repository.py
npm exec -- openspec validate ui-redesign --type change --strict
git diff --check
```

Resultado: arnés `30/30`, quality gate del repositorio superado para `594`
archivos versionados y `648` locales, cambio OpenSpec válido y diff sin errores.

La verificación de cierre añadió la suite Python completa: `134` pruebas
unitarias y `35` pruebas de contrato superadas. Los avisos de los estimadores
sobre fixtures mínimos no representan fallos ni resultados de entrenamiento
real.

## Smoke local

Con `models/cfpb_baseline.pkl`, backend en `127.0.0.1:8000` y frontend en
`127.0.0.1:5173`:

| Control | Resultado agregado |
|---|---|
| Frontend `/classify` | HTTP `200` |
| Backend `/api/v1/health` | `ok` |
| Predicción | Clase `Credit card` |
| Confianza | `0.7016` |
| Modelo | `baseline-lr-C0.1-f8000` |
| Taxonomía | `1.0` |

La entrada utilizada fue sintética y no se conserva en este informe. No se
incluyen identificadores de predicción, datos CFPB, filas, credenciales,
binarios ni logs completos.

## Límite de la evidencia

La revisión humana del 30 de julio comprobó en escritorio la clasificación
local, la navegación de usuario y administración, los estados factuales del
Dashboard y la tabla agregada de cuatro revisiones. No se versiona una captura
nueva ni se afirma una comprobación manual exhaustiva de todos los viewports o
de Edge. La evidencia sí acredita compilación, pruebas del flujo, servicio del
frontend, salud de la API y una inferencia real local.
