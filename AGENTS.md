# Instrucciones para agentes de IA

## Estado del proyecto

El proyecto está en descubrimiento. No se debe inventar una idea de negocio, dataset, target, clases, métrica principal, modelo, framework de aplicación o proveedor cloud.

## Antes de actuar

1. Leer `README.md`, `.specify/README.md` y `CONTRIBUTING.md`.
2. Comprobar la rama y el estado de Git.
3. Identificar la spec y las tareas activas.
4. Distinguir entre contexto aportado y autorización para modificar archivos.
5. Limitar los cambios al alcance solicitado.
6. Revisar el impacto en documentación, fuentes de NotebookLM, UX, seguridad y CI/CD.

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
