## 1. Inventario y fuente canónica

- [x] 1.1 [Arquitectura / documentación] Confirmar el recuento canónico en `docs/project_management/delivery_levels.md` y contrastarlo con el SVG actual. Evidencia: 11 verificados, 2 en curso y 12 no iniciados; `MED-01` verificado, `MED-03` en curso y `ADV-05` en curso.
- [x] 1.2 [Documentación] Localizar todas las referencias activas al nombre antiguo del gráfico y distinguirlas de los expedientes históricos que no deben editarse. Evidencia: README, catálogo NotebookLM y guion de presentación eran referencias activas; los cambios archivados, expedientes numerados, dailies e informes no se editan.

## 2. Recurso y documentación activa

- [x] 2.1 [Documentación] Mover el gráfico a una ruta fechada con el corte real, conservando título, descripción accesible y los recuentos canónicos. Evidencia: se conserva solo `docs/assets/charts/delivery-status-2026-07-28.svg`; se retiran los recursos fechados 23 y 27 de julio que podían generar ambigüedad. El gráfico muestra `ADV-05` como el segundo criterio en curso.
- [x] 2.2 [Documentación] Actualizar `README.md`, `docs/assets/README.md`, `docs/notebooklm/source_catalog.md` y el guion de presentación solo si enlazan el recurso activo anterior. Evidencia: las cuatro fuentes apuntan a `delivery-status-2026-07-28.svg`.
- [x] 2.3 [Documentación] Añadir una nota breve en una fuente activa que identifique `delivery_levels.md` como estado vigente y preserve los archivos históricos como trazabilidad, sin crear un duplicado de estado. Evidencia: nota en README y regla editorial en el catálogo NotebookLM.
- [x] 2.4 [OpenSpec] Actualizar el delta de `project-state-documentation` con las reglas de fuente canónica y conservación histórica. Evidencia: `specs/project-state-documentation/spec.md` de este cambio.

## 3. Verificación y cierre

- [x] 3.1 [QA] Comprobar que no quedan referencias activas al nombre antiguo, que el SVG y `delivery_levels.md` tienen el mismo recuento y distribución por nivel, y que las rutas Markdown modificadas son válidas. Evidencia: búsqueda sin referencias activas a los recursos de 23 y 27 de julio; SVG de 28 de julio y tabla canónica reflejan 11 verificados, 2 en curso (`MED-03` y `ADV-05`) y 12 no iniciados; Avanzado muestra explícitamente 1 en curso y 5 no iniciados.
- [x] 3.2 [QA] Ejecutar `git diff --check`, `python scripts/quality/check_repository.py`, `npm exec -- openspec validate --all --strict` y `python scripts/documentation/build_notebooklm_pack.py --date 2026-07-28`. Evidencia: las cuatro comprobaciones superadas el 28 de julio de 2026; el paquete NotebookLM se regeneró localmente.
- [ ] 3.3 [Coordinación] Actualizar tareas y evidencia, preparar la Pull Request documental hacia `dev` y mantener el cambio activo hasta revisión humana y archivo posterior.
