# Hoja de ruta posterior al MVP esencial

> Estado: hoja de ruta reconciliada con Jira y evidencia versionada. Fecha de
> corte: 31 de julio de 2026. El estado de Jira no sustituye las pruebas.

## Propósito

El nivel esencial de ClaimVox está verificado para ejecución local. Esta hoja
de ruta reúne los catorce criterios restantes en una secuencia única por
dependencias, no en listas independientes por nivel. Cada bloque necesitará su
propio cambio OpenSpec, evidencia reproducible y una revisión humana antes de
pasar a `Listo`.

## Propuesta de estructura Jira

El Epic **PG-9 — Evolución gobernada de ClaimVox después del MVP esencial** ya
está creado en Jira. `PG-10` está en `Listo`; las demás historias empiezan
en `Por hacer`. Su estado operativo no sustituye la evidencia del repositorio.

| Orden | Historia | Estado Jira | Criterios | Estado de evidencia | Siguiente condición |
|---|---|---|---|---|---|
| 0 | [PG-10: cierre del MVP esencial](https://miguel-redondo.atlassian.net/browse/PG-10) | Listo | Corte, sin criterio nuevo | Tag esencial y documentación versionados | Conservar como histórico |
| 1 | [PG-11: selección gobernada](https://miguel-redondo.atlassian.net/browse/PG-11) | En curso | MED-02, MED-03 | Estrategia y piloto; falta CV completa convergida | Folds, variabilidad, optimización y decisión |
| 2 | [PG-12: quality gates](https://miguel-redondo.atlassian.net/browse/PG-12) | Listo | ADV-04, ADV-05, ADV-06 | 16 pruebas sintéticas y política versionada | Mantener gates en CI |
| 3 | [PG-13: feedback y recolección](https://miguel-redondo.atlassian.net/browse/PG-13) | Listo | MED-04, MED-05 | MED-04 verificado; MED-05 parcial | Corpus, validación y política de incorporación |
| 4 | [PG-14: persistencia gobernada](https://miguel-redondo.atlassian.net/browse/PG-14) | Listo | Preparación de ADV-02 | SQLite local con retención | Diseñar base compartida y migraciones para ADV-02 |
| 5 | [PG-15: empaquetado y despliegue](https://miguel-redondo.atlassian.net/browse/PG-15) | En curso | ADV-01, ADV-02, ADV-03 | Docker, PostgreSQL, JWT demo y workflow integrados; sin evidencia completa | Build limpio, prueba DB, smoke y rollback |
| 6 | [PG-16: benchmark avanzado](https://miguel-redondo.atlassian.net/browse/PG-16) | En curso | UX / apoyo a EXP-01, EXP-02 | Rediseño y Dashboard local verificados; benchmark no iniciado | Esperar protocolo de comparación |
| 7 | [PG-17: monitorización y promoción](https://miguel-redondo.atlassian.net/browse/PG-17) | Por hacer | EXP-03, EXP-04 | No iniciado | Requiere runtime desplegado y modelo aprobado |

## Regla de trabajo

Una historia no comienza por código: comienza por una propuesta OpenSpec y por
un elemento Jira enlazado. El estado de Jira explica coordinación; las pruebas,
informes y artefactos versionados son la evidencia de cierre. Ninguna historia
convierte en producción el servicio local existente sin su propio diseño de
seguridad y despliegue.

## Siguiente acción humana

La prioridad pendiente es resolver o cerrar con evidencia honesta `PG-11`.
Después, `PG-15` debe verificar el empaquetado y la persistencia ya integrados
antes de acreditar despliegue. `PG-13` y `PG-14` aportan capacidades locales,
pero no convierten `MED-05` ni `ADV-02` en verificados.
