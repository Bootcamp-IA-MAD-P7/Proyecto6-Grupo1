## Contexto

La comparación `MED-01` confirma que existen alternativas al baseline, pero se
ejecutó sobre una muestra y no autoriza la selección de un modelo definitivo.
La política de preparación vigente ya fija las once clases, la métrica primaria
macro F1 y el control de sobreajuste. Este cambio gobierna la siguiente decisión
sin alterar esa política ni consultar el test protegido para elegir.

## Objetivos y no objetivos

**Objetivos:** definir una evaluación estratificada reproducible, una búsqueda
de hiperparámetros acotada y una regla explícita para recomendar —o rechazar— un
candidato.

**No objetivos:** cambiar la partición aprobada, entrenar un Champion,
desplegar, modificar ClaimVox o convertir resultados de muestra en evidencia
definitiva.

## Decisiones de diseño

### Datos y particiones

- La validación cruzada se ejecutará únicamente sobre los datos de entrenamiento
  permitidos por la política vigente.
- El conjunto de validación se reservará para confirmar el candidato elegido por
  validación cruzada; el test protegido no participa en ajuste, búsqueda ni
  selección.
- La estratificación debe mantener la representación de las once clases. Si la
  prevención vigente de leakage exige agrupar registros relacionados, se usará
  una variante estratificada compatible y se justificará en la evidencia antes
  de ejecutarla.

### Límite de implementación

- La evaluación de PG-11 se implementará en un ejecutor independiente. No se
  reutilizará `scripts/ml/train_ensemble.py`, porque ese script reconstruye un
  corte temporal desde el corpus de entrada y no consume las particiones
  aprobadas aisladas por `narrative_hash`.
- El ejecutor nuevo recibirá únicamente la partición local `train.parquet` y su
  columna de grupo. La validación reservada y el test protegido permanecerán
  fuera de su entrada y de su lógica de selección.

### Métricas y decisión

- Macro F1 es la métrica primaria de comparación.
- La evidencia registrará resultados por fold, media y variabilidad, además del
  gap train-validación con la misma métrica.
- Un candidato solo puede recomendarse si respeta el límite aprobado de gap
  inferior a `0.05`. En empates o resultados próximos, prevalecen menor
  variabilidad, menor coste de ejecución y una limitación de clases documentada.
- Si ningún candidato cumple estas condiciones, el resultado será «sin selección
  aprobada»; no se declarará Champion.

### Reproducibilidad y privacidad

- Cada ejecución registrará semillas, configuración, presupuesto de búsqueda,
  versión de datos permitida y resultados agregados.
- Optuna u otra búsqueda equivalente solo evaluará folds de entrenamiento.
- Git solo conservará configuración, código, pruebas e informes agregados. Los
  datos brutos, narrativas CFPB, artefactos pesados, credenciales y logs
  sensibles permanecerán fuera del repositorio.

### Piloto de viabilidad

- La primera ejecución en Colab se limitará a una muestra determinista de
  100.000 filas de `train.parquet`, con semilla `42`, para comprobar coste y
  comportamiento del protocolo.
- El piloto es evidencia de viabilidad exclusivamente: no puede verificar
  `MED-02` ni `MED-03`, seleccionar un Champion ni sustituir una ejecución sobre
  el alcance aprobado completo.

## Riesgos y mitigaciones

- Las clases minoritarias pueden provocar folds inestables; la variabilidad se
  tratará como criterio de decisión, no como detalle secundario.
- El presupuesto puede resultar insuficiente para comparar configuraciones; se
  declarará explícitamente la cobertura alcanzada en vez de extrapolar.
- Si estratificación y agrupación entran en conflicto, se detiene la selección
  hasta documentar una variante que preserve la prevención de leakage.
- El piloto puede no representar las clases minoritarias del alcance completo;
  sus resultados se etiquetarán como piloto y no como decisión definitiva.

## Trazabilidad

- Jira: `PG-11`.
- Criterios previstos: `MED-02` y `MED-03`.
- La ejecución posterior deberá enlazar informes agregados, pruebas directas y
  una decisión humana sobre la recomendación resultante.
