# complaint-routing-interface Specification

## Purpose

Definir la experiencia React PWA verificable para capturar una reclamación,
mostrar una recomendación revisable y operar con límites explícitos de
privacidad, accesibilidad, conectividad y madurez del producto.

## Requirements

### Requirement: Integración trazable del trabajo frontend

La integración MUST partir de `dev`, mantener intacta la rama
`feature/frontend-foundation`, conservar la autoría original de los commits
frontend de Abel y excluir cambios que no pertenezcan a `PG-4`.

#### Scenario: Incorporación selectiva con atribución

- **GIVEN** que la rama original contiene commits frontend y cambios ajenos al alcance
- **WHEN** se prepare la rama de integración
- **THEN** solo se incorporarán los commits o cambios frontend inventariados, conservando su autor y sin modificar la rama original

#### Scenario: Cambio ajeno detectado

- **GIVEN** que un archivo o conflicto no es necesario para la experiencia de `PG-4`
- **WHEN** se revise la diferencia frente a `dev`
- **THEN** ese cambio se excluirá de la integración y se registrará como fuera de alcance si necesita seguimiento

### Requirement: Shell React PWA instalable

La interfaz MUST ofrecer una React PWA responsive cuyo shell pueda instalarse y
volver a abrirse sin conexión después de haber sido cargado correctamente.

#### Scenario: Instalación en navegador compatible

- **GIVEN** un navegador que admite instalación de PWA
- **WHEN** la persona instala y abre la aplicación
- **THEN** el shell principal se mostrará con los recursos estáticos necesarios para iniciar la experiencia

#### Scenario: Navegador sin instalación PWA

- **GIVEN** un navegador que no admite o no ofrece instalación
- **WHEN** la persona abre la aplicación
- **THEN** el flujo web principal seguirá disponible sin exigir la instalación

### Requirement: Entrada narrativa validada y minimizada

La interfaz MUST aceptar una narrativa de texto conforme a
`PredictionRequest.narrative` en `docs/api/openapi.json`, rechazar entradas
vacías o compuestas solo por espacios y advertir contra la inclusión de datos
personales innecesarios.

#### Scenario: Narrativa válida

- **GIVEN** una narrativa sintética no vacía
- **WHEN** la persona solicita una recomendación
- **THEN** el cliente construirá un `PredictionRequest` cuyo único dato de negocio sea `narrative`

#### Scenario: Entrada vacía

- **GIVEN** un campo vacío o compuesto solo por espacios
- **WHEN** la persona intenta continuar
- **THEN** la interfaz impedirá el envío, asociará un mensaje comprensible al campo y desplazará el foco de forma accesible

#### Scenario: Protección del contenido

- **GIVEN** que la persona ha escrito o dictado una narrativa
- **WHEN** la aplicación gestiona el formulario, un error o un cambio de estado
- **THEN** no incluirá la narrativa en URLs, logs, analítica, almacenamiento persistente ni mensajes de error

### Requirement: Dictado de voz como asistencia de entrada

La interfaz MUST permitir, cuando el navegador lo soporte y la persona lo
autorice, convertir voz en texto editable dentro del mismo campo de narrativa;
el resultado validado seguirá el mismo flujo de `PredictionRequest.narrative`
que el texto escrito.

#### Scenario: Dictado disponible y autorizado

- **GIVEN** un navegador compatible y permiso concedido mediante una acción explícita de la persona
- **WHEN** la persona inicia y finaliza el dictado
- **THEN** la transcripción aparecerá en el campo de narrativa para que pueda revisarse y editarse antes del envío

#### Scenario: Dictado no disponible

- **GIVEN** un navegador sin la capacidad de reconocimiento necesaria
- **WHEN** la persona accede al formulario
- **THEN** la interfaz mantendrá la entrada por teclado y explicará la indisponibilidad sin bloquear el flujo

#### Scenario: Permiso denegado o error de reconocimiento

- **GIVEN** que el permiso se deniega o el servicio de voz falla
- **WHEN** la aplicación recibe el error
- **THEN** detendrá el estado de escucha, mostrará un mensaje seguro y permitirá continuar escribiendo

#### Scenario: Privacidad del dictado

- **GIVEN** que el reconocimiento de voz puede depender del navegador o de su proveedor
- **WHEN** la persona decide activar el dictado
- **THEN** la interfaz informará de esa dependencia y la aplicación no persistirá audio ni transcripciones

