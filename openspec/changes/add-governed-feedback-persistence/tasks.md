# Tareas: persistencia gobernada de feedback

## 1. Fijar contratos y límites

- [x] 1.1 [Arquitectura / backend] Inventariar el contrato de predicción y los campos mínimos permitidos para feedback, sin duplicar narrativas ni crear un endpoint público. Evidencia: `reports/validation/feedback_persistence_contract_review.md` traza los campos mínimos a `PredictionResponse` y excluye narrativa, `client_request_id`, identidad y texto libre.
- [x] 1.2 [Arquitectura / seguridad] Versionar la política local de ubicación, retención, vocabularios de decisión/finalidad y campos prohibidos. Evidencia: `config/claimvox_feedback_persistence_policy.json`; `python -m json.tool config/claimvox_feedback_persistence_policy.json > /dev/null` superado, sin secretos ni datos reales.

## 2. Implementar el almacén local aislado

- [x] 2.1 [Backend] Crear el modelo de dominio y la validación de feedback mínimo, con clases canónicas, versiones, marcas temporales y rechazo seguro de campos prohibidos. Evidencia: `app/api/schemas/feedback.py`; `python -m py_compile app/api/schemas/feedback.py` superado. Las pruebas sintéticas directas corresponden a la tarea 2.3.
- [ ] 2.2 [Backend / plataforma] Implementar un repositorio local bajo raíz controlada con esquema versionado, migración idempotente y rechazo de rutas externas, sin red ni base compartida. Verificación: almacén temporal sintético.
- [ ] 2.3 [Tests / QA] Añadir pruebas sintéticas de registro conforme, clase inválida, campo sensible, fecha inválida, ruta externa e inicialización repetible. No usar narrativas CFPB ni identidad.

## 3. Aplicar retención y lectura mínima

- [ ] 3.1 [Backend] Implementar purga idempotente de registros vencidos y resumen agregado por versión, clase y decisión, sin exponer registros individuales por defecto.
- [ ] 3.2 [Tests / QA] Añadir pruebas sintéticas de retención, purga, agregación privada y ausencia de efectos sobre la ruta de predicción.

## 4. Verificar y cerrar

- [ ] 4.1 [Tests / QA] Ejecutar solo las pruebas unitarias afectadas, `git diff --check` y validación estricta del cambio; registrar resultados reales sin entrenar modelos.
- [ ] 4.2 [Documentación] Crear evidencia agregada y actualizar documentación canónica solo si cambian realmente los estados de `MED-04`, `MED-05` o `ADV-02`; distinguir persistencia local de autenticación, servicio compartido, despliegue y MLOps.
- [ ] 4.3 [Miguel / coordinación] Preparar la Pull Request hacia `dev` con alcance, límites de privacidad, evidencia y reversión; no fusionar ni archivar sin revisión humana.
