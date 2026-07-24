# Complaint Routing Interface

React PWA para introducir una reclamación escrita y revisar una recomendación de
clasificación. Esta entrega corresponde a Jira `PG-4` y al cambio OpenSpec
[`integrate-frontend-foundation`](../../openspec/changes/integrate-frontend-foundation/).

## Estado real

| Capacidad                         | Estado                                                        |
| --------------------------------- | ------------------------------------------------------------- |
| Formulario de reclamación         | Implementado y verificado con texto sintético                 |
| Contrato TypeScript               | Implementado y alineado con OpenAPI                           |
| Recomendación                     | Mock; no procede de un modelo                                 |
| Revisión humana                   | Representada en la interfaz                                   |
| Dictado                           | Implementado mediante Web Speech API con fallback por teclado |
| PWA instalable                    | Verificada manualmente en Chrome sobre Windows                |
| Shell offline                     | Implementado; no clasifica sin conexión                       |
| Autenticación y administración    | Propuestas mock; no aportan seguridad ni operaciones reales   |
| Backend, modelo e inferencia real | No implementados                                              |

Esta interfaz avanza el requisito `ESS-04`, pero no permite marcarlo como
verificado hasta que exista una predicción real extremo a extremo.

## Arranque en cinco minutos

Requisitos:

- Node.js `20` o posterior;
- npm;
- repositorio actualizado y situado en la rama de trabajo correspondiente.

Desde la raíz del repositorio:

```bash
cd app/interface
npm ci
npm run dev
```

Vite mostrará la dirección local de desarrollo, normalmente
<http://localhost:5173>.

Para revisar el build de producción y el comportamiento PWA:

```bash
npm run build
npm run preview -- --host 127.0.0.1
```

La dirección utilizada en la validación es <http://127.0.0.1:4173>. La
instalación, el service worker y el modo offline deben comprobarse sobre este
build, no solo sobre el servidor de desarrollo.

## Recorrido disponible

### Flujo público

1. Abrir `/classify`.
2. Escribir una narrativa sintética o pulsar `Use a synthetic example`.
3. Revisar que el texto no contiene nombres, cuentas, direcciones ni otros datos
   personales innecesarios.
4. Pulsar `Classify complaint`.
5. Revisar la respuesta marcada como `Mock response · demo only`.
6. Confirmar que no aparece una confianza inventada y que se exige revisión
   humana.
7. Pulsar `Start a new classification` para volver a un formulario vacío.

La respuesta actual es fija y sintética. No se consulta el CSV, no existe
backend y no se ejecuta ningún modelo.

### Rutas

| Ruta              | Propósito                           |
| ----------------- | ----------------------------------- |
| `/`               | Resumen público del prototipo       |
| `/classify`       | Formulario y recomendación mock     |
| `/login`          | Propuesta de autenticación ficticia |
| `/admin`          | Concepto de panel administrativo    |
| `/admin/training` | Concepto de flujo de entrenamiento  |
| `/admin/models`   | Concepto de registro de modelos     |

Las rutas administrativas solo pueden revisarse con la identidad sintética
`carlos@example.com`. La propuesta de usuario utiliza `ana@example.com`.
Cualquier contraseña es aceptada porque no existe autenticación real. Estas
pantallas no proporcionan identidad, autorización, permisos, datos operativos,
entrenamiento ni registro de modelos.

## Contrato de predicción

La vista depende de `PredictionClient`, no de una implementación de transporte
concreta. Los tipos y validaciones en
[`src/contracts/prediction.ts`](src/contracts/prediction.ts) siguen
[`docs/api/openapi.json`](../../docs/api/openapi.json) y las once clases
versionadas en
[`config/cfpb_target_contract.json`](../../config/cfpb_target_contract.json).

La petición permite:

```ts
interface PredictionRequest {
  narrative: string
  client_request_id?: string
}
```

Reglas relevantes:

- `narrative` no puede estar vacía ni contener solo espacios;
- la interfaz envía la narrativa recortada;
- una respuesta con campos o clases desconocidas se rechaza;
- una respuesta sin confianza calibrada exige revisión humana;
- la narrativa no forma parte de la respuesta.

El cliente actual es
[`src/services/mock-prediction-client.ts`](src/services/mock-prediction-client.ts).
Para conectar un servicio real deberá añadirse otro `PredictionTransport` que
respete el mismo contrato. No es necesario acoplar la vista al backend ni acceder
directamente a datos de entrenamiento.

## Dictado por voz

El dictado es una ayuda opcional para rellenar el mismo campo de narrativa:

- solo comienza cuando la persona pulsa `Start dictation`;
- solicita permiso de micrófono mediante la Web Speech API del navegador;
- puede depender del navegador o de su proveedor para procesar el audio;
- inserta una transcripción editable que debe revisarse antes de enviarse;
- permite detener la escucha;
- mantiene la escritura por teclado cuando no hay soporte, se deniega el permiso
  o el proveedor falla;
- la aplicación no guarda audio ni transcripciones.

El idioma procede del documento o del navegador como configuración técnica. No
representa una política de idioma aprobada para el producto.

## PWA y funcionamiento offline

La PWA utiliza `vite-plugin-pwa`, estrategia `injectManifest` y un service worker
propio:

