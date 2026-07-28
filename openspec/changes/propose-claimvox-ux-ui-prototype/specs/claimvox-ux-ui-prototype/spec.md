## ADDED Requirements

### Requirement: Prototipo visual aislado y explícito

El repositorio SHALL contener una propuesta visual navegable de ClaimVox fuera
de `app/interface/`, identificada como no integrada y sin dependencias de API,
modelo, datos, autenticación ni persistencia.

#### Scenario: Revisión local del prototipo
- **WHEN** una persona abre la maqueta desde la ruta documentada
- **THEN** puede revisar el flujo visual sin iniciar la React PWA, FastAPI ni un
  artefacto de modelo

#### Scenario: Diferenciación frente a la aplicación entregada
- **WHEN** una persona consulta la maqueta o su documentación
- **THEN** encuentra un aviso visible de que es una propuesta visual no
  integrada y no la interpreta como evidencia de una capacidad de entrega

### Requirement: Flujo visual de orientación revisable

El prototipo SHALL representar un flujo de describir, revisar, orientación
sugerida y siguiente paso, con una zona principal de narrativa, una llamada
opcional a dictado y una explicación persistente de revisión humana.

#### Scenario: Persona revisa el flujo principal
- **WHEN** una persona recorre la pantalla principal del prototipo
- **THEN** identifica el paso actual, la narrativa como entrada principal, la
  acción de obtener orientación y que cualquier sugerencia requiere revisión
  humana

#### Scenario: Estado de propuesta sin inferencia
- **WHEN** el prototipo representa una orientación o un resultado
- **THEN** lo identifica como ejemplo mock o estado conceptual y no afirma que
  se haya realizado una predicción, una decisión o un enrutamiento automático

### Requirement: Privacidad, accesibilidad y adaptación de la propuesta

El prototipo SHALL recordar que no se introduzca información personal
innecesaria, informar de que el dictado depende del navegador y no persiste
audio, y ofrecer estructura semántica, foco visible y adaptación a escritorio,
tableta y móvil.

#### Scenario: Entrada narrativa responsable
- **WHEN** una persona observa el área de narrativa del prototipo
- **THEN** recibe una indicación comprensible para describir el problema sin
  introducir datos personales innecesarios

#### Scenario: Revisión con teclado y pantalla reducida
- **WHEN** una persona usa teclado o reduce el ancho de la ventana
- **THEN** los controles conservan foco visible, orden lógico y contenido sin
  desbordamientos que oculten acciones esenciales

### Requirement: Decisiones preparadas para integración futura

La propuesta SHALL documentar qué decisiones visuales son candidatas, qué
elementos reutilizarían capacidades existentes y qué revisión de frontend/UX se
necesita antes de modificar la aplicación integrada.

#### Scenario: Evaluación de posible integración
- **WHEN** la responsabilidad de frontend/UX revisa la propuesta
- **THEN** puede distinguir decisiones aprobables, trabajo fuera de alcance y
  requisitos de un cambio OpenSpec posterior sin reinterpretar el prototipo
  como implementación existente
