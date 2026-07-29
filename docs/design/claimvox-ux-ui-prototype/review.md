# Revisión de la propuesta UX/UI

## Estado de la evidencia

Esta revisión cubre el código estático, el alcance y los requisitos de la
propuesta. No sustituye una prueba de la React PWA ni acredita una funcionalidad
de producto. No se añaden capturas automáticas porque el entorno de revisión no
dispone de un navegador controlable; la validación visual queda preparada como
revisión humana al abrir `index.html`.

## Recorrido manual previsto

1. Abrir `index.html` en escritorio y comprobar barra lateral, progreso, campo,
   acción primaria, panel de revisión y consejo.
2. Reducir el ancho a tableta y móvil: la navegación pasa a una fila, el panel
   lateral se apila y las acciones ocupan todo el ancho.
3. Navegar con la tecla Tab: enlace de salto, navegación, ayuda, campo,
   dictado, acción principal y controles de ejemplo muestran foco visible.
4. Escribir texto sintético y usar **Obtener orientación**: aparece únicamente
   una respuesta mock de demostración, con revisión humana requerida.
5. Usar **Dictado opcional**: el aviso confirma que es conceptual y que no se
   solicita permiso ni se procesa audio.

## Diferencias frente a ClaimVox integrado

| Propuesta aislada | Aplicación integrada |
|---|---|
| HTML, CSS y JavaScript estáticos | React PWA en `app/interface/` |
| No inicia API ni modelo | Puede usar mock o API local configurada |
| Resultado siempre mock de demostración | Distingue mock y predicción local según configuración |
| Progreso por cuatro pasos conceptual | Flujo funcional vigente y sus estados ya verificados |
| Sin persistencia ni permisos | Mantiene los límites de privacidad de la aplicación |

## Elementos candidatos para una integración futura

- Jerarquía de progreso y señalización del paso actual.
- Agrupación visual de narrativa, dictado, acción y explicación de límites.
- Panel persistente de revisión humana.
- Consejo contextual desplegable.
- Adaptación de la navegación lateral a pantallas reducidas.

## Decisiones pendientes de frontend/UX

- Seleccionar qué tokens de la identidad ClaimVox actual se reutilizan.
- Decidir si los pasos son una guía de una sola vista o estados reales.
- Validar contraste, lectura con tecnología de asistencia y responsive en la
  PWA real.
- Planificar un cambio OpenSpec separado si se aprueba modificar
  `app/interface/`.
