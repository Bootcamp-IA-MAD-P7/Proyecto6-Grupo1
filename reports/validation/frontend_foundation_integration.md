# Validación de la integración frontend

## Estado del informe

| Campo | Valor |
|---|---|
| Cambio OpenSpec | `integrate-frontend-foundation` |
| Jira | `PG-4` |
| Rama | `feature/PG-4-integrate-frontend-foundation` |
| Línea base automática | `6ffb47803032834a16321d8c1f67a032c66de094` |
| Commit de partida para la revisión manual | `cc323215ea5ee16ae792d345df7b38748bc85504` |
| Fecha | `2026-07-24` |
| Estado automático | Correcto |
| Estado de revisión | Tareas 9.2 a 10.3 correctas |

Este informe reúne la evidencia automática de la tarea 9.1 y la revisión manual
de accesibilidad y responsive de la tarea 9.2, además de la verificación de
instalación, actualización, offline, dictado, permisos y privacidad de la tarea
9.3, la revisión final de alcance y repositorio de la tarea 9.4 y el cierre
documental reproducible de las tareas 10.1 y 10.2.

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
| Chrome verificado | `150.0.7871.129` |
| Edge secundario no verificado | `150.0.4078.83` |
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

## Revisión de UX y accesibilidad — tarea 9.2

La revisión se realizó sobre el build de producción servido mediante
`npm run preview -- --host 127.0.0.1` y Chrome
`150.0.7871.129`. Solo se utilizó el ejemplo sintético incorporado en la
interfaz.

### Hallazgos y correcciones

La primera inspección detectó cuatro problemas que no impedían compilar, pero
sí reducían la calidad de la experiencia:

1. La página de clasificación no tenía un encabezado principal de nivel uno y
   el nombre del producto se exponía como un encabezado de nivel dos.
2. A `390 px`, el navegador ampliaba el viewport de diseño hasta `540 px` y
   reducía visualmente toda la aplicación para hacer caber el menú lateral.
3. El dorado original tenía un contraste de `1.55:1` sobre el fondo de papel y
   se utilizaba en texto informativo pequeño.
4. La preferencia de movimiento reducido anulaba las transiciones, pero no
   detenía la animación de pulso.

Se corrigieron la jerarquía de encabezados, la estructura responsive de los
layouts público y administrativo, el reflujo de controles, contadores y
etiquetas, el foco visible de la navegación, el color de texto dorado y la
política de movimiento reducido. El flujo conserva las mismas capacidades y
no añade backend, inferencia ni persistencia.

### Matriz de escenarios

| ID | Escenario | Navegador y viewport | Resultado |
|---|---|---|---|
| UX-01 | Formulario en escritorio | Chrome 150, `1440 × 900` | Correcto; una sola región principal, sin recorte ni scroll horizontal |
| UX-02 | Formulario en tablet vertical | Chrome 150, `768 × 1024` | Correcto; controles legibles, textarea y acciones dentro del viewport |
| UX-03 | Formulario en móvil | Chrome 150, `390 × 844` | Correcto; viewport real de `390 px`, navegación reubicada arriba y sin reducción global ni desbordamiento |
| UX-04 | Orden de teclado y foco visible | Chrome 150, escritorio | Correcto; `Home` → `Classify` → login mock → ejemplo sintético → narrativa → dictado → envío, con indicador visible |
| UX-05 | Validación de narrativa vacía | Chrome 150, escritorio | Correcto; el foco vuelve al textarea, `aria-invalid` pasa a `true` y el error queda enlazado mediante `aria-describedby` |
| UX-06 | Carga y aparición del resultado | Chrome 150, escritorio | Correcto; formulario con `aria-busy`, anuncio `role="status"`, controles bloqueados y foco trasladado al `h1` del resultado |
| UX-07 | Revisión del resultado en móvil | Chrome 150, `390 × 844` | Correcto; resultado sin porcentaje inventado, revisión humana textual y sin desbordamiento horizontal |
| UX-08 | Contraste de los tokens de texto | Cálculo WCAG sobre colores renderizados | Correcto; todos los pares de texto revisados superan `4.5:1` |
| UX-09 | Preferencia de movimiento reducido | Chrome 150, `prefers-reduced-motion: reduce` | Correcto; scroll automático, transiciones de `0.01 ms`, animaciones de `0.01 ms` y una sola iteración |

