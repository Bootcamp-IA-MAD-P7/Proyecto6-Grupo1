## 1. Definir el protocolo lineal

- [ ] 1.1 [Datos / ML] Versionar el perfil de dos fases: muestra agrupada determinista de hasta 50.000 filas, tres folds y 30 trials para búsqueda lineal; CV completa de cinco folds con parámetros congelados. Evidencia: configuración JSON válida y prueba sintética.
- [ ] 1.2 [Datos / ML] Adaptar el ejecutor aislado para aceptar solo LogisticRegression, `train.parquet` y `narrative_hash`; rechazar validation, test, XGBoost/RF y retuning en la fase completa. Evidencia: pruebas directas superadas.

## 2. Generar evidencia privada

- [ ] 2.1 [Datos / ML] Implementar salida agregada de búsqueda con semillas, presupuesto, parámetros, coste y limitaciones por clase, sin narrativas ni datos brutos. Evidencia: esquema y fixture sintético válidos.
- [ ] 2.2 [Datos / ML] Implementar salida de CV completa con macro F1 train/fold, desviación, gap estricto, coste y métricas de las once clases. Evidencia: pruebas directas y quality gate afectados superados.
- [ ] 2.3 [Tests / QA] Añadir pruebas sintéticas de aislamiento, grupos, parámetros congelados, once clases, gap, ausencia de Champion y prohibición de test. Evidencia: comando unitario focalizado superado.

## 3. Ejecutar con revisión humana

- [ ] 3.1 [Miguel / coordinación] Registrar la aprobación humana de entorno y presupuesto antes de fase A; no ejecutar si la aprobación falta.
- [ ] 3.2 [Datos / ML] Ejecutar fase A en entorno aprobado, versionar solo evidencia agregada y congelar parámetros si la salida es válida.
- [ ] 3.3 [Datos / ML] Ejecutar fase B sobre todo `train.parquet` con los parámetros congelados, sin retuning; generar evidencia agregada o registrar ejecución incompleta.
- [ ] 3.4 [Miguel / Datos] Revisar resultados y, solo si cumplen, permitir una única confirmación contra validation sin retuning ni test; no declarar Champion.

## 4. Cerrar con evidencia real

- [ ] 4.1 [Verificación] Ejecutar pruebas directas, quality gates afectados, `git diff --check` y validación estricta del cambio.
- [ ] 4.2 [Documentación] Actualizar evidencia y documentos canónicos solo si MED-02/MED-03 quedan realmente satisfechos; conservar límites y estado no Champion.
- [ ] 4.3 [Miguel / coordinación] Actualizar Jira PG-11, preparar PR hacia `dev` y no archivar sin revisión humana.
