# SPEC: Experiencia de clasificación de reclamaciones

- ID: `003`
- Estado: `in_progress`
- Responsables: `Abel / frontend y UX`; `Miguel / arquitectura`; `José / futura integración backend`
- Fecha: `2026-07-22`

## Contexto y problema

El producto pretende ayudar a personal de operaciones o atención a clasificar una reclamación financiera escrita dentro de once familias CFPB. React PWA está aprobado como dirección frontend; existe una interfaz funcional contra mock en la PR `#14`, pero todavía no hay modelo entrenado, backend ni usuario B2B validado.

El equipo necesita un contrato que permita diseñar y construir la interfaz con respuestas simuladas sin inventar métricas, umbrales o capacidades del futuro modelo.

## Usuario y necesidad

El usuario principal propuesto es una persona que recibe una reclamación y debe decidir qué familia financiera debe revisarla. La predicción actúa como apoyo: la persona conserva la decisión y puede solicitar revisión.

Esta definición es una hipótesis de producto pendiente de contraste con una persona usuaria o responsable de negocio.

## Objetivo observable

Definir e implementar una experiencia React PWA contra un contrato de inferencia simulable que acepte una narrativa, devuelva una de las once clases y represente incertidumbre, revisión y errores de forma accesible y segura.

## Alcance

### Incluido

- Flujo de introducción, envío, carga, resultado y nueva clasificación.
- Clase predicha, alternativas, confianza opcional y necesidad de revisión.
- Estados vacío, inválido, offline, error, servicio no disponible y resultado.
- Contrato OpenAPI versionado para mocks y futura integración.
- React PWA con cliente sustituible y modo mock explícito.
- Privacidad por defecto y prohibición de registrar o devolver la narrativa.
- Reglas responsive, accesibilidad y lenguaje de apoyo a la decisión.
- Endurecimiento de la entrega frontend: instalabilidad PWA, revisión visual por viewport, evidencias seguras y monitorización de dependencias npm.

### Fuera de alcance

- Implementar backend, servicio de inferencia o conexión a un modelo real.
- Definir umbral de confianza, longitud máxima o idioma aceptado sin evidencia.
- Recomendar una cola o departamento no validado con negocio.
- Persistir narrativas, historial o feedback.
- Autenticación, roles y permisos definitivos.
- Registro de usuarios, dashboard administrativo, KPIs o panel de entrenamiento.
- Dictado por voz, transcripción local o descarga de modelos en el navegador.
- Adoptar routing, estado de servidor o una nueva librería visual sin una necesidad aprobada.
- Entrenar, seleccionar o desplegar un modelo.

## Flujo principal

1. La persona accede al espacio de clasificación.
2. La aplicación explica finalidad, límites y tratamiento de datos.
3. La persona introduce una narrativa sin identificadores personales.
4. La interfaz valida que exista texto y que haya conexión con el servicio.
5. La aplicación envía únicamente la narrativa y un identificador técnico opcional.
6. El resultado muestra familia predicha, alternativas y versión del modelo.
7. Si falta confianza calibrada o el servicio indica revisión, el resultado lo comunica sin fingir certeza.
8. La persona decide cómo continuar y puede iniciar una nueva clasificación.

## Requisitos

- R-001: La entrada de negocio será una única narrativa de texto no vacía.
- R-002: La interfaz advertirá que no deben incluirse datos personales innecesarios.
- R-003: La respuesta utilizará exclusivamente las once clases de `config/cfpb_target_contract.json`.
- R-004: La confianza será opcional y solo se mostrará como confianza del modelo cuando esté calibrada.
- R-005: La respuesta incluirá `review_required`; si la confianza es nula deberá ser `true`.
- R-006: La interfaz no presentará la predicción como decisión final ni acción financiera.
- R-007: La narrativa no aparecerá en la respuesta, logs, historial o almacenamiento por defecto.
- R-008: La PWA podrá cargar su shell offline, pero no simulará una predicción real sin servicio.
- R-009: El contrato reservará errores de validación, límite, indisponibilidad y frecuencia sin fijar todavía políticas no aprobadas.
- R-010: La experiencia funcionará mediante teclado, etiquetas accesibles, foco visible, mensajes textuales y diseño responsive.
- R-011: La API devolverá versión de modelo y taxonomía para trazabilidad.
- R-012: La primera versión no incluirá endpoint de feedback ni mapping automático a colas.
- R-013: La entrega frontend registrará evidencia reproducible de instalabilidad, teclado y comportamiento responsive antes de considerarse preparada para revisión final.
- R-014: Las dependencias npm de `app/interface/` tendrán instalación reproducible y monitorización automatizada.

## Criterios de aceptación

- AC-001: Dada una narrativa válida y un mock correcto, cuando finaliza la petición, entonces se muestra una clase canónica, trazabilidad y estado de revisión.
- AC-002: Dada confianza nula, cuando se presenta el resultado, entonces se solicita revisión y no se muestra un porcentaje inventado.
- AC-003: Dada ausencia de conexión, cuando se intenta clasificar, entonces la PWA informa que el servicio es necesario y no fabrica un resultado.
- AC-004: Dada una respuesta o error, cuando se inspecciona, entonces no contiene la narrativa enviada.
- AC-005: Dada una clase fuera del contrato CFPB, cuando se valida el OpenAPI, entonces la comprobación falla.
- AC-006: Dado cualquier estado, cuando se utiliza teclado o lector de pantalla, entonces el estado y la acción disponible son identificables sin depender solo del color.
- AC-007: Dado el contrato actual, cuando se revisan sus rutas, entonces no existe feedback ni recomendación de cola.
- AC-008: Dados los viewports acordados, cuando se revisa manualmente la interfaz, entonces el formulario, resultado, errores y acciones permanecen legibles y operables, con capturas sintéticas como evidencia.
- AC-009: Dada la compilación de producción, cuando se inspecciona la PWA, entonces existen manifest, service worker e iconos adecuados, y Dependabot reconoce el ecosistema npm de la interfaz.

## Preguntas abiertas

- [ ] Q-001: ¿El flujo operativo propuesto coincide con el trabajo real del usuario B2B?
- [ ] Q-002: ¿Qué idioma o idiomas aceptará la primera versión?
- [ ] Q-003: ¿Qué tamaño máximo admite el servicio sin degradar UX u operación?
- [ ] Q-004: ¿Qué métrica calibrada y umbral activarán `review_required`?
- [ ] Q-005: ¿Se necesita autenticación para la demo y para un despliegue posterior?
- [ ] Q-006: ¿Qué mapping de producto a cola tiene significado para el usuario?

## Evidencia de cierre esperada

- Revisión de flujo con una persona usuaria o responsable de negocio.
- OpenAPI y mocks consumidos por la PWA.
- Tests de contrato entre interfaz y servicio.
- Evidencia de teclado, responsive, accesibilidad y estados.
- Evidencia de instalabilidad, recursos PWA, dependencias y revisión visual con contenido sintético.
- Decisiones de privacidad, idioma, límites y revisión sincronizadas.