### Contraste verificado

| Uso | Primer plano | Fondo | Ratio |
|---|---|---|---|
| Texto principal | `#17322e` | `#fffdf7` | `13.47:1` |
| Texto secundario | `#49615d` | `#fffdf7` | `6.55:1` |
| Texto de acento corregido | `#6b5200` | `#fffdf7` | `7.29:1` |
| Avisos de revisión | `#a6472f` | `#fffdf7` | `5.79:1` |
| Navegación | `#ffffff` | `#102925` | `15.37:1` |

### Capturas sin datos sensibles

- [Móvil — 390 × 844](./screenshots/PG-4/frontend-foundation-mobile-390x844.png)
- [Tablet — 768 × 1024](./screenshots/PG-4/frontend-foundation-tablet-768x1024.png)
- [Escritorio — 1440 × 900](./screenshots/PG-4/frontend-foundation-desktop-1440x900.png)
- [Foco de teclado en escritorio](./screenshots/PG-4/frontend-foundation-keyboard-focus-1440x900.png)

### Regresión posterior a las correcciones

```bash
cd app/interface
npm run format
npm run typecheck
npm run lint
npm run format:check
npm test -- --run
npm run build
```

Todos los comandos finalizaron correctamente. La batería conserva `4`
archivos y `29` tests aprobados; el build transforma `123` módulos y el service
worker mantiene `8` entradas de precaché.

## PWA, dictado y privacidad — tarea 9.3

La matriz mínima de demostración de esta entrega se limita a Chrome
`150.0.7871.129` sobre Windows. Edge `150.0.4078.83` está instalado y se
registra como navegador Chromium secundario, pero no se presenta como
verificado porque no se completó en él la misma revisión manual.

### Hallazgos y correcciones

La revisión identificó dos mejoras necesarias antes de considerar verificable
la instalación y la actualización:

1. El manifest solo ofrecía un icono SVG. Se añadieron iconos PNG de
   `192 × 192` y `512 × 512`, más un recurso maskable de `512 × 512`, y se
   conservó el SVG como formato escalable. El recurso maskable mantiene un fondo
   completo para tolerar el recorte del sistema.
2. El service worker utilizaba un nombre de caché fijo. Aunque el worker podía
   actualizarse, recursos con hash de builds anteriores podían permanecer en
   la misma caché. El nombre se deriva ahora de manera determinista del manifest
   de precaché; una versión con contenido diferente obtiene otra caché y la fase
   de activación elimina las anteriores.

La selección de tamaños rasterizados sigue la recomendación de Chromium de
ofrecer recursos de `192 × 192` y `512 × 512`, manteniendo el SVG como formato
adicional y no como único recurso:
<https://web.dev/articles/add-manifest>.

### Matriz de escenarios

