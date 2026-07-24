# Flujo de proyecto

<<<<<<< HEAD
Esta guía explica cómo trabaja una persona del equipo, utilice o no una IA. Jira mantiene el estado operativo; el repositorio conserva contratos, decisiones y evidencias.

Jira comenzará a utilizarse el 23 de julio de 2026. Hasta que se publique su enlace, la asignación vigente se consulta en `docs/project_management/team.md` y en los `tasks.md` de cada spec.

## Mapa sencillo
=======
Jira organiza el trabajo; OpenSpec define y conserva el cambio; el arnés prepara el contexto; GitHub protege la integración.
>>>>>>> 5558ae2204151767a53be0e45102bd04a3b6da83

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

<<<<<<< HEAD
## 6. Responsabilidades actuales

| Persona | Área principal | Tarea activa | Qué debe entregar |
|---|---|---|---|
| Miguel | Arquitectura y coherencia transversal | Gobierno de specs y contratos | Decisiones consistentes, límites claros, documentación y quality gates |
| José | Backend | `003/T-007` | Revisión y preparación del adaptador; implementación real solo cuando se levanten los bloqueos |
| Abel | Frontend y UX | `003/T-008` | PWA mock verificable, accesible, responsive e instalable |
| Víctor | Datos y EDA | `001/T-004` | Notebook reproducible, métricas y gráficos agregados sin narrativas reales |

Josué ya no forma parte del equipo. Las personas de respaldo todavía deben acordarse.

## 7. Paquetes de contexto para cada área

Si la IA puede leer el repositorio, basta con indicarle la spec y la tarea. Si no puede hacerlo, cada responsable puede generar un único archivo temporal con el contexto necesario.

### Víctor: análisis del CSV y EDA

```bash
python scripts/documentation/build_ai_handoff.py \
  --spec 001-cfpb-target-contract \
  --task T-004 \
  --include reports/validation/cfpb_viability.md \
  --include docs/product/candidates/CAND-001-cfpb-complaint-routing.md
```

### Abel: frontend y UX

```bash
python scripts/documentation/build_ai_handoff.py \
  --spec 003-complaint-routing-experience \
  --task T-008 \
  --include app/interface/README.md \
  --include reports/validation/complaint_routing_pwa.md \
  --include docs/design/design_system.md \
  --include docs/security/threat_model.md
```

### José: backend

```bash
python scripts/documentation/build_ai_handoff.py \
  --spec 003-complaint-routing-experience \
  --task T-007 \
  --include docs/api/openapi.json \
  --include docs/architecture/system_blueprint.md \
  --include docs/security/threat_model.md
```

El paquete de José permite revisar el contrato y preparar el trabajo. No elimina los bloqueos de `T-007` ni autoriza una inferencia real. Los archivos generados viven en `exports/ai-handoffs/`, están excluidos de Git y deben revisarse antes de compartirlos.

## 8. Verificación y Pull Request
=======
1. Todo cambio relevante nuevo comienza en `openspec/changes/`.
2. Las tareas numeradas existentes se terminan en modo compatibilidad.
3. Una entrega heredada que altere alcance o contratos se adapta mediante OpenSpec antes de mergear.
4. La implementación no comienza con planificación incompleta.
5. Una tarea no se cierra sin comprobaciones y evidencia.
6. Archivar OpenSpec precede al cierre de la PR.
7. La persona responsable conserva diff, commit, push, archivo y merge bajo su control.
>>>>>>> 5558ae2204151767a53be0e45102bd04a3b6da83

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

<<<<<<< HEAD
## 9. Ejemplo para el equipo EDA

El equipo EDA trabaja en `001/T-004`. Puede estudiar clases, tiempo, ausencias, duplicados, conflictos, longitud e idioma. Debe devolver notebooks reproducibles, cifras y gráficos agregados. No debe incluir narrativas reales ni utilizar como features columnas prohibidas por `config/cfpb_target_contract.json`.

## 10. Cierre de una fase

Una fase se cierra cuando sus criterios tienen evidencia, las decisiones están registradas, la documentación coincide con lo construido y no quedan preguntas bloqueantes. Solo entonces se crea un release o se avanza a la siguiente puerta de entrega.
=======
La ejecución paso a paso está en [harness_quickstart.md](harness_quickstart.md).
La frontera y el uso diario de Jira están en [jira_workflow.md](jira_workflow.md).
>>>>>>> 5558ae2204151767a53be0e45102bd04a3b6da83