### Requirement: Cliente de predicción desacoplado y tipado

La interfaz MUST utilizar un contrato TypeScript alineado con
`PredictionRequest` y `PredictionResponse` de `docs/api/openapi.json`,
manteniendo el cliente de predicción separado de los componentes visuales. Con una
URL local de API configurada explícitamente, el cliente MAY solicitar el servicio
real; sin ella, MUST conservar el cliente mock. Ningún modo puede leer el CSV ni
acceder a artefactos de entrenamiento desde el navegador.

#### Scenario: Uso del cliente mock

- **GIVEN** que no hay una URL local de API configurada
- **WHEN** el formulario envía una narrativa válida
- **THEN** la interfaz invocará un cliente mock que respete el contrato TypeScript sin leer el CSV ni acceder a artefactos de entrenamiento

#### Scenario: Uso del cliente de servicio local

- **GIVEN** que una URL local de API está configurada explícitamente
- **WHEN** el formulario envía una narrativa válida con conexión disponible
- **THEN** la interfaz enviará únicamente `PredictionRequest.narrative` al endpoint versionado y validará la respuesta antes de mostrarla

#### Scenario: Respuesta incompatible

- **GIVEN** una respuesta que no cumple el contrato o contiene una clase fuera del contrato versionado
- **WHEN** el cliente la valida
- **THEN** la interfaz la tratará como error y no mostrará una recomendación aparentemente válida

### Requirement: Recomendación simulada inequívoca

Cuando la interfaz use el cliente mock, toda recomendación MUST identificarse de
forma visible y accesible como demostración o mock, y MUST NOT atribuirse a un
modelo entrenado ni utilizar métricas, versiones o resultados reales inventados.

#### Scenario: Resultado mock correcto

- **GIVEN** una respuesta sintética conforme al contrato
- **WHEN** se presenta el resultado
- **THEN** la clase, las alternativas y cualquier dato de confianza se mostrarán como simulados y no como rendimiento o inferencia real

#### Scenario: Confianza no disponible

- **GIVEN** una respuesta mock con confianza nula
- **WHEN** se presenta el resultado
- **THEN** no se fabricará un porcentaje y la interfaz indicará que la revisión humana es necesaria

### Requirement: Revisión humana y siguiente acción

La interfaz MUST presentar la recomendación como apoyo, comunicar
`review_required` y permitir a la persona revisar el resultado o iniciar una
nueva clasificación sin convertir la recomendación en una decisión automática.

#### Scenario: Revisión requerida

- **GIVEN** una respuesta con `review_required` igual a `true`
- **WHEN** se muestra el resultado
- **THEN** la necesidad y sus motivos serán comprensibles sin depender solo del color

#### Scenario: Nueva clasificación

- **GIVEN** que la persona ha terminado de revisar un resultado
- **WHEN** inicia una nueva clasificación
- **THEN** la vista volverá al formulario sin conservar la narrativa anterior en almacenamiento persistente

### Requirement: Estados completos y recuperación

La experiencia MUST representar de forma explícita los estados inicial, entrada
inválida, envío, resultado, revisión, error, servicio no disponible, frecuencia
limitada y sin conexión, con una acción de recuperación cuando corresponda.

#### Scenario: Envío en curso

- **GIVEN** una narrativa válida
- **WHEN** el cliente seleccionado procesa la solicitud
- **THEN** se anunciará el progreso y se impedirán envíos duplicados

#### Scenario: Error seguro

- **GIVEN** un error del cliente o una respuesta inválida
- **WHEN** el flujo falla
- **THEN** se mostrará un mensaje comprensible sin la narrativa, stack traces ni detalles internos

#### Scenario: Servicio no disponible

- **GIVEN** una configuración de cliente real que no puede alcanzar el servicio
- **WHEN** se intenta clasificar
- **THEN** la interfaz indicará la indisponibilidad y ofrecerá reintento sin fabricar un resultado

### Requirement: Comportamiento offline honesto

El modo offline MUST limitarse al shell, la ayuda y el contenido estático
disponible; MUST NOT producir una recomendación mock o real cuando la
experiencia esté configurada para requerir un servicio no disponible.

#### Scenario: Apertura del shell sin conexión

- **GIVEN** que la PWA se cargó previamente y sus recursos se almacenaron correctamente
- **WHEN** la persona la abre sin conexión
- **THEN** podrá ver el shell y una explicación clara de las funciones disponibles y no disponibles

