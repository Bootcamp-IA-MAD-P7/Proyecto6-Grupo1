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
- Responsable: `Miguel / Arquitectura de datos, entrega a Víctor`
- Dependencias: `T-001, T-002`
- Requisitos cubiertos: `R-006, R-007, AC-006`
- Trabajo: usar esta spec como referencia y devolver únicamente evidencias agregadas.
- Verificación: checklist de población, clases, tiempo, ausencias, duplicados, conflictos, longitud e idioma.
- Evidencia obtenida: contrato de entrega definido y entregado; Víctor asume el análisis del CSV bajo este contrato.

## T-004 Incorporar evidencia del EDA

- Estado: `[~]`
- Responsable: `Víctor / Datos y EDA del CSV`
- Dependencias: `T-003`
- Requisitos cubiertos: `R-006, R-007, R-009`
- Trabajo: contrastar soporte, drift, idioma, duplicados y alternativas de desbalanceo.
- Verificación: informe reproducible, revisión cruzada y ausencia de narrativas versionadas.
- Evidencia obtenida: análisis del CSV en curso; todavía no se ha incorporado al repositorio un informe agregado revisado.

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

## Checklist de cierre

- [ ] Todos los criterios de aceptación están cubiertos.
- [ ] Las pruebas acordadas pasan.
- [ ] El informe EDA cumple el contrato de entrega.
- [ ] Idioma, privacidad, duplicados y partición están decididos.
- [ ] La documentación coincide con el comportamiento real.
- [ ] No se han incorporado narrativas al repositorio.
