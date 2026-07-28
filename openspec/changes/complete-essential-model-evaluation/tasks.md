## 1. Confirmación del candidato y preparación segura

- [x] 1.1 [Datos / ML] Inventariar las evidencias de baseline y ensemble; registrar que LogisticRegression es el único candidato completo elegible y que los ensembles de 50K no se usan para selección. Evidencia: `reports/validation/cfpb_essential_evaluation.md`.
- [x] 1.2 [Datos / ML] Confirmar que las particiones locales, el contrato de once clases y la configuración congelada existen antes de ejecutar; verificar que los artefactos y datos permanecen ignorados por Git. Verificación: manifiesto local y `git check-ignore` confirman la exclusión del artefacto.
- [x] 1.3 [Datos / ML] Añadir tests sintéticos para la generación de diagnósticos, el manifiesto local y la ausencia de la partición test en el flujo de diagnóstico. Evidencia: `tests/unit/test_essential_model_evaluation.py`.

## 2. Evaluación esencial y diagnósticos

- [x] 2.1 [Datos / ML] Implementar un comando reproducible que entrene el baseline congelado con train y evalúe únicamente validation completo, guardando el artefacto local y un manifiesto agregado seguro. Evidencia: `scripts/ml/train_essential_baseline.py`.
- [x] 2.2 [Datos / ML] Generar matriz de confusión y métricas por clase sobre validation completo; versionar figuras y reportes agregados sin narrativas ni resultados por fila. Evidencia: `cfpb_essential_evaluation.json` y figura de matriz.
- [x] 2.3 [Datos / ML] Generar importancia por coeficientes TF-IDF del modelo lineal, explicando su interpretación y limitaciones. Evidencia: figura de coeficiente absoluto medio e informe.
- [x] 2.4 [Datos / ML / producto] Generar análisis agregado de errores: clases débiles, confusiones frecuentes, soporte y acciones de mitigación compatibles con revisión humana. Evidencia: informe esencial sin narrativas.
- [x] 2.5 [Datos / ML] Ejecutar una única evaluación final controlada sobre los datos locales aprobados y registrar tiempos, configuración, hash de artefacto y resultados reales; no usar test para ajuste ni diagnóstico. Evidencia: 628,0 s; gap 0,0078; manifiesto y reporte agregados.

## 3. Integración y documentación de entrega

- [x] 3.1 [Backend / frontend] Confirmar mediante tests de contrato que el artefacto elegido conserva las once clases y la forma de respuesta compatible con el servicio local y ClaimVox; no cambiar el comportamiento de revisión humana. Evidencia: `tests.contract.test_inference_contract` superado.
- [x] 3.2 [Documentación] Crear el informe técnico y guía de ejecución que conecten preparación, baseline elegido, métricas, diagnósticos, backend local, ClaimVox y límites operativos. Evidencia: `cfpb_essential_evaluation.md` y `essential_delivery_guide.md`.
- [x] 3.3 [Documentación] Actualizar `README.md`, niveles de entrega, changelog, daily, fuentes NotebookLM y estado técnico únicamente con evidencias verificadas; no marcar criterios que fallen o carezcan de evidencia.

## 4. Verificación y cierre

- [x] 4.1 [QA] Ejecutar tests unitarios relevantes, comprobaciones del repositorio, validación OpenSpec estricta y comprobaciones de privacidad. Verificación: 19 tests unitarios/contrato, quality gate, diff y validación estricta superados el 28 de julio de 2026.
- [x] 4.2 [Coordinación] Revisar humanamente figuras, informe y límites; actualizar PG-7 solo tras enlazar evidencias reales. Evidencia: revisión humana confirmada el 28 de julio de 2026; PG-7 queda preparada para cierre con la futura PR.
- [ ] 4.3 [Coordinación] Preparar la Pull Request hacia `dev` con resultados, riesgos, reversión y criterios ESS realmente cerrados; no fusionar ni archivar sin revisión humana.
