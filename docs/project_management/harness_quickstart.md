# Manual sencillo: OpenSpec + arnés

Este manual permite trabajar desde el repositorio con cualquier IA. Nadie tiene que esperar a que Miguel le prepare archivos.

## Qué hace cada pieza

| Pieza | Explicación corriente |
|---|---|
| Jira | Dice quién hace el trabajo y en qué estado está |
| OpenSpec | Guarda qué se quiere cambiar, qué debe cumplir y qué tareas hay |
| Arnés | Da a la IA las reglas, el rol y el contexto correctos |
| Git y Pull Request | Conservan el cambio y permiten revisarlo antes de unirlo |
| Persona responsable | Decide, revisa el diff y autoriza la publicación |

OpenSpec está instalado dentro del repositorio. No hace falta instalarlo globalmente ni elegir una IA concreta.

## 0. Primera preparación

Se hace una vez por clon:

```bash
git clone https://github.com/Bootcamp-IA-MAD-P7/Proyecto6-Grupo1.git
cd Proyecto6-Grupo1
git switch dev
npm ci
python scripts/harness.py doctor
```

El diagnóstico correcto muestra cuatro líneas `PASS`: Node.js, OpenSpec, raíz del proyecto y validación estricta.

Requisitos:

- Git;
- Python 3.12;
- Node.js 20.19 o superior;
- acceso de lectura al repositorio.

## 1. Actualizar antes de cada tarea

```bash
git switch dev
git pull --ff-only
npm ci
python scripts/harness.py doctor
git status --short --branch
```

Si hay cambios locales inesperados, se para y se revisan. No se borran.

## 2. Leer la asignación

Abrir:

- `docs/project_management/team.md`;
- la historia Jira `PG-N` o la excepción permitida;
- `docs/project_management/delivery_levels.md`.

Jira no contiene los requisitos completos. Solo enlaza el cambio OpenSpec y permite seguir su estado. El [manual de Jira](jira_workflow.md) recoge el backlog y sus límites.

## 3. Crear una rama

```bash
git switch -c tipo/PG-N-descripcion-corta
```

Ejemplos:

```bash
git switch -c data/PG-2-analyze-language
git switch -c feature/PG-4-complaint-form
git switch -c docs/PG-7-update-client-narrative
```

## 4. Crear un cambio OpenSpec

Solo se crea para trabajo nuevo o para una entrega heredada que cambie decisiones o contratos:

```bash
npm exec -- openspec new change nombre-del-cambio \
  --goal "Resultado observable que se quiere conseguir"
```

El nombre usa minúsculas y guiones. La carpeta aparecerá en:

```text
openspec/changes/nombre-del-cambio/
```

La propuesta incorpora su seguimiento:

```markdown
## Tracking

- Jira: `PG-N`.
```

Las únicas excepciones admitidas son `bootstrap`, `emergency` y `automation`;
deben incluir motivo en la propuesta y en la Pull Request.

La IA debe completar, en este orden, los artefactos que pida OpenSpec:

```text
proposal.md  -> por qué y qué cambia
specs/       -> requisitos comprobables
design.md    -> cómo se plantea resolverlo
tasks.md     -> pasos pequeños y verificables
```

Instrucción sencilla para cualquier IA con acceso al repositorio:

```text
Lee AGENTS.md y openspec/config.yaml.
Trabaja con OpenSpec sobre el cambio <nombre-del-cambio>.
Completa primero los artefactos de planificación que falten.
No implementes nada hasta que la planificación esté completa y validada.
Antes de editar, dime alcance, archivos, bloqueantes y comprobaciones.
No inventes decisiones ni evidencias.
```

Comandos de apoyo:

```bash
npm exec -- openspec status --change nombre-del-cambio
npm exec -- openspec instructions proposal --change nombre-del-cambio
npm exec -- openspec instructions specs --change nombre-del-cambio
npm exec -- openspec instructions design --change nombre-del-cambio
npm exec -- openspec instructions tasks --change nombre-del-cambio
npm exec -- openspec validate nombre-del-cambio --type change --strict
```

Las carpetas `.codex/`, `.github/`, `.claude/`, `.cursor/` y `.gemini/` ya contienen los adaptadores oficiales generados por OpenSpec. Cada herramienta puede reconocer sus skills o comandos; el flujo de terminal anterior funciona siempre.

