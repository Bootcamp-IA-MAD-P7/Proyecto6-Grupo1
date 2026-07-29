## 1. Definir contratos de puertas de calidad

- [ ] 1.1 [Quality Engineer] Inventariar los contratos existentes de datos, modelo y métricas que consumirá cada puerta, sin duplicar clases ni umbrales. Evidencia: decisión breve en `design.md` o configuración versionada que referencia los contratos canónicos.
- [ ] 1.2 [Quality Engineer] Versionar la configuración mínima de quality gates con rutas y umbrales aprobados, sin cambiar métricas, particiones ni políticas de entrenamiento. Verificación: `python -m json.tool <configuración> > /dev/null`.

## 2. Implementar puerta de integridad de datos

- [ ] 2.1 [Quality Engineer] Implementar la validación local de esquema, clases, nulos críticos, duplicados conflictivos y separación de `narrative_hash` entre particiones mediante entradas explícitas y sin emitir textos de reclamaciones. Verificación: prueba unitaria sintética de caso conforme y caso de fuga.
- [ ] 2.2 [Tests / QA] Añadir fixtures y pruebas sintéticas que demuestren el rechazo de columna no autorizada, clase fuera del contrato, nulo crítico, duplicado conflictivo y fuga entre particiones. Verificación: `python -m unittest <módulo-de-tests-de-quality-gates> -v`.

## 3. Implementar puerta del contrato de modelo

- [ ] 3.1 [Quality Engineer] Implementar la validación de carga desde ubicación controlada, contrato de feature, forma de probabilidades, etiquetas canónicas e inferencia segura usando un artefacto sintético local temporal. Verificación: prueba unitaria sin entrenar ni persistir un modelo real.
- [ ] 3.2 [Tests / QA] Añadir pruebas directas para artefacto no compatible, clase no autorizada, forma de salida inválida y entrada prohibida. Verificación: `python -m unittest <módulo-de-tests-de-quality-gates> -v`.

## 4. Implementar puerta de métricas mínimas

- [ ] 4.1 [Quality Engineer] Implementar la validación de reportes agregados contra campos y umbrales versionados para métricas por clase, agregados y gap train-validación, sin recalcular ni seleccionar modelos. Verificación: prueba sintética de reporte conforme y de gap igual o superior a 0.05.
- [ ] 4.2 [Tests / QA] Añadir pruebas para evidencia incompleta, clase sin métricas obligatorias, uso prohibido del test protegido y salida privada sin narrativas. Verificación: `python -m unittest <módulo-de-tests-de-quality-gates> -v`.

## 5. Verificar y cerrar

- [ ] 5.1 [Quality Engineer] Ejecutar únicamente las pruebas unitarias afectadas, la validación estricta del cambio y `git diff --check`; registrar los resultados reales. Verificación: comandos específicos superados sin entrenar modelos completos.
- [ ] 5.2 [Documentation] Generar evidencia agregada de las puertas y actualizar solo `docs/project_management/delivery_levels.md`, README, CHANGELOG y fuentes NotebookLM si los criterios `ADV-04`, `ADV-05` o `ADV-06` quedan realmente verificados.
- [ ] 5.3 [Miguel / coordinación] Preparar la Pull Request hacia `dev` con alcance, evidencia, límites y reversión; no fusionar ni archivar sin revisión humana.
