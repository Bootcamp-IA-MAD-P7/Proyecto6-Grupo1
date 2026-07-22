# Tareas: Selección del problema de negocio

- Spec: `specs/000-problem-discovery/spec.md`
- Plan: `specs/000-problem-discovery/plan.md`

## T-001 Aprobar las reglas de evaluación

- Estado: `[x]`
- Responsable: `Equipo`
- Dependencias: `ninguna`
- Requisitos cubiertos: `R-007, R-008, AC-001`
- Archivos previstos:
  - `docs/product/idea_evaluation_template.md`
  - `specs/000-problem-discovery/decisions.md`
- Trabajo:
  - Resolver Q-001 a Q-004.
  - Definir escala, pesos, mínimos, puertas críticas, aprobación y desempate.
  - Versionar la matriz antes de puntuar candidatos.
- Criterio de cierre:
  - Las reglas están aceptadas, fechadas y no contienen candidatos preseleccionados.
- Verificación:
  - Comando o revisión: revisión del equipo y comprobación del diff.
  - Resultado esperado: matriz y decisión de gobierno trazables.
- Evidencia obtenida:
  - Versión `1.0` aprobada en `docs/product/idea_evaluation_template.md` con fecha `2026-07-22`.
  - Incluye puertas críticas, escala, pesos, umbrales, evidencia mínima, aprobación, desempate y relación con Jira.
  - Votos favorables: Abel, Víctor y Miguel. Ausente: José. Baja del equipo: Josué.
  - Jira queda confirmado como tablero operativo; su enlace se añadirá cuando se cree el proyecto.

## T-002 Registrar las propuestas candidatas

- Estado: `[ ]`
- Responsable: `Equipo`
- Dependencias: `T-001`
- Requisitos cubiertos: `R-001, R-002, R-010, AC-002`
- Archivos previstos:
  - `docs/product/`
- Trabajo:
  - Recoger propuestas con ID estable.
  - Completar problema, usuario, decisión, target potencial y clases.
  - Marcar como incompletas las propuestas que no alcancen el mínimo descriptivo.
- Criterio de cierre:
  - Todas las propuestas de la ronda usan el mismo contrato y tienen estado explícito.
- Verificación:
  - Comando o revisión: revisión de campos obligatorios.
  - Resultado esperado: ninguna idea se evalúa con información estructural ausente.
- Evidencia obtenida:
  - Pendiente.

## T-003 Validar el problema, usuario y decisión

- Estado: `[ ]`
- Responsable: `Producto / descubrimiento, por asignar`
- Dependencias: `T-002`
- Requisitos cubiertos: `R-001, R-008, AC-002, AC-007`
- Archivos previstos:
  - `docs/product/`
- Trabajo:
  - Contrastar necesidad, usuario, decisión, alternativa actual e impacto esperado.
  - Separar hechos, inferencias y supuestos.
- Criterio de cierre:
  - Cada candidato viable explica una decisión concreta y enlaza evidencia suficiente.
- Verificación:
  - Comando o revisión: revisión cruzada por una persona distinta de quien propuso la idea.
  - Resultado esperado: evidencia y supuestos claramente diferenciados.
- Evidencia obtenida:
  - Pendiente.

## T-004 Evaluar datasets y viabilidad multiclase

- Estado: `[ ]`
- Responsable: `Datos / ML, por asignar`
- Dependencias: `T-002`
- Requisitos cubiertos: `R-002, R-003, R-004, R-005, AC-003, AC-004`
- Archivos previstos:
  - `docs/product/`
  - `reports/validation/`
- Trabajo:
  - Registrar fuente, licencia, acceso y documentación.
  - Inspeccionar target, clases, volumen, ausencias, duplicados y distribución preliminar.
  - Revisar momento de inferencia y posibles fugas de información.
- Criterio de cierre:
  - Cada dataset queda como viable, bloqueado o descartado con evidencia reproducible.
- Verificación:
  - Comando o revisión: consulta o script documentado y revisión de licencia.
  - Resultado esperado: ningún dataset avanza sin acceso, licencia y encaje multiclase claros.
- Evidencia obtenida:
  - Pendiente.

## T-005 Evaluar seguridad, privacidad, ética y sesgo

- Estado: `[ ]`
- Responsable: `Seguridad / datos, por asignar`
- Dependencias: `T-002, T-004`
- Requisitos cubiertos: `R-006, AC-006`
- Archivos previstos:
  - `docs/product/`
  - `docs/security/`
- Trabajo:
  - Identificar datos sensibles, poblaciones afectadas, impacto del error y usos indebidos.
  - Proponer mitigaciones y determinar si algún riesgo bloquea la alternativa.
- Criterio de cierre:
  - Todos los candidatos viables tienen riesgos y mitigaciones explícitos.
- Verificación:
  - Comando o revisión: checklist de seguridad y revisión cruzada.
  - Resultado esperado: ningún riesgo crítico queda oculto por la puntuación total.
