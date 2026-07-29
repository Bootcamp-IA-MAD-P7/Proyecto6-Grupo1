## 1. Preparar la comprobación local

- [ ] 1.1 [Backend / QA] Confirmar contrato de predicción, política de feedback,
  artefacto local reproducible y raíz local controlada antes de ejecutar. Evidencia:
  configuración local y comandos de health sin exponer rutas sensibles, registros
  ni contenido introducido.
- [ ] 1.2 [Backend / QA] Definir una única narrativa sintética y los metadatos
  cerrados de feedback derivados de la respuesta local. Evidencia: plan de
  prueba que no incluya narrativas CFPB, identidad, texto libre ni UUID.

## 2. Verificar el recorrido extremo a extremo

- [ ] 2.1 [Backend / QA] Iniciar la API local con el artefacto reproducible y
  comprobar salud y predicción real contractual. Evidencia: resultado agregado
  con modo local, versión disponible y clase canónica, sin copiar la narrativa.
- [ ] 2.2 [Backend / QA] Registrar feedback permitido posterior a esa predicción
  y consultar el resumen local. Evidencia: creación aceptada, resumen exclusivo
  por versión/clase/decisión, ausencia de registros individuales e independencia
  de la predicción.
- [ ] 2.3 [Backend / QA] Comprobar el rechazo seguro de un campo no permitido y
  la indisponibilidad recuperable de la API de feedback. Evidencia: estados de
  error sin reflejar valores sensibles ni fabricar persistencia.

## 3. Decidir y documentar

- [ ] 3.1 [Miguel / coordinación] Crear evidencia agregada versionable del
  recorrido local y decidir si satisface `MED-04`; mantener `MED-05` en curso.
- [ ] 3.2 [Documentación] Actualizar `delivery_levels.md`, README, CHANGELOG y
  fuentes NotebookLM solo si el significado canónico cambia, preservando los
  límites de autenticación, almacenamiento compartido, despliegue, MLOps y
  reentrenamiento.
- [ ] 3.3 [Verificación] Ejecutar solo pruebas y comprobaciones afectadas,
  `git diff --check` y `npm exec -- openspec validate verify-local-feedback-e2e --type change --strict` antes de revisión humana.
