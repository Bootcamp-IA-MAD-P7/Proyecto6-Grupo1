# claimvox-ui-redesign Specification

## MODIFIED Requirements

Baseline spec:
`openspec/specs/complaint-routing-interface/spec.md`.

### Requirement: Layout unificado por roles

La PWA SHALL usar un único layout responsivo cuya barra lateral izquierda
muestre ítems de navegación filtrados por el rol de la persona autenticada.
El rol `user` ve `Home` y `Classify`; el rol `admin` ve `Home`, `Classify`,
`Dashboard`, `Training` y `Models`. Ambos roles ven `Settings`
(ThemeToggle) al pie de la barra.

La cabecera SHALL mostrar el nombre, el rol y un botón de cierre de sesión
para cualquier rol autenticado.

#### Scenario: Persona con rol user ve navegación limitada

- **GIVEN** una persona autenticada con rol `user`
- **WHEN** se renderiza el layout principal
- **THEN** la barra lateral contiene `Home`, `Classify` y `Settings`, y NO
  contiene enlaces a `Dashboard`, `Training` ni `Models`

#### Scenario: Persona con rol admin ve navegación completa

- **GIVEN** una persona autenticada con rol `admin`
- **WHEN** se renderiza el layout principal
- **THEN** la barra lateral contiene `Home`, `Classify`, `Dashboard`,
  `Training`, `Models` y `Settings`

#### Scenario: Cabecera unificada con identidad

- **GIVEN** una persona autenticada
- **WHEN** se renderiza el layout principal
- **THEN** la cabecera muestra el nombre, el rol y un botón de cierre de
  sesión, independientemente del rol

### Requirement: Flujo de clasificación guiado en 4 pasos

`ClassificationPage` SHALL organizar el flujo de narrativa y clasificación
en cuatro pasos secuenciales con una barra de progreso visible: Describe,
Review, Guidance, Next step. La implementación SHALL ser una sola página
con estados, no rutas separadas.

El paso Describe SHALL ofrecer un textarea de narrativa limitado a 6 líneas
visuales (sin desbordamiento), dictado opcional por voz, un aviso de
privacidad y una acción primaria "Clasificar reclamación" / "Obtener
orientación".

#### Scenario: Barra de progreso visible

- **GIVEN** una persona en la página de clasificación
- **WHEN** se renderiza el flujo
- **THEN** se muestra una barra de progreso con los pasos Describe, Review,
  Guidance y Next step, con el paso actual resaltado

#### Scenario: Paso Describe con textarea limitado

- **GIVEN** una persona en el paso Describe
- **WHEN** se renderiza el área de narrativa
- **THEN** el textarea ocupa un máximo de 6 líneas visuales antes de
  activar el desplazamiento interno

#### Scenario: Acción primaria sin promesa de decisión

- **GIVEN** una narrativa válida
- **WHEN** la persona activa la acción principal
- **THEN** el texto del botón es "Clasificar reclamación" o "Obtener
  orientación", y ningún texto de la interfaz promete una decisión final o
  enrutamiento automático

### Requirement: Etiquetas profesionales sin terminología de prototipo

La PWA SHALL eliminar las etiquetas "mock response", "interface
demonstration only", "prototype", "concept" y "proposal only" del flujo
principal de clasificación. Cuando el servicio local esté disponible y
configurado, la interfaz SHALL mostrar "Predicción local", versión del
modelo y confianza. Cuando no haya servicio disponible, SHALL mostrar
"Servicio no disponible" sin fabricar un resultado ni etiquetarlo como
mock.

Las páginas de administración SHALL conservar indicadores de datos no
disponibles sin usar la palabra "Proposal".

#### Scenario: Servicio local disponible

- **GIVEN** que `VITE_PREDICTION_API_BASE_URL` está configurada y el
  servicio responde correctamente
- **WHEN** se completa una clasificación
- **THEN** el resultado se muestra como "Predicción local" con la versión
  del modelo, confianza y revisión humana, sin etiquetas "mock" ni
  "prototype"

#### Scenario: Servicio no disponible

- **GIVEN** que no hay servicio configurado o no responde
- **WHEN** una persona intenta clasificar
- **THEN** la interfaz muestra "El servicio de predicción no está
  disponible" sin mostrar una respuesta sintética ni etiquetarla como mock

#### Scenario: Página de administración sin datos operativos

- **GIVEN** una página de administración (Dashboard, Training, Models)
- **WHEN** no existen datos conectados
- **THEN** la página muestra indicadores de "No conectado" o "Sin datos"
  sin usar la etiqueta "Proposal only" ni "Concept"

### Requirement: Panel explicativo de revisión humana

El layout SHALL incluir un panel lateral derecho (o sección apilada en
móvil) que explique de forma persistente que la sugerencia requiere
revisión humana, con texto explícito, estructura semántica accesible y sin
iconografía genérica de IA.

#### Scenario: Panel visible durante la clasificación

- **GIVEN** una persona en el flujo de clasificación
- **WHEN** se renderiza la página
- **THEN** un panel o sección visible explica que la sugerencia requiere
  revisión humana, usando texto, no solo color o iconos

### Requirement: Aviso contextual útil al pie

La página de clasificación SHALL incluir un aviso contextual ("Helpful
tip") al pie del contenido, con información sobre cómo redactar una
narrativa útil, sin iconografía de IA ni recursos externos.

#### Scenario: Tip visible y colapsable

- **GIVEN** una persona en la página de clasificación
- **WHEN** se renderiza la página
- **THEN** se muestra un aviso contextual con un consejo sobre la
  narrativa, que puede ocultarse o mostrarse mediante un control accesible

### Requirement: Tema en sección Settings de la barra lateral

El control de cambio de tema (ThemeToggle) SHALL ubicarse en una sección
"Settings" al pie de la barra lateral, accesible para ambos roles.

#### Scenario: ThemeToggle en Settings

- **GIVEN** una persona autenticada
- **WHEN** se renderiza la barra lateral
- **THEN** el control de cambio de tema aparece dentro de una sección
  "Settings" al final de la barra, no en la cabecera

### Requirement: Accesibilidad y responsive del rediseño

El layout unificado y el flujo de 4 pasos SHALL mantener navegación por
teclado con foco visible, contraste suficiente, estructura semántica,
anuncio de cambios de estado y adaptación a escritorio, tableta y móvil
sin pérdida de contenido ni acciones.

#### Scenario: Navegación por teclado completa

- **GIVEN** una persona que usa solo teclado
- **WHEN** recorre la barra lateral, cabecera, flujo de 4 pasos y panel
  de revisión
- **THEN** cada elemento interactivo recibe foco visible en orden
  coherente y puede activarse sin puntero

#### Scenario: Diseño responsive

- **GIVEN** un viewport de tableta o móvil
- **WHEN** se renderiza el layout unificado
- **THEN** la barra lateral se colapsa o apila, el panel derecho pasa
  debajo del contenido principal, y ninguna acción o texto queda oculto
  por desbordamiento
