# CFPB training dataset

## Purpose

Construir y validar localmente un corpus CFPB de entrenamiento trazable al contrato de target, manteniendo las narrativas fuera de Git y compartiendo únicamente evidencia agregada.

## Requirements

### Requirement: Constructor local gobernado por contrato

El sistema MUST construir el corpus local elegible únicamente a partir de una fuente CFPB disponible localmente y de `config/cfpb_target_contract.json`. El constructor MUST aplicar la ventana temporal, los campos obligatorios, la normalización de etiquetas, las exclusiones y la política de etiquetas desconocidas definidas por ese contrato, sin duplicar ni reinterpretar sus reglas.

#### Scenario: Construcción con registros contemplados por el contrato

- **WHEN** se ejecuta el constructor sobre una fuente local cuyos registros cumplen el contrato vigente
- **THEN** genera un corpus local con `complaint_what_happened`, `product_canonical` y la información técnica mínima autorizada para la preparación posterior
- **AND** el target contiene únicamente las etiquetas canónicas definidas en el contrato

#### Scenario: Etiqueta de origen no contemplada

- **WHEN** el constructor encuentra una etiqueta de origen no contemplada por el contrato
- **THEN** falla explícitamente sin asignar una clase alternativa automática
- **AND** registra una evidencia agregada que permita investigar el fallo sin publicar narrativas

### Requirement: Exclusiones y recuentos agregados verificables

El sistema MUST excluir y cuantificar los registros que el contrato declara no elegibles, incluida la etiqueta histórica ambigua. El sistema MUST producir recuentos agregados que diferencien la población de entrada, la población elegible, las exclusiones y el corpus resultante.

#### Scenario: Etiqueta histórica ambigua

- **WHEN** el constructor encuentra registros con una etiqueta histórica excluida por el contrato
- **THEN** no los incorpora al corpus de entrenamiento local
- **AND** comunica su número agregado como exclusión trazable

### Requirement: Huellas de narrativa y conflictos de target

El sistema MUST calcular localmente la clave de grupo de narrativa definida por el contrato. Los grupos con targets contradictorios MUST excluirse del corpus de entrenamiento y cuantificarse en la evidencia agregada. El constructor MUST mantener abierta la decisión sobre conservación o ponderación dentro de grupos no conflictivos.

#### Scenario: Grupo duplicado con targets contradictorios

- **WHEN** varias narrativas normalizadas comparten huella y tienen targets canónicos distintos
- **THEN** el constructor excluye todo el grupo del corpus local de entrenamiento
- **AND** registra únicamente el número agregado de grupos y filas excluidos

#### Scenario: Grupo duplicado no conflictivo

- **WHEN** varias narrativas normalizadas comparten huella y tienen el mismo target canónico
- **THEN** el constructor preserva la información de agrupación necesaria para evitar leakage posterior
- **AND** no decide todavía si el grupo se colapsa o se pondera

### Requirement: Privacidad de artefactos y evidencias

El sistema MUST mantener las narrativas y los artefactos de datos resultantes fuera de Git. Los informes, logs, capturas, pruebas versionadas y evidencias MUST contener exclusivamente datos sintéticos, configuraciones o métricas agregadas.

#### Scenario: Generación de evidencia del constructor

- **WHEN** termina una ejecución del constructor
- **THEN** los artefactos con narrativas permanecen en rutas locales ignoradas por Git
- **AND** la evidencia versionable no incluye narrativas, fragmentos de texto ni identificadores de reclamaciones

### Requirement: Repetibilidad y límites previos al entrenamiento

El sistema MUST permitir repetir la construcción sobre la misma fuente local y el mismo contrato obteniendo los mismos recuentos de control. Esta capacidad MUST NOT entrenar modelos, crear particiones definitivas, aplicar una política final de idioma o desbalanceo, ni verificar criterios de entrega que requieran evaluación de modelos.

#### Scenario: Repetición con la misma fuente y contrato

- **WHEN** el constructor se ejecuta dos veces sobre la misma fuente local y el mismo contrato versionado
- **THEN** las ejecuciones producen los mismos recuentos agregados de control y las mismas etiquetas canónicas
- **AND** cualquier discrepancia provoca un fallo explícito para su investigación

#### Scenario: Intento de ampliar el alcance a entrenamiento

- **WHEN** una tarea de esta capacidad intenta entrenar, evaluar o promocionar un modelo
- **THEN** se considera fuera de alcance y requiere un cambio OpenSpec posterior
