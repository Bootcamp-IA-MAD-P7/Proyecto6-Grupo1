# Prototipo UX/UI aislado de ClaimVox

> Estado: propuesta visual no integrada. No modifica ni sustituye la React PWA
> de `app/interface/`; no usa API, modelo, datos CFPB, autenticación ni
> persistencia.

## Abrir la maqueta

Abra `index.html` con un navegador. No requiere instalar dependencias ni iniciar
el backend. Todo el contenido es sintético y demostrativo.

## Qué explora

- Navegación lateral orientada al recorrido de orientación.
- Progreso visible: describir, revisar, orientación y siguiente paso.
- Campo de narrativa con aviso de privacidad y dictado conceptual opcional.
- Acción primaria y respuesta mock explícita.
- Panel persistente de revisión humana y ayuda contextual.

## Límites

- El botón de orientación no realiza una predicción ni guarda el texto.
- El botón de dictado no solicita permisos ni captura audio.
- El selector de modo es informativo: el prototipo no contacta una API local.
- La propuesta no acredita ninguna capacidad adicional de entrega.

## Decisiones pendientes antes de integrar

1. Confirmar con Abel qué tokens de ClaimVox se conservarían o evolucionarían.
2. Validar si los cuatro pasos reflejan estados reales del flujo o una ayuda
   visual sobre el formulario actual.
3. Diseñar y probar en la PWA real los estados de error, offline, carga y
   accesibilidad con tecnologías de asistencia.
4. Aprobar un cambio OpenSpec nuevo antes de modificar `app/interface/`.
