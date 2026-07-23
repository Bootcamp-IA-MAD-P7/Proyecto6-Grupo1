# Flujo de proyecto

Jira organiza el trabajo; OpenSpec define y conserva el cambio; el arnés prepara el contexto; GitHub protege la integración.

```text
Jira
  -> cambio OpenSpec
  -> propuesta + requisitos + diseño + tareas
  -> rama
  -> arnés + trabajo
  -> pruebas + revisión
  -> archivo OpenSpec
  -> Pull Request
  -> CI + revisión humana
  -> dev
```

## Responsabilidad de cada sistema

| Sistema | Conserva | No sustituye |
|---|---|---|
| Jira | Responsable, prioridad, estado y fechas | Requisitos o decisiones |
| OpenSpec | Cambio acordado, requisitos, diseño, tareas y capacidad vigente | Revisión humana |
| Arnés | Reglas, rol, contexto y feedback para la IA | Implementación ni autorización |
| GitHub | Historial, PR, checks y releases | Criterio profesional del equipo |

## Reglas operativas

1. Todo cambio relevante nuevo comienza en `openspec/changes/`.
2. Las tareas numeradas existentes se terminan en modo compatibilidad.
3. Una entrega heredada que altere alcance o contratos se adapta mediante OpenSpec antes de mergear.
4. La implementación no comienza con planificación incompleta.
5. Una tarea no se cierra sin comprobaciones y evidencia.
6. Archivar OpenSpec precede al cierre de la PR.
7. La persona responsable conserva diff, commit, push, archivo y merge bajo su control.

## Documentación que puede cambiar

| Elemento | Cuándo |
|---|---|
| Jira | Inicio, bloqueo, revisión y cierre |
| Cambio OpenSpec | Alcance, requisitos, diseño, tareas o evidencia |
| Daily | Actividad, plan y bloqueos reales de cada persona |
| README | Cambia el estado global o la forma de uso |
| CHANGELOG | Cambio relevante para la entrega |
| NotebookLM | Cambian hechos, métricas o narrativa útil para cliente |

No se actualizan todos los documentos por rutina. Se actualizan porque cambió su significado.

La ejecución paso a paso está en [harness_quickstart.md](harness_quickstart.md).
La frontera y el uso diario de Jira están en [jira_workflow.md](jira_workflow.md).
