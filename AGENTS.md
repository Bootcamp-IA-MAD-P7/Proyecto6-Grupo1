# Instrucciones para agentes de IA

## Estado confirmado del proyecto

- Fase: nivel esencial verificado con baseline evaluado, servicio local e integración local de ClaimVox; OpenSpec + Harness Engineering operativos.
- Problema: clasificación y apoyo al enrutamiento de reclamaciones financieras escritas.
- Dataset: Consumer Complaint Database del CFPB, viable con condiciones.
- Entrada candidata permitida: `complaint_what_happened`.
- Target derivado: `product_canonical`, con once clases en `config/cfpb_target_contract.json`.
- Frontend integrado: prototipo React PWA ClaimVox; una evolución nativa solo se evaluará si aparece evidencia que la justifique.
- Responsabilidades: Miguel coordina arquitectura; José, backend; Abel, frontend/UX; Víctor, datos y EDA. Josué está fuera del equipo.
- Jira: proyecto `PG`; `PG-1` agrupa el nivel esencial.
- Trabajo actual: `PG-2` a `PG-7` completan el nivel esencial con evidencia local; `PG-8` verifica la comparación ensemble `MED-01`. Los siguientes cambios deben gobernar los criterios medios, la selección posterior de modelo o capacidades operativas. Las tareas numeradas `001/T-004` a `T-006` y `003/T-006` permanecen como expedientes cerrados de compatibilidad.
- Existe un baseline reproducible, inferencia local y una PWA integrada localmente bajo configuración explícita. No existe todavía base de datos, despliegue, autenticación, persistencia ni capacidad MLOps.

La métrica inicial del baseline, la política de idioma, duplicados, partición y desbalanceo ya están versionadas para la preparación actual. El modelo evaluado sigue siendo local y revisable, no un Champion ni un servicio desplegado. Siguen abiertas la selección basada en resultados, los modelos posteriores, la cobertura multilingüe, la persistencia y el proveedor cloud. No deben cerrarse sin evidencia y una decisión versionada.

## Fuente de verdad para cambios

Todo cambio relevante nuevo se gobierna en `openspec/`:

```text
proposal -> specs -> design -> tasks -> apply -> verify -> archive -> PR
```

- `openspec/changes/<change>/` conserva la propuesta activa, los requisitos, el diseño y las tareas.
- `openspec/specs/` conserva las capacidades vigentes después de archivar un cambio.
- `openspec/config.yaml` aporta el contexto y las reglas obligatorias para los artefactos.
- `ai-specs/` contiene roles y procedimientos reutilizables; no contiene requisitos de producto.
- `.specify/intent.md` conserva la intención global.
- Las carpetas numeradas de `specs/` son expedientes de compatibilidad anteriores a OpenSpec. Solo pueden actualizarse para terminar o adaptar el trabajo ya asignado; no se crearán carpetas numeradas nuevas.
- Jira registra asignación y estado operativo. Nunca sustituye requisitos, diseño, decisiones ni evidencias versionadas.

## Antes de actuar

1. Leer `README.md`, este archivo, `CONTRIBUTING.md` y `.specify/intent.md`.
2. Ejecutar `npm ci` si todavía no están instaladas las herramientas locales.
3. Ejecutar `python scripts/harness.py doctor`.
4. Comprobar rama y estado de Git.
5. Identificar el cambio OpenSpec activo o, solo para trabajo heredado, la spec y tarea numeradas.
6. Identificar la historia Jira `PG-N` o la excepción permitida y comprobar que no contradice el repositorio.
7. Resumir alcance, archivos previstos, bloqueantes y comprobaciones antes de editar.
8. Limitar los cambios al alcance autorizado y revisar impacto en documentación, NotebookLM, UX, seguridad y CI/CD.

Si una IA no puede leer el repositorio, la persona responsable genera un paquete seguro con `scripts/harness.py`. No se seleccionan archivos manualmente ni se adjuntan datos brutos.

## Flujo obligatorio

Para un cambio nuevo:

```bash
npm exec -- openspec new change <nombre-en-kebab-case>
python scripts/harness.py start --role <rol> --change <nombre> --jira PG-N
```

Para una tarea heredada ya asignada:

```bash
python scripts/harness.py start \
  --role <rol> \
  --spec <id> \
  --task <T-NNN>
```

- No implementar preguntas bloqueantes.
- No ampliar silenciosamente el alcance.
- Si el código contradice un requisito, actualizar primero el cambio OpenSpec y registrar la decisión.
- Una tarea solo se completa con evidencia proporcional.
- No afirmar que una carpeta, contrato, mock o documento representa una capacidad implementada.
- No inventar contenido de dailies ni evidencias.
- No utilizar iconografía genérica de IA en documentación o producto.
- No debilitar quality gates, permisos o controles de seguridad.
- No incorporar narrativas CFPB reales a Git, informes, logs, capturas, prompts o servicios externos.
- No copiar requisitos completos a Jira ni tratar su estado como evidencia de implementación.
- No utilizar como features campos prohibidos por `config/cfpb_target_contract.json`.
- No presentar React PWA, backend, modelo, Docker, despliegue o MLOps como implementados sin código y evidencia.
- No marcar requisitos de `docs/project_management/delivery_levels.md` como verificados sin su evidencia mínima.
- No ejecutar commit, push, archive, Pull Request o merge sin revisión humana.

## Cierre de una intervención

Indicar:

- cambio OpenSpec o tarea heredada relacionada;
- archivos modificados;
- comprobaciones ejecutadas y resultados;
- decisiones tomadas;
- riesgos y trabajo pendiente.

Cuando cambien comportamiento, métricas, arquitectura, UX o estado de entrega, revisar únicamente los documentos que cambien de significado: `README.md`, el cambio OpenSpec, `CHANGELOG.md`, las fuentes de NotebookLM y las evidencias relevantes.
