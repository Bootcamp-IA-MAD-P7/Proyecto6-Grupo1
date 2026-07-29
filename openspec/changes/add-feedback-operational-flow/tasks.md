## 1. Contrato local y frontera de privacidad

- [ ] 1.1 [Backend] Definir esquemas tipados de creación de feedback y resumen agregado que acepten solo campos y vocabularios de `claimvox_feedback_persistence_policy.json`. Evidencia: pruebas sintéticas de esquema y errores sin valores sensibles.
- [ ] 1.2 [Backend] Extender `docs/api/openapi.json` con operaciones locales versionadas de creación y resumen de feedback, sin incluir narrativa, identidad ni exportación individual. Verificación: validación estructural del JSON.

## 2. Servicio local de feedback

- [ ] 2.1 [Backend] Implementar el caso de uso local que valide el feedback antes de delegar en el repositorio PG-14 y mantenga la predicción independiente. Evidencia: prueba sintética de creación conforme y rechazo de campos prohibidos.
- [ ] 2.2 [Backend] Exponer rutas locales para crear feedback y consultar exclusivamente el resumen agregado, con errores seguros y sin red ni base compartida. Evidencia: pruebas directas del cliente ASGI con UUID y clases sintéticas.
- [ ] 2.3 [Backend] Ejecutar purga idempotente antes del resumen y registrar solo contadores agregados. Evidencia: prueba de vencidos, vigentes y ausencia de UUID o registros individuales en la salida.

## 3. Recorrido explícito en ClaimVox

- [ ] 3.1 [Frontend] Añadir un cliente de feedback local desacoplado y configurable, sin reutilizar ni persistir la narrativa de predicción. Verificación: type-check y pruebas de contrato sintético.
- [ ] 3.2 [Frontend] Añadir controles posteriores al resultado para decisiones y finalidades permitidas, con clase revisada solo cuando la decisión lo exija. Evidencia: pruebas de componente con contratos sintéticos, sin narrativas CFPB.
- [ ] 3.3 [Frontend] Comunicar éxito, indisponibilidad y límites de privacidad de forma accesible, sin bloquear una predicción ni presentar la operación como autenticada o desplegada. Evidencia: pruebas de estado y revisión manual local con entrada sintética.

## 4. Recolección gobernada y evidencia

- [ ] 4.1 [Datos / arquitectura] Definir la evidencia agregada de candidatos de reentrenamiento y sus límites: no hay corpus, validación, deduplicación ni incorporación automática. Evidencia: informe versionado sin registros individuales ni narrativas.
- [ ] 4.2 [Tests / QA] Ejecutar solo las pruebas nuevas o afectadas de backend y frontend, type-check, `git diff --check` y validación OpenSpec estricta. Registrar resultados reales.

## 5. Documentar y cerrar

- [ ] 5.1 [Documentación] Actualizar únicamente README, CHANGELOG, niveles de entrega y fuentes NotebookLM cuyo significado cambie; distinguir feedback local implementado de autenticación, operación compartida, reentrenamiento, Docker y despliegue pendientes.
- [ ] 5.2 [Miguel / coordinación] Revisar humanamente la evidencia de `MED-04` y `MED-05`, actualizar Jira `PG-13` con enlaces reales y preparar PR hacia `dev`; no verificar criterios ni archivar sin evidencia completa y revisión humana.
