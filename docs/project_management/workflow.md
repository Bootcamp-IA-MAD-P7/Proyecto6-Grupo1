# Flujo de proyecto

Esta guía explica cómo trabaja una persona del equipo, utilice o no una IA. Jira mantiene el estado operativo; el repositorio conserva contratos, decisiones y evidencias.

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

1. Leer la historia de Jira y localizar la spec y tarea indicadas.
2. Actualizar `dev` y crear una rama pequeña.
3. Leer `AGENTS.md`, `README.md`, `CONTRIBUTING.md` y el bundle de la spec.
4. Confirmar qué queda fuera del alcance y qué preguntas bloquean.
5. Indicar en Jira que el trabajo está en curso.

```bash
git switch dev
git pull --ff-only
git switch -c <tipo>/<descripcion>
```

## 2. Trabajar con una IA que accede al repositorio

Abrir la raíz del proyecto y utilizar esta instrucción, adaptando spec y tarea:

```text
Lee AGENTS.md, README.md y CONTRIBUTING.md.

Trabaja únicamente en la tarea T-004 de
specs/001-cfpb-target-contract/tasks.md.

Lee también spec.md, plan.md y decisions.md de esa carpeta.
Antes de editar, resume el alcance, los archivos previstos y los bloqueantes.
No amplíes el alcance ni inventes decisiones pendientes.
Al terminar, ejecuta las verificaciones de la tarea y presenta evidencias.
```

No es necesario copiar todos los Markdown al chat: el agente debe leerlos desde el repositorio.

## 3. Trabajar con una IA sin acceso al repositorio

Generar un único paquete temporal desde fuentes versionadas:

```bash
python scripts/documentation/build_ai_handoff.py \
  --spec 001-cfpb-target-contract \
  --task T-004 \
  --include reports/validation/cfpb_viability.md
```

El archivo se crea en `exports/ai-handoffs/`, que está excluido de Git. Debe revisarse antes de compartirlo. No se adjuntarán datasets, `.env`, modelos, logs ni narrativas reales.

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

1. Ejecutar las pruebas de la spec y `python scripts/quality/check_repository.py`.
2. Revisar `git diff --check` y el diff completo.
3. Actualizar tarea, decisión y documentación realmente afectadas.
4. Crear un commit descriptivo y publicar la rama.
5. Abrir Pull Request hacia `dev` con la plantilla completa.
6. Resolver checks y conversaciones antes del merge.

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
