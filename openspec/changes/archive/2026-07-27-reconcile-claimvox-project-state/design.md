## Context

La PR #28 fusionó la evolución visual de la React PWA de `PG-4` en `dev`.
El cambio conserva el prototipo como una interfaz con datos y respuestas
sintéticas, pero actualiza su identidad visible a ClaimVox, añade la
preferencia de tema claro/oscuro/sistema y mejora elementos de accesibilidad y
presentación. La PR no actualizó el conjunto transversal de fuentes que usa el
arnés para contextualizar a personas e IAs.

En paralelo, `PG-2` quedó en `Listo` tras las PR #27 y #29. El siguiente hito
de datos es `PG-3`, que preparará el baseline sin usar el test protegido para
seleccionar. Sin embargo, `AGENTS.md`, el manual de Jira y la tabla de equipo
todavía presentan el EDA inicial como trabajo activo y mantienen dependencias
ya resueltas.

La documentación tiene tres audiencias con necesidades distintas:

- el equipo y sus IAs necesitan instrucciones operativas actuales;
- la presentación para cliente necesita explicar valor y límites sin proceso
  interno innecesario;
- los revisores necesitan trazabilidad entre Jira, OpenSpec, GitHub y las
  evidencias versionadas.

Restricciones: no se modifica el código integrado de Abel, no se cambia Jira
desde el repositorio y ninguna referencia puede acreditar modelo, backend,
inferencia, autenticación, administración, entrenamiento, despliegue o MLOps
reales que aún no existen.

## Goals / Non-Goals

**Goals:**

- Mantener una descripción única y verificable del prototipo ClaimVox y sus
  límites en las fuentes que alimentan al equipo, al arnés y a NotebookLM.
- Actualizar responsables, hitos y bloqueos documentales conforme al estado
  integrado: `PG-2` preparado y cerrado, `PG-3` listo para planificación,
  `PG-4` integrado y ampliado mediante la PR #28, `PG-5` aún dependiente del
  modelo evaluado.
- Registrar actividad real por persona en la daily, con lenguaje proporcionado
  pero sin atribuir implementación, datos o decisiones a quien no las realizó.
- Conservar la trazabilidad de `PG-4`, PR #28 y el cambio OpenSpec archivado
  `integrate-frontend-foundation`.

**Non-Goals:**

- Validar de nuevo la interfaz, alterar su diseño o realizar pruebas de
  navegador adicionales.
- Completar `ESS-04`, actualizar criterios de entrega o convertir pantallas
  mock en capacidades operativas.
- Reabrir decisiones de idioma, partición, desbalanceo, modelo, backend,
  privacidad operativa o despliegue.
- Cambiar el estado de tickets Jira desde esta rama; la sincronización se
  limita a describir el estado que ya consta en Jira y GitHub.

## Decisions

### 1. GitHub integrado y evidencia versionada prevalecen sobre texto heredado

Para establecer el estado se priorizan: la PR fusionada y sus commits, los
artefactos OpenSpec archivados, los informes de validación y el estado de Jira
confirmado por una persona. Las tablas heredadas de `specs/` se conservan como
compatibilidad, pero no se usan para declarar trabajo actual cuando contradicen
el estado integrado.

Se descarta reescribir todos los expedientes históricos porque perdería su
valor de trazabilidad y ampliaría innecesariamente el alcance.

### 2. ClaimVox se documenta como identidad de un prototipo, no como producto

El README principal, la documentación técnica de frontend y las fuentes de
NotebookLM usarán ClaimVox para referirse a la interfaz visible. Cuando se
hable del problema o del contrato técnico, se mantendrá la expresión
"clasificación y apoyo al enrutamiento de reclamaciones". Así se distingue la
marca de interfaz de la capacidad aún en estudio.

Se descarta una renombrada global de rutas, contratos, nombres históricos y
capacidad OpenSpec: podría implicar cambios de API o alcance que la PR #28 no
ha propuesto ni verificado.

### 3. Separar estado integrado, próximo trabajo y bloqueos

