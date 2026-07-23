# Guía autoservicio para trabajar con IA

Esta guía permite que cualquier integrante empiece desde el repositorio sin recibir archivos preparados por otra persona y sin depender de una herramienta de IA concreta.

## Qué hace el arnés

El arnés reúne automáticamente:

- reglas del proyecto;
- intención y briefing;
- rol;
- spec, plan, tareas y decisiones;
- contratos de datos o API relacionados;
- procedimiento de inicio, verificación, revisión o Pull Request.

No ejecuta una tarea por su cuenta, no comparte datos, no hace commits y no fusiona cambios.

## Requisitos locales

- Git y acceso de lectura al repositorio.
- Python `3.12`, que es la versión utilizada por CI.
- Una terminal situada en la raíz del clon.

Comprobación inicial:

```bash
python --version
python scripts/harness.py --help
```

GitHub CLI no es necesario para generar contexto ni trabajar en local. Solo facilita algunas operaciones posteriores con Pull Requests.

## 1. Obtener el repositorio

La primera vez:

```bash
git clone https://github.com/Bootcamp-IA-MAD-P7/Proyecto6-Grupo1.git
cd Proyecto6-Grupo1
git switch dev
```

Si el repositorio ya está clonado:

```bash
git switch dev
git pull --ff-only
```

Antes de trabajar debe aparecer:

```text
## dev...origin/dev
```

## 2. Consultar la asignación

Abrir [`team.md`](team.md) y localizar:

- persona;
- rol;
- spec;
- tarea;
- estado o bloqueo.

Después comprobar la tarea en `specs/<spec>/tasks.md`. Jira indica asignación y estado operativo; el repositorio conserva el contrato y las evidencias.

Si la tarea está marcada `[!]`, no se implementa. Se informa del bloqueo y se espera una decisión o dependencia.

## 3. Crear una rama

```bash
git switch -c <tipo>/<descripcion-corta>
```

Ejemplos:

```bash
git switch -c data/cfpb-eda
git switch -c feature/inference-service
git switch -c docs/update-analysis
```

## 4. Preparar el contexto

Ejemplo para `data-analyst`, spec `001` y tarea `T-004`:

```bash
python scripts/harness.py start \
  --role data-analyst \
  --spec 001 \
  --task T-004
```

La terminal muestra una ruta dentro de:

```text
exports/ai-handoffs/
```

### Si la IA puede leer el repositorio

Abrir la raíz del proyecto en la herramienta y escribir:

```text
Lee el paquete generado en exports/ai-handoffs/.

No modifiques nada todavía.
Explícame el objetivo, el alcance, los archivos previstos,
los bloqueantes, los requisitos del briefing y las comprobaciones.
Después trabaja únicamente en la tarea indicada.
```

Si la IA dispone de terminal, también puede ejecutar el comando del arnés por petición de la persona responsable.

### Si la IA no puede leer el repositorio

Subir únicamente el Markdown generado y utilizar la misma instrucción. No se seleccionan documentos manualmente y nunca se adjuntan datasets, narrativas, secretos, modelos ni logs.

## 5. Trabajar

La IA debe explicar antes de editar:

1. qué pide la tarea;
2. qué queda fuera;
3. qué archivos propone modificar;
4. qué decisiones están abiertas;
5. cómo comprobará el resultado.

La persona responsable revisa el alcance y el diff. El rol orienta a la IA, pero no le concede permiso para ignorar bloqueos ni tomar decisiones pendientes.

## 6. Verificar

Preparar el contexto de verificación:

```bash
python scripts/harness.py verify \
  --role <rol> \
  --spec <spec> \
  --task <T-XXX>
```

Como mínimo deben ejecutarse:

```bash
git diff --check
python scripts/quality/check_repository.py
git status --short --branch
```

Además se ejecutan los tests definidos en la tarea. Un resultado con checks fallidos no se presenta como terminado.

## 7. Revisar

Preparar una revisión independiente:

```bash
python scripts/harness.py review \
  --role <rol> \
  --spec <spec> \
  --task <T-XXX>
```

La revisión busca defectos, riesgos, fugas de datos, contratos rotos, tests ausentes y afirmaciones que no coincidan con el estado real.

## 8. Preparar la Pull Request

Cuando la tarea esté verificada y marcada `[x]`:

```bash
python scripts/harness.py prepare-pr \
  --role <rol> \
  --spec <spec> \
  --task <T-XXX>
```

La IA debe leer `.github/pull_request_template.md` y devolverla completa en Markdown. La persona copia ese contenido en la PR, revisa las casillas y firma el cambio.

Después:

```bash
git add <archivos-revisados>
git commit -m "tipo: descripción del cambio"
git push -u origin <rama>
```

La Pull Request apunta a `dev`. No se hace merge hasta que los checks pasen y las conversaciones estén resueltas.

## Relación con el briefing

Todo paquete incluye [`delivery_levels.md`](delivery_levels.md). La IA debe indicar qué identificadores `ESS`, `MED`, `ADV` o `EXP` afecta la tarea.

Un requisito solo cambia a `Verificado` cuando existe la evidencia mínima definida en ese documento.

## Relación con Jira

Cada historia debe incluir, como mínimo:

```text
Spec: specs/<spec>/
Tarea: T-XXX
Responsable:
Criterios del briefing:
```

Jira mantiene asignación, prioridad y estado diario. La spec conserva el contrato; Git y la Pull Request conservan implementación y evidencias. Si se contradicen, se detiene el trabajo y se corrige el origen antes de continuar.

## Si algo falla

| Mensaje | Qué significa |
|---|---|
| `Unknown role` | El rol no existe en `ai-specs/agents/` |
| `Task ... does not exist` | La tarea o la spec no coinciden |
| `blocked` | La tarea tiene una dependencia sin resolver |
| `must be completed` | Se intentó preparar la PR antes de verificar la tarea |
| `Source ... is not allowed` | Se intentó incluir una fuente insegura o no versionada |

No se desactiva la comprobación. Se corrige la entrada o se consulta el bloqueo.
