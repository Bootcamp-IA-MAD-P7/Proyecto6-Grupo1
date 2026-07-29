## 1. Delimitación y estructura del prototipo

- [x] 1.1 [Frontend/UX] Confirmar que la exploración parte de la rama aislada y
  que ningún archivo existente de `app/interface/` está incluido en el alcance.
  Evidencia: `git diff --name-only dev...HEAD` antes de construir la maqueta.
- [x] 1.2 [Frontend/UX] Crear `docs/design/claimvox-ux-ui-prototype/` con una
  nota de alcance que identifique la maqueta como propuesta visual no integrada
  y explique cómo abrirla localmente.
- [x] 1.3 [Frontend/UX] Registrar en la nota de alcance las decisiones que
  requieren validación de Abel antes de cualquier integración en ClaimVox.

## 2. Maqueta visual aislada

- [x] 2.1 [Frontend/UX] Crear una pantalla estática navegable con navegación
  lateral, cabecera, progreso de cuatro pasos, área narrativa, dictado opcional,
  acción de orientación, panel de revisión humana y ayuda contextual.
- [x] 2.2 [Frontend/UX] Usar exclusivamente contenido sintético, etiquetas de
  propuesta visual y mensajes que separen mock, predicción local conceptual y
  capacidades futuras no implementadas.
- [x] 2.3 [Frontend/UX] Implementar adaptación para escritorio, tableta y móvil
  sin modificar `app/interface/`, API ni dependencias.
- [x] 2.4 [Frontend/UX] Revisar estructura semántica, etiquetas, foco visible,
  orden de tabulación, contraste y mensajes de privacidad del prototipo.

## 3. Evidencia y revisión de diseño

- [x] 3.1 [Frontend/UX] Evaluar la necesidad de capturas pequeñas y
  versionables. Decisión: no se añaden capturas automáticas porque no hay
  navegador controlable en la revisión; `review.md` deja un recorrido manual
  verificable para escritorio, tableta y móvil.
- [x] 3.2 [Frontend/UX] Documentar diferencias frente a la aplicación actual,
  elementos reutilizables y trabajo que requeriría un cambio OpenSpec de
  integración posterior.
- [x] 3.3 [Miguel / coordinación] Revisar que el prototipo no se presente como
  una capacidad entregada ni cambie estados de Jira o niveles de entrega.

## 4. Verificación y entrega para decisión humana

- [x] 4.1 [Frontend/UX] Ejecutar `python scripts/quality/check_repository.py`,
  `git diff --check` y `npm exec -- openspec validate
  propose-claimvox-ux-ui-prototype --type change --strict`.
- [x] 4.2 [Frontend/UX] Presentar archivos creados, instrucciones de apertura,
  evidencia visual, riesgos y decisiones pendientes sin hacer commit, push, PR,
  merge ni archive.
