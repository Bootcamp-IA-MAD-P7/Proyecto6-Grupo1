## ADDED Requirements

### Requirement: Evidencia de baseline comunicada con alcance estadístico correcto

Cuando un baseline multiclase fusionado aporte informes versionados de train,
validation y test protegido, la documentación de estado MUST separar el
control de sobreajuste, obtenido de la misma métrica entre train y validation,
de la evaluación final sobre test. La documentación MUST enlazar o nombrar el
informe, la configuración y la trazabilidad de PR, Jira y OpenSpec, y MUST NOT
atribuir causalidad a una diferencia puntual entre validation y test.

#### Scenario: Test protegido supera a validation

- **WHEN** el valor de una métrica en test protegido es superior al de validation
- **THEN** la documentación lo presenta como una observación de evaluación final
  y mantiene el gap train/validation como la única evidencia del control de
  sobreajuste

#### Scenario: Criterio individual respaldado por evidencia

- **WHEN** un criterio de entrega cuenta con el código, configuración, informe
  agregado y comprobación mínima exigidos
- **THEN** su estado puede cambiar a `Verificado` sin declarar completado el
  nivel de entrega ni criterios independientes