| ID | Escenario | Evidencia | Resultado |
|---|---|---|---|
| PWA-01 | Manifest y recursos de instalación | Build de producción y revisión de `manifest.webmanifest` | Correcto; nombre, `start_url`, `scope`, modo `standalone`, colores e iconos PNG, maskable y SVG presentes |
| PWA-02 | Instalación en Chrome | Revisión humana sobre `127.0.0.1` | Correcto; Chrome ofreció instalar `Complaint Routing Workspace` y la abrió en una ventana independiente |
| PWA-03 | Actualización del worker | `registerType: autoUpdate`, caché versionada por contenido y tests de regresión | Correcto; un build distinto obtiene una caché distinta y la activación elimina cachés anteriores |
| PWA-04 | Recarga offline | Revisión manual registrada en 6.2 sobre el build de producción | Correcto; el shell completo vuelve a abrirse desde caché y muestra el estado offline |
| PWA-05 | Clasificación sin servicio | Revisión manual y tests de conectividad | Correcto; el botón queda deshabilitado y no aparece resultado mock ni real |
| VOICE-01 | Dictado soportado y autorizado | Chrome 150 con permiso real concedido | Correcto; la acción explícita activa el dictado y el texto sintético aparece editable en la narrativa |
| VOICE-02 | Dictado no soportado | Test con Web Speech API ausente | Correcto; no aparece la acción de dictado, el fallback se explica y el teclado sigue disponible |
| VOICE-03 | Permiso denegado | Test con error `not-allowed` | Correcto; la escucha se detiene, aparece un mensaje seguro y el teclado continúa disponible |
| VOICE-04 | Error del proveedor | Test con error de red sintético | Correcto; no se expone detalle interno y la entrada manual permanece operativa |
| PRIV-01 | Narrativa fuera de almacenamiento y telemetría | Test con spies de Storage, Cache Storage, URL y consola | Correcto; no hay escrituras, cambios de URL ni logs con el texto |
| PRIV-02 | Caché limitada a recursos estáticos | Política, build y revisión de Cache Storage de 6.2 | Correcto; API, sonda de conectividad, escrituras, datos y orígenes externos permanecen `network-only` |

### Comprobaciones reproducibles posteriores

```bash
cd app/interface
npm run typecheck
npm run lint
npm run format:check
npm test -- --run
npm run build
```

Todos los comandos finalizaron correctamente. La batería aumenta a `31` tests
aprobados y el build PWA genera `14` entradas antes de la normalización interna
de URLs duplicadas. Los tres PNG tienen las dimensiones y el modo RGBA
esperados.

### Limitaciones conservadas

- No se probó la instalación y el dictado manual en Edge; sigue siendo un
  navegador secundario pendiente de evidencia.
- El permiso concedido se verificó con el navegador real. El permiso denegado y
  el navegador sin soporte se validaron mediante pruebas controladas para no
  presentar una combinación no observada como evidencia manual.
- El idioma del reconocimiento procede del documento o del navegador y no
  establece todavía una política de idioma del producto.
- La actualización se verificó en la mecánica del worker, el build y la caché;
  no representa todavía una estrategia de despliegue en producción.
- Instalar la PWA no añade backend, modelo, autenticación real ni inferencia.

## Seguridad de la evidencia

- No se utilizaron narrativas reales del CFPB.
- Los tests usan únicamente fixtures sintéticos.
- No se generaron logs, capturas ni artefactos con datos personales.
- `node_modules` y `dist` permanecen fuera de Git.
- No se ejecutó backend, entrenamiento ni servicio de inferencia.

## Revisión final de repositorio — tarea 9.4

La rama se actualizó sobre `origin/dev` después de que el trabajo de datos y EDA
añadiera dos commits a la base. El rebase terminó sin conflictos y mantuvo los
cincuenta y ocho commits propios y la autoría de Abel y Miguel.

| Comprobación | Resultado |
|---|---|
| Base vigente | `origin/dev` en `12092f68d8eb6d83da409b22d03c602eec362df6` |
| Relación con la base | `0` commits pendientes de `dev`; `58` commits propios |
| Quality gate | Correcto; `302` archivos versionados y `314` locales revisados |
| Whitespace | Correcto; `git diff --check` sin salida |
| Entradas sin fusionar | `0` |
| Simulación de integración | Correcta; `git merge-tree --write-tree` finalizó con código `0` |
| Diferencia frente a `dev` | `72` rutas añadidas y limitadas a PG-4 |
| Rutas inesperadas | `0` |
| Archivos de datos o secretos por ruta | `0` |
| Archivos de texto inspeccionados | `61` |
| Patrones de secretos | `0` |
| Marcadores de conflicto | `0` |
| Referencias al campo bruto del CFPB | `0` |
| OpenSpec estricto | Correcto |

Las rutas revisadas pertenecen exclusivamente a:

