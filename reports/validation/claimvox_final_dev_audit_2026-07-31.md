# Auditoría final de `dev` · ClaimVox · 2026-07-31

## Corte y alcance

- Rama integrada auditada: `origin/dev`.
- SHA: `1366ef202cbabe45a1c53a96d57e6284e690993a`.
- Cambio OpenSpec: `audit-final-dev-delivery-state`.
- Jira de seguimiento: `PG-16`.
- Alcance: Git/GitHub, aplicación, contratos, seguridad, plataforma,
  documentación, NotebookLM y los 25 criterios.
- Exclusiones: entrenamiento, CV, narrativas CFPB reales, cloud, publicación,
  commit, push, merge, archive, `main`, tags y releases.

## Inventario Git y GitHub

Las PR #70 y #71 integraron Docker, PostgreSQL, JWT demo y el workflow EC2.
Las PR #72 a #76 integraron después la resolución same-origin, configuración
de feedback, conexión PostgreSQL, estado de base en Dashboard y la frontera de
DDL. En repositorios con squash merge, una rama histórica puede aparecer como
“no contenida” aunque su PR esté fusionada; la clasificación usa el estado de
la PR y el árbol de `dev`, no solo ancestría.

PR abiertas en el corte:

| PR | Rama | Clasificación |
|---|---|---|
| #18 | `dependabot/github_actions/actions/setup-node-7` | Revisión pendiente; antigua y no se fusiona automáticamente |
| #49 | `docs/align-delivery-status-sources` | Draft histórico; revisar/cerrar como sustituido |
| #53 | `design/claimvox-ux-ui-prototype` | Draft histórico; revisar/cerrar como sustituido |

Ramas PG-11 (`ml/PG-11-*`) contienen trabajo no integrado o ejecuciones no
convergentes. No acreditan `MED-02`, `MED-03` ni Champion. Las ramas de PR ya
fusionadas se consideran históricas/sustituidas y no deben volver a fusionarse.

Cambios OpenSpec activos en el corte:

| Cambio | Estado auditado |
|---|---|
| `packaging-and-deploy` | En curso: 2/5 tareas; Docker, PostgreSQL y AWS requieren evidencia dinámica |
| `add-governed-feedback-persistence` | En curso: 9/10; existe además spec archivada y debe reconciliarse antes de otro cierre |
| `propose-claimvox-ux-ui-prototype` | Completo pero no archivado; histórico/sustituido por el rediseño integrado |
| `govern-cfpb-model-selection` | Completo como implementación/piloto, no acredita `MED-02`/`MED-03` |
| `reconcile-baseline-delivery-evidence` | Completo y no archivado; revisar su cierre sin alterar la evidencia |
| `audit-final-dev-delivery-state` | Auditoría actual; pendiente de revisión humana |

## Hallazgos y correcciones seguras

| Hallazgo | Corrección |
|---|---|
| Secretos JWT, DB y credenciales demo embebidos | Compose exige variables externas; `.env.example` contiene solo placeholders; el fallback JWT es efímero |
| Login exponía credenciales | La UI pide credenciales al operador local y no muestra valores |
| CORS no permitía `Authorization` | Se permite únicamente `Authorization` y `Content-Type` en orígenes locales explícitos |
| Feedback no exigía el token | Creación y resumen requieren Bearer token; el cliente lo adjunta |
| Repositorio PostgreSQL conservaba DDL residual | DDL retirado del runtime; inicialización administrativa versionada |
| Smoke EC2 podía fallar sin fallar el job | Reintentos acotados y salida no cero |
| OpenAPI y documentación negaban capacidades integradas | Contratos y fuentes activas reconciliados sin acreditar cloud |
| Auditoría npm del frontend detectó vulnerabilidades altas | Dependencias/resoluciones corregidas; tipos, 63 tests, build y auditoría pasan |

No se imprimieron ni versionaron valores reales, datos, narrativas o modelos.

## Estado funcional

- Backend: health/estado, login demo, predicción protegida, feedback protegido,
  errores seguros, límites locales y fallback degradado.
- Frontend: login, clasificación, revisión humana, registro de feedback y
  Dashboard con health, conexión de base y resumen exclusivamente agregado.
- Modelo: baseline local reproducible; el binario permanece ignorado y debe
  reconstruirse antes de un build limpio.
- Persistencia: SQLite local verificada; PostgreSQL integrado por configuración
  pero sin prueba dinámica en este entorno.
- Plataforma: Dockerfiles, Nginx, Compose y workflow EC2 integrados. El daemon
  Docker no estaba disponible, por lo que no se verifican build ni ejecución.

## Criterios

| Nivel | Verificado | En curso | No iniciado |
|---|---:|---:|---:|
| Esencial | 10 | 0 | 0 |
| Medio | 2 | 3 | 0 |
| Avanzado | 3 | 3 | 0 |
| Experto | 0 | 0 | 4 |
| Total | 15 | 6 | 4 |

- `MED-02`/`MED-03`: falta CV completa convergida y decisión versionada.
- `MED-05`: falta corpus, validación, deduplicación e incorporación gobernada.
- `ADV-01`: falta build/ejecución desde clon limpio.
- `ADV-02`: falta prueba PostgreSQL, migraciones, backup y reversión.
- `ADV-03`: falta URL, smoke observado, monitorización y rollback.
- `EXP-01` a `EXP-04`: no iniciados.

## Verificación

Comprobaciones directas ya superadas durante la corrección:

- 141 tests unitarios Python.
- 40 tests de contrato Python.
- 63 tests frontend en 10 archivos.
- Type-check, ESLint, Prettier y build PWA.
- `npm audit --audit-level=high`: cero vulnerabilidades en tooling raíz y
  frontend.
- Harness doctor: 32 artefactos OpenSpec válidos.
- Quality gate: 628 archivos versionados y 684 locales comprobados.
- OpenAPI JSON, Compose estático, SVG XML/accesibilidad y `git diff --check`.

La comprobación Docker queda limitada a `docker compose config --quiet` y
revisión estática porque el daemon local no respondió. Tampoco se realizó una
revisión visual automatizada del SVG porque no había navegador disponible; se
validaron estructura, texto sincronizado, título y descripción accesibles.

## Riesgos y recomendaciones

1. Revisar/cerrar PR #18, #49 y #53; no fusionar ramas históricas por nombre.
2. Resolver `PG-11` sin promover el baseline o un piloto como Champion.
3. En `PG-15`, reconstruir el modelo, crear `.env`, levantar Compose desde clon
   limpio y versionar resultados agregados de health, PostgreSQL y rollback.
4. No iniciar `PG-17` como capacidad verificada sin telemetría, referencia de
   drift, alertas y promoción reversible.
5. Sustituir el JWT demo por identidad y autorización reales antes de exposición
   pública.