- precachea únicamente el shell y recursos estáticos del mismo origen;
- utiliza una caché versionada por el contenido del build;
- elimina cachés antiguas al activar una versión nueva;
- excluye `/api/`, escrituras, orígenes externos, sondas de conectividad y
  peticiones de datos;
- ofrece una página o shell de navegación cuando no hay red;
- deshabilita la clasificación si el servicio no está disponible;
- nunca fabrica ni recupera de caché una predicción.

Para una comprobación limpia desde Chrome:

1. abrir DevTools;
2. ir a `Application`;
3. revisar `Manifest`, `Service workers` y `Cache storage`;
4. recargar una vez con conexión;
5. activar `Offline` y recargar;
6. confirmar que el shell se muestra, aparece el aviso offline y la
   clasificación permanece bloqueada.

Si se han probado builds anteriores, conviene eliminar previamente los service
workers y datos del sitio desde `Application > Storage`.

## Privacidad y seguridad

- No utilizar narrativas reales del CFPB en desarrollo, pruebas, capturas,
  prompts, logs ni servicios externos.
- Los ejemplos y fixtures del repositorio son sintéticos.
- La narrativa se mantiene solo en memoria durante el flujo activo.
- La aplicación no escribe narrativas, audio o transcripciones en
  `localStorage`, `sessionStorage`, IndexedDB, Cache Storage, URL o consola.
- La caché contiene únicamente recursos estáticos.
- La propuesta de login sí guarda una identidad ficticia en `localStorage` para
  poder revisar sus pantallas. No es un control de seguridad.
- No existen secretos, tokens, credenciales reales ni conexión con sistemas de
  producción.

## Compatibilidad verificada

| Entorno                          | Evidencia                                                                        |
| -------------------------------- | -------------------------------------------------------------------------------- |
| Chrome `150.0.7871.129`, Windows | Flujo, responsive, instalación PWA, offline, permiso real de micrófono y dictado |
| Edge `150.0.4078.83`, Windows    | Registrado como navegador secundario; revisión manual pendiente                  |
| Navegador sin Web Speech API     | Cubierto mediante test; permanece el teclado                                     |
| Permiso de micrófono denegado    | Cubierto mediante test; se recupera el flujo por teclado                         |

La instalación PWA y Web Speech API dependen del navegador. La aplicación web y
la entrada por teclado no deben depender de esas capacidades opcionales.

## Scripts

Todos estos comandos se ejecutan desde `app/interface/`:

| Comando                               | Uso                                                |
| ------------------------------------- | -------------------------------------------------- |
| `npm ci`                              | Instalar exactamente el lockfile                   |
| `npm run dev`                         | Iniciar desarrollo con Vite                        |
| `npm run build`                       | Ejecutar typecheck y generar el build PWA          |
| `npm run preview -- --host 127.0.0.1` | Servir el build para revisión manual               |
| `npm run typecheck`                   | Validar TypeScript de React, Node y service worker |
| `npm run lint`                        | Ejecutar ESLint                                    |
| `npm run lint:fix`                    | Aplicar correcciones seguras de ESLint             |
| `npm run format`                      | Aplicar Prettier                                   |
| `npm run format:check`                | Comprobar formato sin modificar archivos           |
| `npm test -- --run`                   | Ejecutar la batería una vez                        |
| `npm run test:watch`                  | Ejecutar tests en modo interactivo                 |
| `npm audit --audit-level=high`        | Comprobar vulnerabilidades altas o críticas        |

Comprobación completa del frontend:

```bash
npm ci
npm run typecheck
npm run lint
npm run format:check
npm test -- --run
npm run build
npm audit --audit-level=high
```

Desde la raíz del repositorio:

```bash
python scripts/quality/check_repository.py
git diff --check
npm exec -- openspec validate integrate-frontend-foundation --type change --strict
```

## Estructura principal

```text
app/interface/
├── public/                 # iconos, manifest generado y fallback offline
├── src/
│   ├── components/         # componentes visuales y avisos
│   ├── contracts/          # contrato y validación de predicción
│   ├── hooks/              # conectividad, autenticación mock y dictado
│   ├── layouts/            # layouts público, mock y administrativo
│   ├── pages/              # clasificación y capacidades propuestas
│   ├── providers/          # contexto de sesión mock y consultas
│   ├── pwa/                # política de caché comprobable
│   ├── services/           # cliente de predicción y autenticación mock
│   └── sw.ts               # service worker
├── package.json
├── vite.config.ts
└── vitest.config.ts
```

## Limitaciones y próximos límites

- No existe backend, modelo entrenado, inferencia real ni confianza calibrada.
- No existe una cola operativa ni persistencia de reclamaciones o feedback.
- No existe autenticación, autorización ni administración real.
- Las pantallas de entrenamiento y modelos son conceptos no operativos.
- No se ha aprobado una política de idioma.
- Edge continúa pendiente de revisión manual equivalente.
- La PWA no ofrece clasificación offline.
- Las métricas del nivel esencial solo podrán presentarse cuando exista un
  modelo evaluado con evidencia reproducible.

La evidencia detallada está en
[`reports/validation/frontend_foundation_integration.md`](../../reports/validation/frontend_foundation_integration.md).
