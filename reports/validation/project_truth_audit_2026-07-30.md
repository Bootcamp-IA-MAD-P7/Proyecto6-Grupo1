# Auditoría de verdad integrada · 30 de julio de 2026

## Alcance y método

Auditoría estática y reproducible de la rama `dev` sincronizada en
`9152de6`, seguida en la rama de trabajo
`docs/PG-9-audit-project-truth`. Se revisaron Git, OpenSpec, Jira, contratos,
aplicación, ML, pruebas, CI, seguridad y documentación activa.

No se abrieron datasets, narrativas CFPB, notebooks pesados ni artefactos de
modelo; no se ejecutó entrenamiento. Las ramas no fusionadas y los archivos
locales no versionados se excluyeron como evidencia.

## Estado integrado confirmado

| Área | Capacidad confirmada en `dev` | Límite vigente |
|---|---|---|
| Datos / ML | Once clases canónicas, preparación gobernada, EDA y baseline Logistic Regression evaluado | No existe Champion seleccionado |
| Backend | FastAPI local, health, predicción real con artefacto local y fallback mock seguro | No hay servicio desplegado ni autenticación |
| Frontend | React PWA con clasificación local legible, errores recuperables y revisión humana | Administración sigue siendo conceptual |
| Feedback | Captura local minimizada, SQLite local con retención y resumen exclusivamente agregado | No hay base compartida, operación multiusuario ni reentrenamiento automático |
| QA | Quality gates sintéticos de datos, modelo y métricas; CI de repositorio | No sustituyen ejecución sobre datos operativos ni despliegue |
| Gobierno | OpenSpec, arnés, Jira y PRs operativos | Persisten cambios OpenSpec activos antiguos que requieren cierre humano |

## Métricas versionadas del baseline

Fuente: `reports/validation/cfpb_baseline_metrics.json`.

| Métrica | Resultado |
|---|---:|
| Train macro F1 | `0.6455` |
| Validation macro F1 | `0.5973` |
| Gap macro F1 | `0.0482` |
| Validation accuracy | `0.8484` |
| Test protegido accuracy | `0.8230` |
| Test protegido macro F1 | `0.6625` |

El baseline utiliza TF-IDF y Logistic Regression con `class_weight=balanced`.
Las clases más débiles en validation incluyen `Debt or credit management`,
`Payday loan, title loan, personal loan, or advance loan` y `Prepaid card`.

Existe además una reconstrucción esencial posterior, documentada en
`cfpb_essential_evaluation.json`, sobre otro corte local (1.372.751 train y
294.161 validation): macro F1 `0.6390`, accuracy `0.8684` y gap `0.0078`, sin
usar test. Ambas evidencias son válidas para sus respectivas particiones y
deben publicarse con tamaño y procedencia, no combinarse.

## Estado de los criterios

Fuente canónica: `docs/project_management/delivery_levels.md`.

| Nivel | Verificado | En curso | No iniciado |
|---|---:|---:|---:|
| Esencial | 10 | 0 | 0 |
| Medio | 2 | 3 | 0 |
| Avanzado | 3 | 0 | 3 |
| Experto | 0 | 0 | 4 |
| **Total** | **15** | **3** | **7** |

Verificados: `ESS-01` a `ESS-10`, `MED-01`, `MED-04` y `ADV-04` a
`ADV-06`. En curso: `MED-02`, `MED-03` y `MED-05`.

## Coherencia Jira / repositorio

Consulta de Jira realizada el 30 de julio de 2026:

| Jira | Estado | Coherencia observada |
|---|---|---|
| `PG-11` | En curso | Coherente con `MED-02` y `MED-03` sin evidencia convergida completa |
| `PG-12` | Listo | Coherente con `ADV-04` a `ADV-06` verificados |
| `PG-13` | Listo | Coherente con `MED-04` verificado y frontera de `MED-05` |
| `PG-14` | Listo | Coherente con persistencia local; no acredita `ADV-02` |
| `PG-15` | Por hacer | Coherente con Docker y despliegue no iniciados |
| `PG-16` | Por hacer | Coherente con benchmark neuronal no iniciado |
| `PG-17` | Por hacer | Coherente con drift y promoción no iniciados |

