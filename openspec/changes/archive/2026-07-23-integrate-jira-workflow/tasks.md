## 1. Gobierno y backlog

- [x] 1.1 Miguel / arquitectura: verificar sitio, proyecto, tipos de incidencia y backlog vacío. Evidencia: sitio `miguel-redondo.atlassian.net`, proyecto `PG`, cero incidencias.
- [x] 1.2 Equipo / producto: aprobar el Epic inicial y el desglose de seis tickets antes de escribir en Jira. Evidencia: confirmación humana previa a la creación.
- [x] 1.3 Miguel / coordinación: crear primero el Epic y después sus tickets hijos, sin asignar cuentas no confirmadas. Evidencia: `PG-1` y `PG-2` a `PG-7`.
- [x] 1.4 Miguel / arquitectura: registrar claves, enlaces y relaciones en el cambio OpenSpec y documentación viva. Evidencia: jerarquía `PG-1` → `PG-2..PG-7` y ocho relaciones `Blocks` verificadas en la dirección prevista.

## 2. Integración del arnés

- [x] 2.1 Miguel / arquitectura: añadir `--jira PG-N` y una excepción explícita controlada al modo OpenSpec de `scripts/harness.py`. Evidencia: CLI y validadores locales.
- [x] 2.2 Miguel / QA: probar claves válidas, formatos inválidos, ausencia sin excepción, tareas heredadas y paquetes sin credenciales. Evidencia: `tests/unit/test_harness.py`.
- [x] 2.3 Miguel / arquitectura: incluir la referencia Jira en los paquetes `start`, `verify` y `prepare-pr`. Evidencia: generador común y paquetes de prueba para `PG-2` y bootstrap.

## 3. GitHub y autoservicio

- [x] 3.1 Miguel / proceso: añadir el campo Jira o excepción a la plantilla de Pull Request.
- [x] 3.2 Miguel / documentación: documentar ramas `tipo/PG-N-descripcion`, límites y flujo diario en lenguaje corriente. Evidencia: `docs/project_management/jira_workflow.md`.
- [x] 3.3 Miguel / QA: ampliar el quality gate sin bloquear Dependabot ni el cambio de bootstrap. Evidencia: se validan propuestas activas y plantilla; las ramas administradas quedan exceptuadas.

## 4. Verificación y cierre

- [x] 4.1 Miguel / QA: ejecutar OpenSpec estricto, tests unitarios y de contrato, quality check, compilación y whitespace. Evidencia: 3 validaciones OpenSpec, 48 tests unitarios, 7 de contrato, 0 vulnerabilidades y checks locales correctos.
- [x] 4.2 Equipo: pilotar una historia real desde Jira hasta una Pull Request o registrar el alcance exacto del piloto pendiente. Evidencia: piloto delimitado a `PG-2` / `001/T-004`; ejecución y feedback de Víctor pendientes.
- [x] 4.3 Miguel / arquitectura: actualizar daily, changelog, NotebookLM y evidencia sin presentar Jira como trabajo de producto terminado.
- [x] 4.4 Miguel / arquitectura: obtener revisión humana antes de archivo, commit, publicación o merge. Evidencia: revisión y aprobación explícita de Miguel antes del archivo.
