## 1. Preparar la ejecución de entrega

- [ ] 1.1 [Datos / ML] Extender el ejecutor aislado para distinguir explícitamente el perfil de entrega del piloto, exigir `train.parquet` completo, `narrative_hash`, cinco folds y la política vigente; rechazar cualquier reducción de presupuesto presentada como evidencia de `MED-02` o `MED-03`. Verificación: compilación y prueba sintética directa.
- [ ] 1.2 [Datos / ML] Extender la integración de tuning para registrar por trial y por fold macro F1 de train y validación, media, desviación, coste, configuración y limitaciones agregadas por clase, sin cargar `validation` reservada ni `test`. Verificación: prueba sintética directa de salida agregada.
- [ ] 1.3 [Datos / ML] Definir el manifiesto versionado de ejecución completa y su salida agregada, incluyendo huella de partición, versiones, presupuesto, estrategia de grupos, semillas y frontera de confirmación única sobre validation. No incluir datos, narrativas, binarios ni credenciales. Verificación: validación JSON y prueba directa.

## 2. Proteger el protocolo

- [ ] 2.1 [Tests / QA] Añadir pruebas sintéticas para rechazar corpus completo, validation, test, ausencia de `narrative_hash`, número de folds o presupuesto incompatibles, y uso del perfil piloto como cierre de entrega. Verificación: `python -m unittest tests.unit.test_model_selection -v` y los tests nuevos directamente afectados superados.
- [ ] 2.2 [Tests / QA] Añadir pruebas sintéticas de informe para comprobar macro F1 por fold, variabilidad, gap estricto menor que `0.05`, coste, métricas por clase, ausencia de Champion y prohibición de test para selección. Verificación: tests nuevos directamente afectados superados.

## 3. Ejecutar y revisar con autorización humana

- [ ] 3.1 [Miguel / coordinación] Registrar la aprobación humana explícita del presupuesto de cómputo, entorno y duración antes de ejecutar la totalidad de `train.parquet`; no iniciar una ejecución de entrega sin esa decisión.
- [ ] 3.2 [Datos / ML] Ejecutar el perfil completo aprobado sobre `train.parquet`, cinco folds y hasta 30 trials por candidato; generar únicamente informe y manifiesto agregados. Si la ejecución no finaliza o no alcanza el presupuesto, marcar evidencia incompleta y no actualizar `MED-02` ni `MED-03`.
- [ ] 3.3 [Miguel / Datos] Revisar humanamente la recomendación o ausencia de selección y, solo si procede, confirmar una única configuración contra validation sin retunar; no cargar test protegido ni declarar Champion.

## 4. Verificar y documentar

- [ ] 4.1 [Verificación] Ejecutar las pruebas directas, `git diff --check`, la validación estricta del cambio y las puertas de métricas afectadas; registrar resultados reales.
- [ ] 4.2 [Documentación] Actualizar únicamente la evidencia, `delivery_levels.md`, README, CHANGELOG y fuentes NotebookLM cuyo significado cambie. Marcar `MED-02` y `MED-03` como verificados solo con la evidencia completa y revisión humana; mantener límites, no Champion y no despliegue.
- [ ] 4.3 [Miguel / coordinación] Actualizar Jira `PG-11` con enlaces a evidencias reales, preparar PR hacia `dev` y no archivar sin revisión humana.
