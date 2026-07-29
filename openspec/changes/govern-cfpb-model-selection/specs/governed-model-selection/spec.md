## ADDED Requirements

### Requirement: Validación cruzada sin fuga de datos

El sistema MUST evaluar candidatos mediante validación cruzada estratificada
usando únicamente los datos de entrenamiento permitidos por la política vigente.
La implementación MUST conservar la prevención de leakage establecida para la
partición; si necesita agrupación, DEBE emplear una estrategia compatible y
documentarla antes de producir resultados.

#### Scenario: Evaluación de un candidato

- **WHEN** se ejecuta la evaluación de un candidato multiclase
- **THEN** los folds contienen solo datos permitidos de entrenamiento
- **AND** se registra la semilla, la estrategia de folds y resultados agregados
- **AND** el test protegido no se utiliza.

### Requirement: Ejecutor aislado de selección

El sistema MUST implementar la evaluación de PG-11 en un ejecutor independiente
que consuma solo la partición local `train.parquet` y conserve
`narrative_hash` para agrupar. El ejecutor MUST NOT reconstruir particiones desde
el corpus completo ni cargar validación reservada o test protegido.

#### Scenario: Inicio de una evaluación gobernada

- **WHEN** se inicia la evaluación de selección de modelo
- **THEN** el ejecutor recibe únicamente la partición de entrenamiento aprobada
- **AND** rechaza rutas de validación, test o corpus completo.

### Requirement: Optimización reproducible y acotada

El sistema MUST ejecutar la optimización de hiperparámetros únicamente dentro de
los folds de entrenamiento y MUST registrar configuración, presupuesto, semillas
y resultados por fold. La métrica primaria MUST ser macro F1.

#### Scenario: Búsqueda de hiperparámetros

- **WHEN** se comparan configuraciones de un candidato
- **THEN** la búsqueda no consulta validación reservada ni test protegido para
  elegir parámetros
- **AND** el informe permite reproducir el presupuesto y la configuración
  evaluada.

### Requirement: Decisión gobernada de candidato

El sistema MUST recomendar un candidato solo a partir de criterios definidos
antes de consultar el test protegido: macro F1, variabilidad entre folds, coste
de ejecución, limitaciones por clase y un gap train-validación inferior a `0.05`.
Si ningún candidato los satisface, MUST registrar que no existe selección
aprobada.

#### Scenario: Candidato no elegible

- **WHEN** todos los candidatos exceden el gap permitido o presentan evidencia
  insuficiente
- **THEN** el informe declara «sin selección aprobada»
- **AND** no presenta ningún modelo como Champion ni como desplegado.

### Requirement: Evidencia agregada y privada

El sistema MUST conservar solo evidencia agregada y reproducible en Git. El
sistema MUST NOT versionar narrativas CFPB, datos brutos, artefactos pesados,
credenciales ni logs sensibles.

#### Scenario: Publicación de resultados

- **WHEN** se versiona el resultado de una ejecución
- **THEN** incluye métricas agregadas, configuración y limitaciones
- **AND** no contiene contenido sensible ni datos de reclamaciones.

### Requirement: Piloto de viabilidad explícitamente limitado

El sistema MAY ejecutar un piloto determinista de 100.000 filas de
`train.parquet` con semilla `42`. Un informe de piloto MUST identificarse como
evidencia de viabilidad y MUST NOT verificar `MED-02`, `MED-03`, un Champion ni
una selección definitiva.

#### Scenario: Ejecución de piloto en Colab

- **WHEN** se solicita una ejecución limitada de selección
- **THEN** el ejecutor limita la entrada a 100.000 filas con la semilla aprobada
- **AND** la salida declara que el resultado no cierra criterios de entrega.
