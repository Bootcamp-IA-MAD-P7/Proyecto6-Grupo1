## ADDED Requirements

### Requirement: Evidencia final de diagnóstico del baseline

El baseline elegible SHALL poder generar desde train y validation completo una
matriz de confusión, importancia por coeficientes y análisis agregado de
errores, manteniendo el test protegido fuera del diagnóstico.

#### Scenario: Ejecución final sin test

- **WHEN** se ejecuta el comando de evaluación final con la configuración
  congelada
- **THEN** genera artefacto local, manifiesto, figuras y reportes agregados sin
  cargar la partición test
