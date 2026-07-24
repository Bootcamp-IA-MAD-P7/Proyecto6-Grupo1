# Tareas: Contrato de target CFPB

- Spec: [`spec.md`](spec.md)
- Plan: [`plan.md`](plan.md)

## T-001 Versionar la taxonomía y sus excepciones

- Estado: `[x]`
- Responsable: `Datos / ML`
- Requisitos cubiertos: `R-001, R-002, R-008, AC-001, AC-004`
- Trabajo: declarar once clases, dos aliases y una exclusión ambigua.
- Verificación: tests de cardinalidad, destinos y cobertura de etiquetas observadas.
- Evidencia obtenida: `config/cfpb_target_contract.json` y `tests/unit/test_cfpb_target_contract.py`.

## T-002 Fijar límites de features, privacidad y duplicados

- Estado: `[x]`
- Responsable: `Datos / seguridad`
- Dependencias: `T-001`
- Requisitos cubiertos: `R-003, R-004, R-005, AC-002, AC-003, AC-005`
- Trabajo: declarar entrada única, campos prohibidos, persistencia y agrupación anti-leakage.
- Verificación: revisión del contrato y tests de separación feature/target.
- Evidencia obtenida: spec, plan y contrato versionado.

## T-003 Entregar el contrato al EDA paralelo

- Estado: `[x]`
- Responsable: `Equipo EDA`
- Dependencias: `T-001, T-002`
- Requisitos cubiertos: `R-006, R-007, AC-006`
- Trabajo: usar esta spec como referencia y devolver únicamente evidencias agregadas.
- Verificación: checklist de población, clases, tiempo, ausencias, duplicados, conflictos, longitud e idioma.
- Evidencia obtenida: contrato de entrega definido; ejecución del EDA fuera de esta rama.

## T-004 Incorporar evidencia del EDA

- Estado: `[~]`
- Responsable: `Víctor / Datos y EDA`
- Dependencias: `T-003`
- Requisitos cubiertos: `R-006, R-007, R-009`
- Trabajo: contrastar soporte, drift, idioma, duplicados y alternativas de desbalanceo.
- Verificación: informe reproducible, revisión cruzada y ausencia de narrativas versionadas.
- Evidencia obtenida: trabajo activo fuera de esta rama; pendiente de incorporar informe, gráficos y revisión.

## T-005 Implementar el constructor reproducible

- Estado: `[ ]`
- Responsable: `Datos / ML`
- Dependencias: `T-004`
- Requisitos cubiertos: `R-001 a R-008`
- Trabajo: aplicar filtros, mapping, exclusiones, huellas y salida agregada usando el contrato.
- Verificación: tests unitarios y de integración sobre una muestra local.
- Evidencia obtenida: pendiente.

## T-006 Cerrar idioma, privacidad y partición

- Estado: `[ ]`
- Responsable: `Equipo`
- Dependencias: `T-004, T-005`
- Requisitos cubiertos: `R-004, R-005, R-009`
- Trabajo: resolver Q-001 a Q-004 y actualizar decisiones antes de entrenar.
- Verificación: revisión del equipo, tests y documentación sincronizada.
- Evidencia obtenida: pendiente.

## T-007 Adoptar el flujo reproducible de notebooks

- Estado: `[x]`
- Responsable: `Víctor / Datos y EDA`
- Dependencias: ninguna (relacionada con T-004, no bloqueante)
- Requisitos cubiertos: `ADR-003`
- Trabajo: implementar ADR-003: crear `.jupytext.toml`, actualizar `.gitignore` con `*.ipynb`, crear `Makefile` opcional, actualizar `notebooks/README.md`.
- Límites: no modificar el EDA (T-004), no entrenar modelos, no crear spec de modelado, no marcar T-004 como completada.
- Verificación: `git diff --check`, `python scripts/quality/check_repository.py`, sincronización de prueba entre `.py` y `.ipynb`, ausencia de narrativas versionadas.
- Evidencia obtenida: `.jupytext.toml`, `.gitignore` actualizado, `Makefile`, `notebooks/README.md` actualizado, `pyproject.toml` con uv y dependencias, sincronización jupytext verificada.

## Checklist de cierre

- [ ] Todos los criterios de aceptación están cubiertos.
- [ ] Las pruebas acordadas pasan.
- [ ] El informe EDA cumple el contrato de entrega.
- [ ] Idioma, privacidad, duplicados y partición están decididos.
- [ ] La documentación coincide con el comportamiento real.
- [ ] No se han incorporado narrativas al repositorio.
