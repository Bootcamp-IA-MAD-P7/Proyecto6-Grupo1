# Hoja de ruta posterior al MVP esencial

> Estado: propuesta versionada para preparar Jira. No crea elementos de Jira ni
> acredita implementación. Fecha: 28 de julio de 2026.

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

| Orden | Historia propuesta | Criterios del briefing | Dependencia de inicio | Evidencia mínima de cierre | Responsable inicial |
|---|---|---|---|---|---|
| 0 | [PG-10: cierre de madurez y presentación](https://miguel-redondo.atlassian.net/browse/PG-10) | Corte de MVP, sin criterio nuevo | PR de este cambio revisada | Controles, README, NotebookLM y tag anotado | Arquitectura / coordinación |
| 1 | [PG-11: selección de modelo gobernada](https://miguel-redondo.atlassian.net/browse/PG-11) | MED-02, MED-03 | Particiones locales y baseline actuales | CV estratificada, búsqueda reproducible sin test y decisión documentada | Datos / Víctor |
| 2 | [PG-12: quality gates](https://miguel-redondo.atlassian.net/browse/PG-12) | ADV-04, ADV-05, ADV-06 | PG-11 y contrato vigente | Tests de integridad, carga/salida y umbrales ejecutados en CI | Datos + backend |
| 3 | [PG-13: feedback y recolección](https://miguel-redondo.atlassian.net/browse/PG-13) | MED-04, MED-05 | Política de propósito, retención y consentimiento aprobada | Esquema, minimización, trazabilidad y pipeline de reentrenamiento | Producto + backend |
| 4 | [PG-14: persistencia gobernada](https://miguel-redondo.atlassian.net/browse/PG-14) | ADV-02 | PG-13 | Esquema, migraciones, mínimo privilegio y pruebas de acceso | Backend / José |
| 5 | [PG-15: empaquetado y despliegue](https://miguel-redondo.atlassian.net/browse/PG-15) | ADV-01, ADV-03 | PG-12 y PG-14, más decisión de entorno | Imagen, healthcheck, smoke, rollback y entorno documentado | Plataforma / equipo |
| 6 | [PG-16: benchmark avanzado](https://miguel-redondo.atlassian.net/browse/PG-16) | EXP-01, EXP-02 | PG-11 y criterio de comparación aprobado | Red neuronal comparable y experimento/simulación reproducible | Datos / Víctor |
| 7 | [PG-17: monitorización y promoción](https://miguel-redondo.atlassian.net/browse/PG-17) | EXP-03, EXP-04 | PG-13, PG-14, PG-15 y modelo aprobado | Referencia, umbrales, alerta, aprobación y rollback verificables | MLOps / equipo |

## Regla de trabajo

Una historia no comienza por código: comienza por una propuesta OpenSpec y por
un elemento Jira enlazado. El estado de Jira explica coordinación; las pruebas,
informes y artefactos versionados son la evidencia de cierre. Ninguna historia
convierte en producción el servicio local existente sin su propio diseño de
seguridad y despliegue.

## Siguiente acción humana

La estructura Jira está creada y sus ocho dependencias se han enlazado. `PG-10`
está cerrado con la PR `#44` y el tag anotado `v0.1.0-essential-mvp`; el siguiente
trabajo de producto es `PG-11`, mediante un cambio OpenSpec nuevo.
