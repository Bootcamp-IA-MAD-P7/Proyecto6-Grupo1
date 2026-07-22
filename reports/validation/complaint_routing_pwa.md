# Validación de la React PWA con mock

- Fecha: `2026-07-22`
- Spec: `003-complaint-routing-experience`
- Tarea: `T-006`
- Alcance: interfaz y PWA contra respuesta sintética; sin backend ni modelo

## Resultado

La interfaz implementa el formulario de narrativa, estados de validación, conexión y servicio, resultado simulado, confianza opcional, revisión humana, alternativas y trazabilidad. El modo mock permanece visible en cabecera, resultado y versión de modelo.

## Verificación automatizada

| Comprobación | Resultado |
|---|---|
| `npm run typecheck` | Correcta |
| `npm run lint` | Correcta, incluidas reglas `jsx-a11y` |
| `npm test` | 5 tests correctos |
| `npm run build` | Correcta; manifest y service worker generados |
| `npm audit` durante instalación | 0 vulnerabilidades conocidas |
| `python -m unittest discover -s tests -v` | 28 tests Python y de contrato correctos |

Los tests cubren formulario accesible, rechazo de texto vacío, resultado sintético, confianza nula, revisión obligatoria, ausencia de eco de la narrativa, modo offline y error seguro del servicio.

## Verificación en navegador

La compilación de producción se sirvió localmente y se inspeccionó mediante el árbol accesible:

- los títulos, regiones, formulario, textarea y botones tienen nombres identificables;
- el flujo de ejemplo sintético llega al resultado esperado;
- el foco pasa al título del resultado;
- el resultado comunica que es simulado, que no hay confianza calibrada y que una persona debe revisarlo;
- no se muestra la narrativa enviada ni una cola operativa.

La comprobación automatizada del viewport móvil no respetó el ancho solicitado en el navegador de validación. Existen breakpoints a `850 px` y `560 px`, controles táctiles y diseño de una columna, pero la revisión visual manual en móvil, tablet y escritorio continúa pendiente antes de cerrar toda la evidencia responsive de la spec.

## Privacidad y seguridad

- El mock no registra, devuelve ni persiste la narrativa.
- La narrativa se borra del estado visible al recibir el resultado.
- Los errores no exponen el mensaje interno ni el body de la petición.
- El service worker precachea recursos estáticos y excluye `/api/` del fallback de navegación.
- No existe caché runtime de peticiones o respuestas de inferencia.

## Límites

Este resultado valida una experiencia y un contrato. No demuestra precisión, inferencia real, funcionamiento offline del modelo, autenticación, despliegue ni aceptación por una persona usuaria de negocio.
