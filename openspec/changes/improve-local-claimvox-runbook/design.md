## Context

ClaimVox ofrece dos recorridos locales distintos: la demostración mock por
defecto y la inferencia local mediante FastAPI y un artefacto reproducible. La
documentación existente describe ambos, pero reparte los pasos entre varias
guías, mezcla shells y no establece una comprobación mínima que permita saber
si se ha cargado el modo real.

## Goals / Non-Goals

**Goals:**

- Proporcionar una secuencia de arranque corta, específica para Git Bash en
  Windows y enlazada desde el README.
- Separar el recorrido mock seguro del recorrido local real, incluyendo la
  respuesta esperada de salud y el significado del resultado.
- Mantener el detalle técnico en los manuales de frontend y backend, evitando
  repetirlo en cada documento.
- Revisar las fuentes de comunicación afectadas para preservar una única fuente
  de verdad y el carácter local del MVP.

**Non-Goals:**

- No añadir Docker, cloud, autenticación, persistencia, logging de usuarios,
  cambios de React, FastAPI, modelos ni dependencias.
- No convertir el procedimiento local en una afirmación de despliegue ni
  incorporar datos, narrativas o artefactos locales a Git.

## Decisions

### Un runbook de referencia y enlaces, no instrucciones duplicadas

La guía esencial será la referencia operativa. README, manual de frontend y
manual de backend enlazarán a ella y conservarán solo el contexto propio de su
área. Esto reduce contradicciones entre puertos, rutas y variables.

Alternativa considerada: repetir todos los comandos en cada README. Se descarta
porque ya ha provocado divergencias de shell y de nombre de artefacto.

### Git Bash como recorrido principal de Windows

El runbook usará comandos compatibles con la terminal que utiliza el equipo:
`export` para variables y rutas `/c/...`. Se añadirá una equivalencia breve para
PowerShell cuando sea útil, sin mezclar ambas sintaxis en el mismo bloque.

### Verificación explícita y segura

La comprobación de modo real será `GET /api/v1/health`: `ok` confirma que el
predictor local está disponible y `degraded` que el backend usa el fallback
mock. La prueba de interfaz seguirá usando solo el ejemplo sintético incluido.

La PWA puede conservar recursos de un build anterior durante desarrollo. La
guía indicará usar una ventana de incógnito como primer diagnóstico sencillo;
la eliminación de datos de sitio quedará como procedimiento avanzado enlazado
desde el manual del frontend.

## Risks / Trade-offs

- [El artefacto local no existe] → el health responde `degraded`; la guía no lo
  oculta y remite a la reconstrucción reproducible.
- [Puerto ocupado por un proceso anterior] → el runbook explica que se reutilice
  el proceso que responde o se cierre solo el proceso local identificado.
- [Una PWA cachea una versión anterior] → ventana de incógnito antes de acciones
  de DevTools más complejas.
- [Documentación futura divergente] → README enlaza al runbook y la fuente de
  estado continúa siendo `delivery_levels.md`.
