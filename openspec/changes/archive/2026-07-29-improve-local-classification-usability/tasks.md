# Tareas: usabilidad de clasificación local

## 1. Revisar el contrato y el recorrido

- [x] 1.1 [Frontend / UX] Inventariar los estados y campos contractuales ya consumidos por la pantalla de clasificación, sin cambiar API ni modelo. Evidencia: `reports/validation/claimvox_local_classification_ui_inventory.md` identifica campos, estados existentes y cuatro ajustes acotados.
- [x] 1.2 [Frontend / UX] Definir el texto seguro por defecto para revisión humana, fuente, error y recuperación, sin prometer operación productiva. Evidencia: `design.md` fija el catálogo aprobado de API local, mock, revisión sin motivo, carga, error y reinicio.

## 2. Mejorar la interfaz funcional

- [x] 2.1 [Frontend] Ajustar la presentación de resultado para diferenciar respuesta local y mock, jerarquizar clase, confianza, versión y revisión humana. Evidencia: `ClassificationPage.tsx` propaga el modo configurado y `PredictionResult.tsx` identifica fuente local/mock y separa versión de modelo; type-check superado.
- [x] 2.2 [Frontend] Limitar alternativas a tres, mostrar motivo de revisión seguro y mejorar estados de carga, error y reinicio. Evidencia: `PredictionResult.tsx` limita alternativas a tres, informa ausencia y muestra motivo seguro; type-check superado.
- [x] 2.3 [Frontend] Mantener las rutas administrativas conceptuales fuera del recorrido de clasificación funcional, sin convertirlas en operación real. Evidencia: `UserLayout.tsx` elimina la entrada visible de sesión mock y mantiene Home/Classify como recorrido público; las rutas conceptuales no cambian ni se presentan como operativas.

## 3. Verificar

- [x] 3.1 [Tests / QA] Añadir o ajustar pruebas de componente con contratos sintéticos para fuente, alternativas, revisión, carga y error. Evidencia: `npm exec -- vitest run src/pages/user/ClassificationPage.test.tsx src/layouts/UserLayout.test.tsx` superado: 18 pruebas, 0 fallos; cubre fuente, alternativas, revisión, carga, error y navegación pública.
- [x] 3.2 [UX / QA] Realizar una revisión manual local con texto sintético contra API configurada y registrar evidencia agregada. Evidencia: `reports/validation/claimvox_local_classification_usability.md`; revisión manual confirmada el 29 de julio de 2026, sin narrativas CFPB reales.

## 4. Cerrar

- [x] 4.1 [Verificación] Ejecutar solo los tests frontend afectados, `git diff --check` y la validación OpenSpec estricta. Evidencia: `npm exec -- vitest run src/pages/user/ClassificationPage.test.tsx src/layouts/UserLayout.test.tsx` superado: 18 pruebas, 0 fallos; `npm exec -- tsc --noEmit --pretty false`, `git diff --check` y `npm exec -- openspec validate improve-local-classification-usability --type change --strict` superados el 29 de julio de 2026.
- [x] 4.2 [Documentación] Actualizar únicamente evidencia y documentación canónica cuyo significado cambie; diferenciar local real, mock, administración conceptual y despliegue pendiente. Evidencia: `reports/validation/claimvox_local_classification_usability.md`, README, CHANGELOG y fuentes NotebookLM actualizados sin afirmar autenticación, administración operativa ni despliegue.
- [x] 4.3 [Miguel / coordinación] Preparar PR hacia `dev` con alcance, evidencia, límites y reversión; no fusionar ni archivar sin revisión humana. Evidencia: PR [#58](https://github.com/Bootcamp-IA-MAD-P7/Proyecto6-Grupo1/pull/58) revisada y fusionada hacia `dev`; no amplía el contrato de predicción ni presenta la administración conceptual como capacidad operativa.