- `app/interface/`;
- `openspec/changes/integrate-frontend-foundation/`;
- los informes `frontend_foundation_*`;
- las capturas sintéticas de `reports/validation/screenshots/PG-4/`.

No se añadieron CSV, Parquet, JSONL, bases de datos, variables de entorno,
modelos, narrativas CFPB reales ni otros artefactos de datos. Los textos de
prueba y demostración permanecen identificados como sintéticos, mock o
propuesta.

## Cierre documental — tareas 10.1 y 10.2

El manual `app/interface/README.md` permite instalar, ejecutar, probar y revisar
el prototipo sin conocimiento previo de la integración. También documenta sus
rutas, contrato, dictado, política offline, privacidad, compatibilidad y
limitaciones. `app/interface/.gitattributes` fija LF en los archivos web para
que el control de formato sea reproducible en Windows.

La documentación global adopta una única formulación:

- existe una React PWA prototipo validada con contenido sintético;
- la entrega permanece en su rama, pendiente de revisión humana y merge;
- no existe backend, modelo entrenado ni inferencia real;
- el modo offline conserva el shell, pero bloquea la clasificación;
- login, administración, entrenamiento y registro de modelos son propuestas;
- `ESS-04` continúa sin verificar.

Se actualizaron únicamente el resumen y las referencias del README, el
changelog y las fuentes de NotebookLM cuyo significado había cambiado. El
paquete del `2026-07-24` incorpora este informe de forma automática desde
`reports/**/*.md` y no contiene narrativas reales.

## Revisión humana con Abel — tarea 10.3

El 24 de julio de 2026, Abel confirmó que:

- su trabajo frontend se ha conservado;
- la atribución es correcta;
- las adaptaciones respetan el objetivo original;
- los mocks y las capacidades propuestas no se presentan como capacidades
  reales.

La comprobación del historial anterior a registrar esta evidencia produjo:

| Evidencia | Resultado |
|---|---|
| Rama original de Abel | Intacta en `70cf2d9479047eefad07b02f05b3b64467b77fd9` |
| Commit revisado de integración | `46b86034d4a325c726585134b7b986ba95a67447` |
| Commits frontend atribuidos a Abel | `30` |
| Commits frontend o de integración atribuidos a Miguel | `17` |
| Validación estricta OpenSpec | Correcta |
| Conversaciones de Pull Request | No existen todavía; la PR no se ha publicado |

La confirmación cierra la revisión de autoría y alcance, pero no autoriza por sí
sola el archivo, `push`, Pull Request o merge. Esas acciones permanecen
condicionadas a las tareas 10.4 y 10.5.

## Borrador de Pull Request — tarea 10.4

El cuerpo completo de la Pull Request se preparó localmente en
`exports/pr-bodies/integrate-frontend-foundation.md` a partir de la plantilla
del repositorio. El directorio `exports/` permanece ignorado por Git, por lo que
el borrador no se incorpora a la entrega y puede utilizarse directamente con
`gh pr create --body-file` después de la autorización humana.

El borrador enlaza `PG-4`, el cambio OpenSpec, la delta spec, las tareas, los dos
informes de validación, el manual, el contrato y las capturas sintéticas. También
incluye:

  - 79 rutas modificadas en el instante de preparación;
  - 62 commits propios respecto de `dev` en ese mismo instante;
  - 30 commits atribuidos a Abel y 32 a Miguel antes del commit de esta
    evidencia;
- 31 tests frontend correctos;
- build React y PWA correctos;
- auditoría con cero vulnerabilidades;
- riesgos, límites y rollback.

La rama quedó actualizada respecto de `origin/dev` con relación `0 62` en el
instante de preparación; el quality gate, `git diff --check`, OpenSpec estricto
y la simulación de integración terminaron correctamente. El arnés generó el
paquete de verificación acotado a `PG-4`. Los recuentos se volverán a calcular
antes de publicar porque los commits de cierre todavía son locales.

## Verificaciones pendientes

- Tarea 10.5: solicitar aprobación antes de archivar o publicar.
