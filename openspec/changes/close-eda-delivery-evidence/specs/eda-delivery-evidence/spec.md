## ADDED Requirements

### Requirement: EDA multiclase comunicada con visualizaciones pertinentes

El repositorio MUST mantener un informe EDA reproducible para la instantánea
analizada que cubra distribución y soporte de clases, tiempo, nulos,
duplicados, longitud, idioma y desbalanceo. Cuando la entrada sea texto libre y
el target sea categórico, el informe MUST justificar explícitamente por qué una
matriz de correlación numérica convencional no es pertinente y MUST identificar
las visualizaciones alternativas utilizadas.

#### Scenario: Entrada textual sin correlación numérica pertinente

- **WHEN** el EDA evalúa un clasificador cuya entrada permitida es una narrativa
  textual y cuyo target es una clase categórica
- **THEN** el informe documenta la no aplicabilidad de la correlación numérica y
  enlaza visualizaciones agregadas de clasificación pertinentes

### Requirement: Conclusiones EDA trazadas a decisiones posteriores

El informe EDA MUST enlazar las decisiones aprobadas de idioma, duplicados,
partición y tratamiento inicial del desbalanceo sin sustituir las cifras de su
propia instantánea por las de una fuente posterior. El repositorio MUST
mantener la referencia al contrato, script, figuras e informes agregados que
permiten revisar esas conclusiones.

#### Scenario: Fuente posterior con recuentos diferentes

- **WHEN** la preparación de entrenamiento usa una instantánea distinta de la
  analizada por el EDA
- **THEN** la documentación conserva ambos contextos separados y describe las
  decisiones posteriores como continuidad, no como cifras del EDA

### Requirement: Cierre verificable de ESS-02

El estado de `ESS-02` MUST cambiar a `Verificado` únicamente cuando exista
evidencia versionada del informe reproducible, sus visualizaciones agregadas,
conclusiones, límites y trazabilidad a las decisiones de datos. El cierre MUST
NOT afirmar que existe un modelo integrado, inferencia real ni resultados de
criterios independientes.

#### Scenario: Evidencia EDA completa

- **WHEN** la revisión confirma el script, informe, figuras, conclusiones y
  trazabilidad requeridos sin narrativas reales
- **THEN** los documentos de estado pueden declarar `ESS-02` como verificado y
  mantienen los demás criterios en su estado real