## 5. Dar contexto a la IA mediante el arnés

Cuando la planificación esté completa:

```bash
python scripts/harness.py start \
  --role architect \
  --change nombre-del-cambio \
  --jira PG-N
```

Roles disponibles:

- `architect`;
- `data-analyst`;
- `backend-developer`;
- `frontend-developer`.

El comando consulta al OpenSpec real, valida el cambio y crea un único Markdown en `exports/ai-handoffs/`.

- Si la IA ve el repositorio, se le indica que lea ese archivo.
- Si no ve el repositorio, se sube únicamente ese Markdown después de revisarlo.
- Nunca se suben CSV, narrativas CFPB, secretos, modelos, `.env` o logs.
- El arnés valida la forma `PG-N`, pero no almacena credenciales ni consulta Jira.

## 6. Trabajo anterior a OpenSpec

Víctor y Abel pueden terminar las tareas ya asignadas sin rehacerlas:

```bash
python scripts/harness.py start \
  --role data-analyst \
  --spec 001 \
  --task T-004
```

```bash
python scripts/harness.py start \
  --role frontend-developer \
  --spec 003 \
  --task T-006
```

Esta opción es transitoria. Si durante el trabajo aparece una decisión nueva que cambia el contrato, se crea antes un cambio OpenSpec.

## 7. Implementar y verificar

Se trabajan las tareas de `openspec/changes/<nombre>/tasks.md` en orden. Al completar una:

1. se ejecutan sus comprobaciones;
2. se registra evidencia real;
3. se cambia `[ ]` por `[x]`.

Contexto de verificación:

```bash
python scripts/harness.py verify \
  --role <rol> \
  --change nombre-del-cambio \
  --jira PG-N
```

Comprobaciones mínimas:

```bash
npm run openspec:validate
python scripts/quality/check_repository.py
python -m unittest discover -s tests/unit -p "test_*.py" -v
python -m unittest discover -s tests/contract -p "test_*.py" -v
git diff --check
git status --short
```

Cada área añade sus propios tests.

## 8. Revisar el cambio

```bash
python scripts/harness.py review \
  --role <rol> \
  --change nombre-del-cambio \
  --jira PG-N
```

La IA ayuda a buscar contradicciones, riesgos, datos sensibles y evidencia ausente. La persona responsable revisa el diff completo.

## 9. Archivar y preparar la Pull Request

Cuando todas las tareas estén marcadas y verificadas:

```bash
npm exec -- openspec archive nombre-del-cambio --yes
```

Archivar:

- mueve el expediente terminado al histórico;
- actualiza `openspec/specs/` con la capacidad vigente;
- no hace commit, push ni merge.

Después:

```bash
git add <archivos-revisados>
git diff --cached --check
git commit -m "tipo: descripción breve"
git push -u origin <rama>
```

Se abre una Pull Request hacia `dev`. La plantilla aparece automáticamente. Puede pedirse a la IA:

```text
Lee .github/pull_request_template.md y el diff de esta rama.
Devuélveme la plantilla completa en Markdown.
No inventes tests, evidencias ni resultados.
```

Solo hay que copiar y pegar el Markdown resultante en la descripción de la PR.
La plantilla exige la clave Jira o una excepción aprobada y el cambio OpenSpec.

## 10. Cierre

Antes del merge:

- OpenSpec y CI pasan;
- no quedan conversaciones pendientes;
- las tareas y evidencias coinciden;
- la daily refleja únicamente aportaciones reales;
- NotebookLM se actualiza solo si cambian hechos útiles para la presentación;
- una persona confirma el merge.

## Errores frecuentes

| Mensaje o situación | Qué hacer |
|---|---|
| `OpenSpec is not installed locally` | Ejecutar `npm ci` |
| `planning artifacts are incomplete` | Completar propuesta, requisitos, diseño y tareas |
| `does not pass strict validation` | Ejecutar la validación y corregir requisitos o escenarios |
| `unfinished tasks` al preparar PR | Verificar y marcar las tareas restantes |
| Tarea heredada contradice una decisión | Abrir un cambio OpenSpec antes de seguir |
| La IA pide el CSV o narrativas | No compartirlos; utilizar evidencias agregadas y contratos |
