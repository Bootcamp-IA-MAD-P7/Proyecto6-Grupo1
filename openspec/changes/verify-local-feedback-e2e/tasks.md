## 1. Preparar la comprobación local

- [x] 1.1 [Backend / QA] Confirmar contrato de predicción, política de feedback,
  artefacto local reproducible y raíz local controlada antes de ejecutar. Evidencia:
  `reports/validation/claimvox_local_feedback_e2e_preflight.md` inventaría el
  contrato, operaciones, política, raíz y comando de salud, sin afirmar que el
  artefacto o la API estén activos.
- [x] 1.2 [Backend / QA] Definir una única narrativa sintética y los metadatos
  cerrados de feedback derivados de la respuesta local. Evidencia: plan de
  prueba en `reports/validation/claimvox_local_feedback_e2e_preflight.md` que
  usa el ejemplo sintético existente y deriva solo metadatos permitidos, sin
  narrativas CFPB, identidad, texto libre ni UUID nuevos.

## 2. Verificar el recorrido extremo a extremo

- [x] 2.1 [Backend / QA] Iniciar la API local con el artefacto reproducible y
  comprobar salud y predicción real contractual. Evidencia: resultado agregado
  del 29 de julio de 2026 con salud `ok`, fuente Local API, clase `Credit card`,
  confianza `78%`, modelo `baseline-lr-C0.1-f8000` y taxonomía `1.0`, sin copiar
  la narrativa.
- [x] 2.2 [Backend / QA] Registrar feedback permitido posterior a esa predicción
  y consultar el resumen local. Evidencia: creación aceptada, resumen exclusivo
  por versión/clase/decisión, ausencia de registros individuales e independencia
  de la predicción; la ejecución local devolvió un único contador agregado para
  `baseline-lr-C0.1-f8000`, `Credit card` y `confirmed`.
- [x] 2.3 [Backend / QA] Comprobar el rechazo seguro de un campo no permitido y
  la indisponibilidad recuperable de la API de feedback. Evidencia: estados de
  error sin reflejar valores sensibles ni fabricar persistencia. `POST` con el
  nombre de campo prohibido devolvió `422 VALIDATION_ERROR` sin reflejar su
  valor; `npm exec -- vitest run src/components/PredictionResult.test.tsx`
  superado: 2 pruebas, incluida indisponibilidad segura.

## 3. Decidir y documentar

- [x] 3.1 [Miguel / coordinación] Crear evidencia agregada versionable del
  recorrido local y decidir si satisface `MED-04`; mantener `MED-05` en curso.
  Evidencia: `reports/validation/claimvox_local_feedback_e2e.md` registra salud,
  predicción local, feedback permitido, resumen agregado, rechazo seguro e
  indisponibilidad; Miguel aprobó verificar `MED-04` el 29 de julio de 2026.
- [x] 3.2 [Documentación] Actualizar `delivery_levels.md`, README, CHANGELOG y
  fuentes NotebookLM solo si el significado canónico cambia, preservando los
  límites de autenticación, almacenamiento compartido, despliegue, MLOps y
  reentrenamiento. Evidencia: `MED-04` pasa a verificado en los niveles de
  entrega y los documentos canónicos enlazan la evidencia extrema a extremo sin
  promocionar capacidades fuera de alcance.
- [x] 3.3 [Verificación] Ejecutar solo pruebas y comprobaciones afectadas,
  `git diff --check` y `npm exec -- openspec validate verify-local-feedback-e2e --type change --strict` antes de revisión humana. Evidencia: `python -m unittest tests.unit.test_feedback_operational_flow -v` superado (3 pruebas); `npm exec -- vitest run src/components/PredictionResult.test.tsx` superado (2 pruebas); validación OpenSpec y comprobación de diff superadas el 29 de julio de 2026.
