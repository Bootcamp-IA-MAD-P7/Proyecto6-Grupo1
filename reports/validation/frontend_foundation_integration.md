# Validación de la integración frontend

## Estado del informe

| Campo | Valor |
|---|---|
| Cambio OpenSpec | `integrate-frontend-foundation` |
| Jira | `PG-4` |
| Rama | `feature/PG-4-integrate-frontend-foundation` |
| Commit verificado | `62b0dbae55fbb6a8d19480e351e680c048483c53` |
| Fecha | `2026-07-24` |
| Estado automático | Correcto |
| Estado manual | Pendiente de las tareas 9.2 y 9.3 |

Este informe comienza con la evidencia automática de la tarea 9.1. Se ampliará
con las verificaciones manuales de accesibilidad, responsive, PWA, dictado y
privacidad antes de considerarlo definitivo.

La entrega validada es una interfaz React PWA con respuestas sintéticas. Todavía
no existe backend, modelo entrenado ni inferencia real, por lo que esta evidencia
no permite marcar `ESS-04` como verificado.

## Entorno reproducible

| Componente | Versión o referencia |
|---|---|
| Sistema operativo | Windows |
| Node.js | `24.18.0` |
| npm | `11.16.0` |
| Vitest | `4.1.10` |
| Vite | `6.4.3` |
| Hash Git del lockfile | `ff078583c3aa9d4a5a5d320b9b9d777414bc9df0` |

## Batería automática — tarea 9.1

La instalación se reconstruyó desde cero mediante `npm ci` antes de ejecutar
ningún control:

```bash
cd app/interface
npm ci
npm run typecheck
npm run lint
npm run format:check
npm test -- --run
npm run build
npm audit --audit-level=high
```

| Comprobación | Resultado |
|---|---|
| Instalación limpia | Correcta; `575` paquetes instalados |
| Auditoría durante la instalación | `0` vulnerabilidades |
| TypeScript | Correcto |
| ESLint | Correcto; sin errores ni avisos |
| Prettier | Correcto; todos los archivos cumplen el formato |
| Tests | `4` archivos y `29` tests aprobados |
| Build React | Correcto; `123` módulos transformados |
| Build service worker | Correcto |
| Precache PWA | `8` entradas, `338.26 KiB` |
| Auditoría final con umbral alto | Correcta; `0` vulnerabilidades |

La instalación comunica deprecaciones en dos paquetes transitivos de desarrollo.
No producen vulnerabilidades en la auditoría y su actualización no se fuerza
dentro de este cambio.

## Seguridad de la evidencia

- No se utilizaron narrativas reales del CFPB.
- Los tests usan únicamente fixtures sintéticos.
- No se generaron logs, capturas ni artefactos con datos personales.
- `node_modules` y `dist` permanecen fuera de Git.
- No se ejecutó backend, entrenamiento ni servicio de inferencia.

## Verificaciones pendientes

- Tarea 9.2: teclado, foco, anuncios, contraste, movimiento reducido y
  responsive.
- Tarea 9.3: instalación y actualización PWA, offline, dictado, permisos y
  privacidad.
- Tarea 9.4: revisión final del alcance y quality gates del repositorio.
