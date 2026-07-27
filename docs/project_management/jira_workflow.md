# Jira, OpenSpec y GitHub: manual operativo

Este documento explica cómo utilizar los tres sistemas sin repetir información.
La regla principal es sencilla:

> Jira dice quién y en qué estado; OpenSpec dice qué debe cumplirse; GitHub
> demuestra qué se cambió y cómo se comprobó.

## Tablero del proyecto

- Proyecto Jira: [`PG`](https://miguel-redondo.atlassian.net/jira/software/projects/PG/boards).
- Épico activo: [`PG-1`](https://miguel-redondo.atlassian.net/browse/PG-1).
- Repositorio: [`Proyecto6-Grupo1`](https://github.com/Bootcamp-IA-MAD-P7/Proyecto6-Grupo1).

No se guardan tokens de Jira en el repositorio. El arnés local valida la clave,
pero no necesita conectarse a Atlassian.

## Backlog esencial

| Jira | Responsable funcional | Resultado | Fuente de requisitos | Estado inicial |
|---|---|---|---|---|
| `PG-2` | Víctor | EDA y decisiones de datos | `specs/001-cfpb-target-contract/`, `T-004` a `T-006` | Listo; preparación cerrada |
| `PG-3` | Víctor | Baseline multiclase | Cambio OpenSpec por crear | Pendiente de inicio; `PG-2` ya no lo bloquea |
| `PG-4` | Abel | React PWA ClaimVox | `specs/003-complaint-routing-experience/`, `T-006` | Integrado mediante PR #25 y evolución visual PR #28 |
| `PG-5` | José | Backend de inferencia | `specs/003-complaint-routing-experience/`, `T-007` | Bloqueada por `PG-3` |
| `PG-6` | Equipo | Integración de extremo a extremo | Cambio OpenSpec por crear | Bloqueada por `PG-3`, `PG-4` y `PG-5` |
| `PG-7` | Equipo | Métricas e informe técnico | Cambio OpenSpec por crear | Bloqueada por `PG-3` y `PG-6` |

Jira confirma el cierre de `PG-2`, la responsabilidad de Víctor sobre `PG-3`
y la integración de `PG-4` de Abel. La cuenta de José y los responsables de
`PG-6` y `PG-7` siguen sin confirmarse; no deben asignarse por suposición.

## Qué se escribe en cada lugar

| Lugar | Sí contiene | No contiene |
|---|---|---|
| Jira | Responsable, estado, prioridad, bloqueos y enlace al repositorio | Specs completas, datasets, narrativas o secretos |
| OpenSpec | Propuesta, requisitos, diseño, tareas, decisiones y aceptación | Seguimiento diario de personas |
| GitHub | Rama, código, tests, informe, diff, revisión y Pull Request | Decisiones no versionadas |
| Daily | Actividad real, siguiente paso y bloqueantes comunicados | Requisitos duplicados o trabajo inventado |

## Empezar una tarea nueva

### 1. Abrir el ticket

Leer el objetivo, las dependencias y la fuente versionada. Si el ticket está
bloqueado, no se implementa la parte bloqueada.

### 2. Actualizar el clon

```bash
git switch dev
git pull --ff-only
npm ci
python scripts/harness.py doctor
```

### 3. Crear una rama identificable

```bash
git switch -c tipo/PG-N-descripcion-corta
```

Ejemplos:

```bash
git switch -c data/PG-2-complete-cfpb-eda
git switch -c feature/PG-4-build-complaint-pwa
git switch -c feature/PG-5-add-inference-service
```

Dependabot y automatizaciones administradas conservan sus nombres automáticos.
Las ramas heredadas que ya existían antes de esta regla no se renombran solo por
estética.

### 4. Preparar el cambio OpenSpec

Para trabajo nuevo:

```bash
npm exec -- openspec new change nombre-del-cambio \
  --goal "Resultado observable"
```

La propuesta debe incluir:

```markdown
## Tracking

- Jira: `PG-N`.
```

Si es imposible crear un ticket, solo se permiten estas excepciones:

- `bootstrap`: crea el propio mecanismo de seguimiento;
- `emergency`: corrección urgente que debe justificarse;
- `automation`: actualización automática, como Dependabot.

La excepción y su motivo deben aparecer en la propuesta y en la Pull Request.

### 5. Preparar el contexto para la IA

```bash
python scripts/harness.py start \
  --role <rol> \
  --change <nombre-del-cambio> \
  --jira PG-N
```

Para este cambio de implantación, que crea el propio mecanismo:

```bash
python scripts/harness.py start \
  --role architect \
  --change integrate-jira-workflow \
  --jira-exception bootstrap
```

El arnés comprueba el formato, incorpora la referencia al paquete y recuerda a la
IA que Jira no sustituye los requisitos.

## Trabajo heredado

Las tareas que ya estaban asignadas antes de Jira conservan sus identificadores:

```bash
python scripts/harness.py start \
  --role data-analyst \
  --spec 001 \
  --task T-004
```

El arnés relaciona automáticamente `001/T-004` con `PG-2`, `003/T-006` con
`PG-4` y `003/T-007` con `PG-5`. Si una entrega heredada cambia alcance o
contratos, se abre un cambio OpenSpec antes de implementar esa decisión.

## Durante el trabajo

- Jira se actualiza al comenzar, bloquearse, entrar en revisión o terminar.
- OpenSpec se actualiza si cambian alcance, requisitos, diseño o decisiones.
- Las tareas se marcan como completas solo después de verificar.
- No se copian narrativas CFPB, CSV, secretos ni evidencias sensibles a Jira o IA.

Comandos de contexto:

```bash
python scripts/harness.py verify \
  --role <rol> \
  --change <nombre-del-cambio> \
  --jira PG-N

python scripts/harness.py review \
  --role <rol> \
  --change <nombre-del-cambio> \
  --jira PG-N
```

## Pull Request y cierre

La PR debe enlazar:

- Jira `PG-N` o la excepción aprobada;
- el cambio OpenSpec;
- las tareas terminadas;
- las comprobaciones y evidencias reales.

Se puede pedir a cualquier IA:

```text
Lee .github/pull_request_template.md, el cambio OpenSpec y el diff.
Completa toda la plantilla en Markdown.
Usa la referencia Jira indicada y no inventes pruebas ni evidencias.
```

Antes del merge se comprueba que Jira, OpenSpec y GitHub describen el mismo
estado. Un ticket cerrado no prueba por sí solo que una capacidad funcione.