- Evidencia obtenida:
  - Pendiente.

## T-006 Evaluar UX, demo y evolución técnica

- Estado: `[ ]`
- Responsable: `Producto / UX / plataforma, por asignar`
- Dependencias: `T-003, T-004`
- Requisitos cubiertos: `R-009`
- Archivos previstos:
  - `docs/product/`
  - `docs/design/`
- Trabajo:
  - Valorar claridad de entradas, salida, explicación y decisión del usuario.
  - Evaluar viabilidad de demo, despliegue, feedback y progresión hasta nivel experto.
- Criterio de cierre:
  - Cada candidato viable tiene un recorrido de producto comprensible sin diseñar la solución final.
- Verificación:
  - Comando o revisión: revisión conjunta de producto, UX y plataforma.
  - Resultado esperado: no se confunde potencial con funcionalidad implementada.
- Evidencia obtenida:
  - Pendiente.

## T-007 Puntuar y comparar alternativas

- Estado: `[ ]`
- Responsable: `Equipo`
- Dependencias: `T-003, T-004, T-005, T-006`
- Requisitos cubiertos: `R-007, R-008, R-010, AC-005, AC-007`
- Archivos previstos:
  - `docs/product/idea_evaluation_template.md`
  - `docs/product/`
- Trabajo:
  - Aplicar la misma matriz a todos los candidatos viables.
  - Enlazar evidencia para cada puntuación.
  - Revisar sensibilidad a pesos y registrar desacuerdos.
- Criterio de cierre:
  - La comparación es reproducible y no oculta puertas críticas ni incertidumbre.
- Verificación:
  - Comando o revisión: recalcular totales y revisión cruzada de evidencias.
  - Resultado esperado: puntuaciones coherentes y razonamiento cualitativo disponible.
- Evidencia obtenida:
  - Pendiente.

## T-008 Registrar la decisión del equipo

- Estado: `[ ]`
- Responsable: `Equipo`
- Dependencias: `T-007`
- Requisitos cubiertos: `R-008, R-010, R-011, AC-007, AC-008, AC-009`
- Archivos previstos:
  - `specs/000-problem-discovery/decisions.md`
- Trabajo:
  - Aplicar el mecanismo de aprobación acordado.
  - Seleccionar una alternativa o registrar la no selección.
  - Conservar motivos, consecuencias, riesgos, supuestos y evidencia.
- Criterio de cierre:
  - Existe una decisión explícita, auditable y no contradictoria con las puertas críticas.
- Verificación:
  - Comando o revisión: revisión de criterios de aceptación y aprobación registrada.
  - Resultado esperado: una decisión válida o una no selección justificada.
- Evidencia obtenida:
  - Pendiente.

## T-009 Sincronizar documentación y fuentes

- Estado: `[ ]`
- Responsable: `Documentación / QA, por asignar`
- Dependencias: `T-008`
- Requisitos cubiertos: `R-013, AC-009`
- Archivos previstos:
  - `README.md`
  - `CHANGELOG.md`
  - `docs/notebooklm/project_facts.md`
  - `docs/notebooklm/technical_status.md`
  - `docs/project_management/dailies/`
- Trabajo:
  - Actualizar hechos y estado sin presentar hipótesis como decisiones.
  - Regenerar y revisar el paquete de NotebookLM.
- Criterio de cierre:
  - Todas las fuentes relevantes describen el mismo resultado de descubrimiento.
- Verificación:
  - Comando o revisión: `python scripts/documentation/build_notebooklm_pack.py --date <AAAA-MM-DD>`.
  - Resultado esperado: paquete coherente y sin afirmaciones contradictorias.
- Evidencia obtenida:
  - Pendiente.

## T-010 Preparar la primera spec funcional

- Estado: `[ ]`
- Responsable: `Equipo`
- Dependencias: `T-008, T-009`
- Requisitos cubiertos: `R-011, R-012, AC-010`
- Archivos previstos:
  - `specs/001-<nombre>/`
- Trabajo:
  - Trasladar problema, usuario, decisión, dataset, target, clases, riesgos y preguntas abiertas.
  - Definir alcance funcional sin implementar en esta spec.
- Criterio de cierre:
  - Existe una nueva spec coherente con la decisión y separada de `000-problem-discovery`.
- Verificación:
  - Comando o revisión: revisión de trazabilidad entre decisión y nueva spec.
  - Resultado esperado: la implementación futura parte de un contrato aprobado.
- Evidencia obtenida:
  - Pendiente.

## Checklist de cierre

- [ ] Todos los criterios de aceptación están cubiertos.
- [ ] Las pruebas y revisiones acordadas pasan.
- [ ] Las decisiones relevantes están registradas.
- [ ] La documentación coincide con el resultado real.
- [ ] No quedan preguntas bloqueantes.
- [ ] Las ideas descartadas conservan motivo y evidencia.
- [ ] No se ha iniciado implementación funcional dentro de esta spec.