El Epic `PG-9` permanece `Por hacer`, aunque varias historias hijas están
completadas. Es una discrepancia operativa de Jira, no un defecto de evidencia
del repositorio.

## Discrepancias reproducibles

1. `scripts/quality/check_repository.py` validaba un gráfico del 27 de julio,
   distinto del recurso activo enlazado; por ello CI no detectaba un gráfico
   obsoleto.
2. El gráfico activo del 28 de julio mostraba `11/25`, mientras el estado
   canónico es `15/25`.
3. El resumen global de `delivery_levels.md` decía «Avanzado: No iniciado»
   aunque `ADV-04`, `ADV-05` y `ADV-06` figuran verificados.
4. `AGENTS.md`, `.specify/intent.md`, `openspec/config.yaml`, arquitectura,
   API y amenaza seguían negando persistencia o feedback local ya integrados.
5. README y guion publicaban métricas de dos reconstrucciones sin identificar
   siempre el corte y tamaño correspondientes, lo que podía hacerlas parecer
   contradictorias.
6. README abría con lenguaje promocional y duplicaba demasiado detalle antes
   de explicar arquitectura, evidencia y límites.
7. `pyproject.toml` conservaba la descripción placeholder
   `Add your description here`.
8. OpenSpec conserva tres cambios completados sin archivar y uno anterior de
   persistencia con 9/10 tareas, pese a cambios posteriores archivados. No se
   archivan en esta auditoría porque requieren revisión humana.
9. La batería completa del frontend reveló tres incompatibilidades TypeScript
   en el flujo de feedback, un test dependiente de la variable local de API y
   seis archivos fuera del formato exigido. Los tests parciales usados durante
   la implementación no habían detectado el conjunto.

Las discrepancias 1 a 7 y 9 se corrigen en
`docs/PG-9-audit-project-truth`. La discrepancia 8 permanece como
housekeeping sujeto a revisión humana.

## Fuentes canónicas por afirmación

| Afirmación | Fuente |
|---|---|
| Estados ESS/MED/ADV/EXP | `docs/project_management/delivery_levels.md` |
| Target y once clases | `config/cfpb_target_contract.json` |
| Partición y entrenamiento | `config/cfpb_training_policy.json` |
| Métricas del baseline | `reports/validation/cfpb_baseline_metrics.json` |
| Evaluación esencial | `reports/validation/cfpb_essential_evaluation.md` |
| Comparación MED-01 | `reports/validation/med_01_comparison.md` |
| Quality gates | `reports/validation/cfpb_quality_gates.md` |
| Inferencia local | `reports/validation/claimvox_local_inference_smoke.md` |
| Feedback local E2E | `reports/validation/claimvox_local_feedback_e2e.md` |
| Contrato HTTP | `docs/api/openapi.json` |

## Riesgos y pendientes

- `MED-02` y `MED-03` no pueden verificarse sin CV completa convergida y
  evidencia final de variabilidad y optimización; no hay Champion.
- `MED-05` no dispone de corpus gobernado ni pipeline de incorporación.
- `ADV-01`, `ADV-02` y `ADV-03` requieren Docker, base compartida y despliegue,
  respectivamente.
- Los cambios OpenSpec activos antiguos y el estado del Epic `PG-9` deben
  revisarse como housekeeping independiente.
- La etiqueta `v0.1.0-essential-mvp` debe conservarse en su commit histórico.
- No debe crearse aún una etiqueta nueva: frontend declara `0.2.0`, mientras
  paquete Python y servicio declaran `0.1.0`. Tras reconciliar la versión y
  fusionar esta auditoría, el nombre propuesto es
  `v0.2.0-local-governed-workflow`, dejando explícito que no es un despliegue.

## Verificación de la auditoría

- Suites Python unitarias, de contrato e integración: superadas.
- Frontend: typecheck, ESLint, Prettier, 52 tests y build PWA: superados.
- Calidad de repositorio: 579 archivos versionados y 639 locales comprobados.
- OpenSpec: 30 cambios y specs válidos en modo estricto.
- Arnés: Node.js, OpenSpec, raíz de proyecto y validación estricta correctos.
- `git diff --check`: superado.

No se ejecutaron entrenamiento, validación cruzada completa, datasets ni
procesos de despliegue.
