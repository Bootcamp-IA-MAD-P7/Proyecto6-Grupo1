# Instrucciones para agentes de IA

## Estado confirmado del proyecto

- Fase: descubrimiento, EDA y adopción del arnés agéntico.
- Problema: clasificación y apoyo al enrutamiento de reclamaciones financieras escritas.
- Dataset: Consumer Complaint Database del CFPB, viable con condiciones.
- Entrada inicial permitida: `complaint_what_happened`.
- Target derivado: `product_canonical`, con once clases definidas en `config/cfpb_target_contract.json`.
- Frontend: React con capacidades PWA como dirección inicial; una evolución nativa solo se evaluará si aparecen requisitos que la justifiquen.
- Specs activas: `000-problem-discovery`, `001-cfpb-target-contract`, `003-complaint-routing-experience`, `004-agentic-harness` y la spec asignada a la tarea actual.
- Responsabilidades: Miguel coordina arquitectura y arnés; José, backend; Abel, frontend/UX; Víctor, datos y EDA. Josué está fuera del equipo.
- Asignación de producto activa desde `dev`: `001/T-004` para Víctor.
- La PWA experimental permanece fuera de `dev`; no debe tratarse como aplicación implementada ni como tarea activa desde esta rama.
- La integración real `003/T-007` continúa bloqueada hasta disponer de EDA, modelo aprobado y decisiones de datos.

Siguen abiertas la métrica principal, modelos, política de idioma, tratamiento final de duplicados, partición, estrategia de desbalanceo, backend, persistencia y proveedor cloud. No deben inventarse ni cerrarse sin evidencia y decisión registrada.

## Antes de actuar

1. Leer `README.md`, `.specify/README.md`, `.specify/intent.md`, `CONTRIBUTING.md` y `docs/project_management/delivery_levels.md`.
2. Comprobar la rama y el estado de Git.
3. Identificar la spec y las tareas activas.
4. Identificar la historia de Jira cuando exista y comprobar que no contradice la spec.
5. Distinguir entre contexto aportado y autorización para modificar archivos.
6. Resumir alcance, archivos previstos y bloqueantes antes de editar.
7. Limitar los cambios al alcance solicitado.
8. Revisar el impacto en documentación, fuentes de NotebookLM, UX, seguridad y CI/CD.

Cada integrante debe obtener el contexto desde su propio clon actualizado. Si la IA accede al repositorio, debe leer las fuentes versionadas directamente. Si no accede, la propia persona genera un paquete mediante `scripts/harness.py`; no se utiliza una selección manual de archivos ni se comparten datos brutos.

## Flujo obligatorio para cambios relevantes

```text
spec -> plan -> tasks -> implementation -> verification -> closure
```

- No implementar preguntas bloqueantes.
- No ampliar silenciosamente el alcance.
- Si el código necesita contradecir una spec, actualizar primero el contrato y registrar la decisión.
- Una tarea solo se completa cuando existe evidencia de verificación.
- No afirmar que una carpeta vacía representa una capacidad implementada.
- No inventar contenido para una daily; usar pendientes explícitos si el equipo no ha aportado información.
- No utilizar iconografía genérica de IA en documentación o producto.
- No debilitar quality gates, permisos o controles de seguridad para hacer pasar un cambio.
- No incorporar narrativas CFPB reales a Git, informes, logs, capturas, prompts o servicios externos.
- No utilizar como features campos prohibidos por `config/cfpb_target_contract.json`.
- No presentar React PWA, backend, modelo, Docker, despliegue o MLOps como implementados sin código y evidencia.
- No actualizar todos los documentos por rutina: revisar únicamente los que cambien de significado o estado.
- No interpretar un rol de área como autorización para saltarse dependencias, preguntas bloqueantes o criterios de aceptación.
- No marcar un requisito de `docs/project_management/delivery_levels.md` como verificado sin la evidencia mínima indicada.

## Responsabilidad humana

La IA puede proponer, implementar y verificar dentro del alcance autorizado. La persona responsable de la rama debe revisar el diff, proteger datos, confirmar las decisiones y firmar la Pull Request. Una conversación con una IA no sustituye Jira, una spec, una decisión versionada ni una revisión humana.

## Cierre de una intervención

Indicar:

- spec y tareas relacionadas;
- archivos modificados;
- comprobaciones ejecutadas y resultados;
- decisiones tomadas;
- riesgos o trabajo pendiente.

## Documentación viva

Cuando un cambio altere comportamiento, métricas, arquitectura, UX o estado de entrega, revisar:

- `README.md`;
- spec, tareas y decisiones;
- `CHANGELOG.md`;
- `docs/notebooklm/source_catalog.md` y las fuentes afectadas;
- diagramas, capturas e informes relevantes.