#### Scenario: Solicitud sin conexión

- **GIVEN** que la clasificación requiere un servicio y no hay conexión
- **WHEN** la persona intenta solicitar una recomendación
- **THEN** no se generará un resultado y se informará de que la conexión es necesaria

### Requirement: Accesibilidad y adaptación responsive

El flujo principal MUST ser utilizable con teclado y tecnologías de asistencia,
conservar foco visible, anunciar cambios de estado, no depender solo del color y
adaptarse a vistas móvil, tablet y escritorio sin pérdida de contenido o
acciones.

#### Scenario: Uso completo con teclado

- **GIVEN** una persona que no utiliza puntero
- **WHEN** recorre formulario, dictado, resultado, revisión y nueva clasificación
- **THEN** podrá identificar y activar todas las acciones en un orden de foco coherente

#### Scenario: Cambio de estado anunciado

- **GIVEN** que la interfaz pasa de formulario a carga, error o resultado
- **WHEN** cambia el contenido relevante
- **THEN** el nuevo estado se anunciará mediante semántica accesible y texto comprensible

#### Scenario: Vista móvil

- **GIVEN** un viewport móvil soportado
- **WHEN** se recorre el flujo principal
- **THEN** no habrá desbordamientos que oculten texto, controles o acciones necesarias

### Requirement: Capacidades pendientes separadas del alcance entregable

El login y autenticación mock, el panel administrativo, las pantallas de
entrenamiento y el registro o comparación de modelos MUST NOT eliminarse por
defecto durante la integración, pero MUST quedar identificados como propuestas
pendientes de aprobación y separados del flujo principal verificable de `PG-4`.

#### Scenario: Capacidad pendiente visible

- **GIVEN** que una ruta o componente pendiente se conserva en la integración
- **WHEN** una persona accede a ella
- **THEN** la interfaz indicará que es una propuesta o demo sin presentar autenticación, administración, entrenamiento, registro o comparación como capacidades de producción

#### Scenario: Métricas o modelos no existentes

- **GIVEN** una pantalla pendiente relacionada con entrenamiento o modelos
- **WHEN** muestra contenido de demostración
- **THEN** utilizará datos inequívocamente sintéticos y no afirmará precisión, entrenamiento, versión desplegada o rendimiento real

### Requirement: Verificación reproducible de la integración

La entrega MUST aportar evidencia reproducible de typecheck, lint, formato,
tests, build, auditoría de dependencias, quality gate del repositorio y
revisiones de accesibilidad, responsive, offline, dictado y privacidad.

#### Scenario: Comprobaciones automáticas correctas

- **GIVEN** la integración preparada para revisión
- **WHEN** se ejecutan los comandos versionados en las tareas del cambio
- **THEN** cada comprobación finalizará correctamente o conservará una excepción explícita, acotada y aprobada con su riesgo

#### Scenario: Vulnerabilidad detectada

- **GIVEN** que la auditoría identifica una dependencia vulnerable
- **WHEN** se evalúa una actualización
- **THEN** no se utilizará un arreglo forzado y cualquier riesgo no resoluble de forma compatible quedará documentado antes de solicitar integración

### Requirement: Identidad y madurez del prototipo comunicadas con precisión

La documentación de la capacidad `complaint-routing-interface` MUST usar la
identidad visible integrada de la interfaz y MUST comunicar que sigue siendo un
prototipo React PWA. La identidad visual MUST NOT alterar el contrato de
predicción ni utilizarse para afirmar que existen autenticación, administración,
entrenamiento, registro de modelos o despliegue operativos. La inferencia local
debe seguir identificándose como una recomendación con revisión humana, no como
un producto desplegado.

#### Scenario: Consulta del manual de frontend

- **WHEN** una persona consulte el README raíz, el manual de la interfaz o las
  fuentes de presentación después de una evolución visual integrada
- **THEN** encontrará la identidad actual, los límites de mock y la referencia
  a la evidencia de integración sin contradicciones entre documentos

#### Scenario: Pantallas propuestas conservadas

- **WHEN** la interfaz incluya rutas o pantallas de autenticación,
  administración, entrenamiento o modelos como propuesta visual
- **THEN** la documentación las mantendrá diferenciadas de las capacidades
  operativas y no las utilizará como evidencia de un nivel de entrega