Las fuentes operativas usarán etiquetas explícitas: integrado, pendiente,
bloqueado o propuesto. `PG-2` se describirá como cerrado con su preparación de
datos; `PG-3` como trabajo de baseline pendiente de iniciar; `PG-4` como
prototipo integrado con evolución visual; `PG-5` como bloqueado por la
existencia y evaluación del baseline, no por la preparación ya finalizada.

Se descarta presentar el movimiento de Jira como una prueba técnica. Jira
aporta asignación y estado, mientras que OpenSpec y GitHub conservan alcance,
verificación y evidencia.

### 4. Daily equilibrada por tipo de aportación verificable

La daily diferenciará implementación fusionada de Abel, evidencia de datos y
próximo baseline de Víctor, coordinación documental de Miguel y preparación o
bloqueo del backend de José. El equilibrio será de claridad, no de inventar
volumen de trabajo equivalente.

Se descarta resumirla como una lista única de cambios porque ocultaría tanto
las responsabilidades como los bloqueos relevantes.

### 5. NotebookLM recibe hechos seleccionados, no el proceso completo

`project_facts.md`, `technical_status.md`, `business_narrative.md` y el
catálogo se actualizarán solo si cambia su significado. La narrativa para
cliente mencionará que existe una demostración visual ClaimVox, pero mantendrá
el problema, el valor esperado, la revisión humana y los límites por delante de
OpenSpec, Jira o detalles de tema.

Se descarta alimentar la presentación con toda la documentación de gobierno:
esa información sirve para trabajo interno y podría hacer que una narrativa de
cliente empiece por terminología técnica.

## Risks / Trade-offs

- [Una PR de diseño sin checklist completo puede dejar evidencia de validación
  incompleta] → Documentar solo los cambios confirmados por el diff fusionado;
  no afirmar pruebas adicionales y señalar cualquier verificación pendiente.
- [La marca ClaimVox puede confundirse con un producto desplegado] → Añadir
  siempre "prototipo" o "interfaz demostrativa" cuando se describan sus
  capacidades actuales.
- [Los documentos heredados pueden volver a quedar desfasados] → Centralizar
  el estado operativo en `AGENTS.md`, README, guía de Jira y OpenSpec; mantener
  los expedientes numerados como histórico de compatibilidad.
- [Una daily equilibrada puede diluir la autoría] → Indicar explícitamente
  contribución, responsabilidad, coordinación o bloqueo según corresponda.
- [NotebookLM puede mezclar fuentes de distintas audiencias] → Mantener el
  catálogo y su regla editorial; verificar la selección antes de cada carga.

## Migration Plan

1. Inventariar PR #28, los cambios archivados y los estados confirmados de
   Jira, sin modificar Jira ni código.
2. Actualizar primero el contexto operativo del arnés y la guía de equipo para
   evitar que nuevos paquetes de IA propaguen referencias obsoletas.
3. Alinear README, documentación de frontend cuando sea necesario, daily,
   changelog y fuentes de NotebookLM.
4. Ejecutar comprobaciones documentales, la validación estricta del cambio y
   generar el paquete NotebookLM de la fecha.
5. Solicitar revisión humana mediante Pull Request. Si una afirmación no puede
   confirmarse, se elimina o se marca como pendiente antes de integrar.

La reversión consiste en revertir exclusivamente el commit documental de esta
rama. No hay migraciones de datos, código ni infraestructura que deshacer.

## Open Questions

- La PR #28 se integró con la plantilla de PR sin completar; esta
  reconciliación no puede reconstruir verificaciones no registradas. Solo se
  describirá lo observable en el cambio fusionado y en la evidencia existente.
- La asignación formal y el inicio de `PG-3` deben confirmarse en Jira antes de
  comenzar su cambio OpenSpec; esta reconciliación no los ejecuta.
- La revisión manual equivalente en Edge continúa pendiente según la evidencia
  de `PG-4`; el tema visual añadido por la PR #28 no permite cerrarla por sí
  solo.
