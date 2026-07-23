# Flujo de proyecto

Esta guía explica cómo trabaja una persona del equipo, utilice o no una IA. Jira mantiene el estado operativo; el repositorio conserva contratos, decisiones y evidencias.

La incorporación paso a paso está en la [guía autoservicio del arnés](harness_quickstart.md).

## Mapa sencillo

```text
Historia de Jira
      ↓
Spec y tarea
      ↓
Rama desde dev
      ↓
Trabajo con o sin IA
      ↓
Pruebas y evidencias
      ↓
Pull Request
      ↓
Merge y actualización de Jira
```

## 1. Antes de empezar

1. Clonar o actualizar el repositorio desde GitHub.
2. Leer la historia de Jira y localizar en `team.md` la spec y tarea indicadas.
3. Actualizar `dev` y crear una rama pequeña.
4. Preparar desde el propio clon el contexto del rol, spec y tarea.
5. Leer `AGENTS.md`, el briefing y el bundle de la spec.
6. Confirmar qué queda fuera del alcance y qué preguntas bloquean.
7. Indicar en Jira que el trabajo está en curso.

```bash
git switch dev
git pull --ff-only
git switch -c <tipo>/<descripcion>
```

## 2. Preparar el contexto desde el repositorio

Cada integrante ejecuta el arnés desde su propio clon. Ejemplo:

```bash
python scripts/harness.py start \
  --role data-analyst \
  --spec 001 \
  --task T-004
```

Si la IA accede al repositorio, lee el paquete generado desde `exports/ai-handoffs/`. No es necesario copiar documentos al chat.

## 3. Trabajar con una IA sin acceso al repositorio

La propia persona sube únicamente el mismo paquete generado. El archivo está excluido de Git y debe revisarse antes de compartirlo. No se adjuntarán datasets, `.env`, modelos, logs ni narrativas reales.

## 4. Durante el trabajo

- Trabajar solo en la tarea acordada.
- Convertir decisiones nuevas en cambios de spec o `decisions.md` antes de contradecir el contrato.
- Mantener datos brutos y artefactos locales fuera de Git.
- Hacer comprobaciones pequeñas durante la implementación.
- No marcar una tarea como completada hasta disponer de evidencia.
- No actualizar documentos sin impacto real solo para aumentar el volumen de cambios.

## 5. Qué actualiza cada persona

| Elemento | Cuándo se actualiza | Responsable |
|---|---|---|
| Jira | Inicio, bloqueo, revisión y cierre | Persona asignada |
| `tasks.md` | Cambia estado o aparece evidencia | Persona responsable de la tarea |
| `decisions.md` | Se toma o revisa una decisión relevante | PR que introduce la decisión |
| Daily | Actividad, plan o bloqueo del día | Cada integrante en su apartado |
| README | Cambia el estado general o la forma de usar el proyecto | PR que produce el cambio |
| CHANGELOG | Cambio relevante para una entrega | PR que produce el cambio |
| NotebookLM | Cambian hechos, métricas o narrativa verificable | PR que produce el cambio |

No todo el equipo debe actualizar todos los documentos en cada PR.

## 6. Verificación y Pull Request

1. Generar el contexto `verify` y ejecutar las pruebas de la spec.
2. Ejecutar `python scripts/quality/check_repository.py`.
3. Revisar `git diff --check` y el diff completo.
4. Generar el contexto `review` y atender los hallazgos.
5. Actualizar tarea, decisión y documentación realmente afectadas.
6. Crear un commit descriptivo y publicar la rama.
7. Generar el contexto `prepare-pr` y completar la plantilla.
8. Abrir Pull Request hacia `dev`.
9. Resolver checks y conversaciones antes del merge.

El cierre debe indicar:

- spec y tarea;
- archivos modificados;
- comandos y resultados;
- decisiones;
- riesgos o trabajo pendiente.

## 7. Ejemplo para el equipo EDA

El equipo EDA trabaja en `001/T-004`. Puede estudiar clases, tiempo, ausencias, duplicados, conflictos, longitud e idioma. Debe devolver notebooks reproducibles, cifras y gráficos agregados. No debe incluir narrativas reales ni utilizar como features columnas prohibidas por `config/cfpb_target_contract.json`.

## 8. Cierre de una fase

Una fase se cierra cuando sus criterios tienen evidencia, las decisiones están registradas, la documentación coincide con lo construido y no quedan preguntas bloqueantes. Solo entonces se crea un release o se avanza a la siguiente puerta de entrega.
