# essential-model-evaluation Specification

## Purpose

Gobernar la selección local reproducible del baseline esencial y sus diagnósticos agregados sin reutilizar el test protegido.

## Requirements

### Requirement: Selección esencial gobernada

El sistema SHALL seleccionar un candidato para la entrega esencial únicamente cuando exista evidencia reproducible sobre el split aprobado, sus predicciones pertenezcan a las once clases de `config/cfpb_target_contract.json` y el gap de macro F1 train-validation cumpla el umbral vigente. Una comparación realizada solo sobre una muestra SHALL NOT seleccionar el candidato esencial.

#### Scenario: Candidato completo elegible

- **WHEN** un candidato dispone de configuración congelada, artefacto local, predicciones válidas y gap dentro del umbral
- **THEN** el informe lo identificará como candidato esencial local y enlazará su evidencia sin declararlo desplegado ni automático

#### Scenario: Candidato exploratorio incompleto

- **WHEN** un modelo solo cuenta con resultados de muestra o no cumple el control de overfitting
- **THEN** el sistema lo conservará como comparación experimental y no lo usará para seleccionar el modelo esencial

### Requirement: Diagnósticos completos sin reutilizar el test

El sistema SHALL generar sobre validation completo una matriz de confusión, un resumen de errores por clase y figuras de importancia compatibles con el candidato seleccionado. El proceso SHALL NOT usar el test protegido para seleccionar, ajustar ni diagnosticar el modelo.

#### Scenario: Diagnósticos agregados de validation

- **WHEN** finaliza la evaluación del candidato esencial
- **THEN** el repositorio contendrá figuras y reportes agregados de matriz de confusión, soporte, métricas por clase, confusiones frecuentes e importancia de variables sin narrativas CFPB

#### Scenario: Test protegido preservado

- **WHEN** se produce la evidencia de diagnóstico
- **THEN** el comando recibirá únicamente train y validation, y el informe diferenciará las métricas test previamente registradas de los diagnósticos nuevos

### Requirement: Artefacto local reconstruible

El sistema SHALL guardar el candidato seleccionado como artefacto local ignorado por Git y SHALL versionar un manifiesto agregado con configuración, semilla, contrato de clases, versiones y hash del artefacto.

#### Scenario: Reconstrucción del artefacto

- **WHEN** una persona autorizada ejecuta el comando documentado con las particiones locales aprobadas
- **THEN** se genera el artefacto local y un manifiesto sin datos, narrativas ni predicciones individuales

### Requirement: Limitaciones y análisis de errores accionable

El informe SHALL identificar clases débiles, confusiones frecuentes y acciones de mitigación proporcionales, sin transformar esas asociaciones en decisiones automáticas ni recomendaciones financieras.

#### Scenario: Clase con rendimiento débil

- **WHEN** una clase quede por debajo del umbral documentado de F1
- **THEN** el informe mostrará su soporte y métricas agregadas, describirá el riesgo de revisión humana y propondrá una acción de datos o evaluación futura
