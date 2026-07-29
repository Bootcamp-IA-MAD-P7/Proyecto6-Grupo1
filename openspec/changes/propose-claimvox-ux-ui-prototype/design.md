## Context

ClaimVox dispone de una React PWA integrada y verificable. La referencia visual
aportada propone una composición distinta: navegación lateral, progreso por
pasos, formulario central, acción primaria y panel de explicación. El objetivo
es evaluar esa composición sin modificar la aplicación ni confundir un estudio
visual con una funcionalidad entregada.

La responsabilidad de frontend/UX conserva la decisión de integrar, adaptar o
descartar la propuesta. El prototipo no cambia `PG-4`, no altera su autoría ni
acredita ninguna capacidad adicional frente a los niveles de entrega.

## Goals / Non-Goals

**Goals:**

- Crear una maqueta navegable de bajo peso con un flujo visual de cuatro pasos:
  describir, revisar, orientación sugerida y siguiente paso.
- Comunicar entrada minimizada, dictado opcional, modo mock/predicción local y
  revisión humana obligatoria con texto explícito.
- Documentar el comportamiento esperado en escritorio, tableta y móvil, con
  foco visible, semántica accesible y contraste suficiente.
- Hacer la comparación futura sencilla: el resultado debe abrirse localmente
  desde documentación y no depender de API, datos, modelo o dependencias.

**Non-Goals:**

- Modificar, copiar, bifurcar o sustituir `app/interface/`.
- Crear un flujo de autenticación, perfil, administración, métricas, analítica,
  persistencia, backend o predicción.
- Mostrar narrativas reales, información personal, resultados reales o métricas
  como parte de la maqueta.
- Decidir la identidad visual final o integrar la propuesta sin aprobación
  explícita de frontend/UX.

## Decisions

### Prototipo estático aislado

La propuesta se implementará, después de una segunda aprobación humana, como
HTML, CSS y JavaScript mínimos en `docs/design/claimvox-ux-ui-prototype/`.
Abrir `index.html` localmente será suficiente para revisar la composición.

**Alternativa considerada:** modificar rutas o componentes de `app/interface/`.
Se descarta porque mezclaría exploración y producto integrado, aumentaría el
riesgo de regresión y exigiría una integración funcional no autorizada.

### Inspiración estructural, no copia visual

Se adoptan la jerarquía, la distribución y el patrón de progreso de la
referencia. Se crearán textos, símbolos CSS o iconos de interfaz propios y
sobrios; no se copiarán marca, ilustraciones, textos, colores ni iconos de la
referencia. La propuesta conservará el nombre ClaimVox y los límites de
privacidad actuales.

**Alternativa considerada:** reproducir la imagen píxel a píxel. Se descarta
por falta de autorización de reutilización visual y porque no resolvería las
necesidades propias de ClaimVox.

### Estados honestos y datos sintéticos

El prototipo mostrará etiquetas de propuesta visual y utilizará contenido
puramente sintético. Si se representa un resultado, se identificará como mock;
si se representa el modo local, se mostrará como estado conceptual no conectado
y siempre con revisión humana requerida.

**Alternativa considerada:** consumir la API local. Se descarta porque la
propuesta es de diseño y no debe depender de ejecución, artefactos ni datos.

### Accesibilidad y responsive como parte del diseño

La maqueta incluirá estructura semántica, orden de foco coherente, foco visible,
etiquetas asociadas, mensajes no dependientes del color y puntos de ruptura para
móvil, tableta y escritorio. Los controles de navegación serán demostrativos y
no prometerán navegación operativa externa.

## Risks / Trade-offs

- [La maqueta puede confundirse con una segunda app] → Etiqueta persistente
  “Propuesta visual no integrada”, documentación de alcance y ausencia de API.
- [El estilo puede alejarse de la identidad entregada] → Registrar los tokens y
  decisiones como candidatos sujetos a validación de Abel.
- [El formulario puede normalizar la recogida excesiva de datos] → Incluir una
  instrucción visible para no introducir información personal innecesaria y no
  solicitar campos adicionales.
- [El diseño puede parecer accesible sin estar validado] → Tratar la revisión
  como evidencia de maqueta; una integración futura requerirá pruebas reales.
- [Los iconos o recursos pueden aumentar el peso o tener licencias inciertas]
  → Usar elementos propios de CSS o texto, sin dependencias ni recursos externos.

## Migration Plan

No existe migración: se añaden únicamente archivos nuevos fuera de la aplicación
integrada. Para revertir la exploración basta eliminar el directorio aislado y
revertir el cambio de documentación correspondiente. Cualquier adopción futura
requerirá un cambio OpenSpec independiente, revisión de Abel y pruebas del
frontend real.

## Open Questions

- Qué tokens concretos de color, tipografía y espaciado de la identidad actual
  debe preservar la versión integrada, si se aprueba.
- Si el progreso por pasos refleja rutas reales o solo el estado del formulario.
- Qué densidad de información lateral funciona mejor en móvil.
- Qué partes de la propuesta tienen prioridad frente a mejoras ya planificadas
  por el responsable de frontend/UX.
