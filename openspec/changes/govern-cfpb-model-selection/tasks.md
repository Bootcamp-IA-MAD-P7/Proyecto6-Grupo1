## 1. Preparar el protocolo

- [ ] 1.1 [Datos / ML] Confirmar que los datos usados para CV pertenecen solo al conjunto de entrenamiento permitido y que se conserva la prevención de leakage vigente.
- [ ] 1.2 [Datos / ML] Definir y versionar la estrategia estratificada compatible, número de folds, semillas y presupuesto de ejecución antes de ejecutar candidatos.
- [ ] 1.3 [Datos / ML] Definir el formato agregado de resultados: macro F1 por fold, media, variabilidad, gap train-validación, coste y limitaciones por clase.

## 2. Implementar evaluación gobernada

- [ ] 2.1 [Datos / ML] Adaptar la evaluación de candidatos para ejecutar CV únicamente en datos de entrenamiento, sin consultar validación reservada ni test protegido durante la selección.
- [ ] 2.2 [Datos / ML] Integrar la búsqueda de hiperparámetros acotada con macro F1 como métrica primaria y registro de configuración, semillas y presupuesto.
- [ ] 2.3 [Datos / ML] Implementar la regla de recomendación: gap inferior a `0.05`; en empate, menor variabilidad y coste; si no se cumple, registrar «sin selección aprobada».

## 3. Verificar y evidenciar

- [ ] 3.1 [Tests / QA] Añadir o ajustar pruebas directas para impedir el uso del test protegido, comprobar semillas, estrategia de folds y la salida agregada.
- [ ] 3.2 [Datos / ML] Ejecutar la evaluación aprobada y generar informes agregados sin narrativas CFPB, datos brutos, binarios, credenciales ni logs sensibles.
- [ ] 3.3 [Miguel / coordinación] Revisar humanamente la recomendación o la ausencia de selección, enlazar evidencias con `PG-11` y actualizar criterios `MED-02` y `MED-03` solo si su evidencia mínima queda satisfecha.

## 4. Cierre

- [ ] 4.1 [Verificación] Ejecutar las pruebas unitarias directamente afectadas, `git diff --check` y la validación estricta del cambio antes de preparar la Pull Request.
- [ ] 4.2 [Documentación] Actualizar únicamente la documentación cuyo significado cambie con resultados reales, límites y decisión; no presentar ningún candidato como Champion o desplegado sin aprobación y evidencia posterior.
