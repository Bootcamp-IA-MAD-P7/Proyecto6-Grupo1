# ClaimVox Interface

React PWA para introducir una reclamación escrita y revisar una recomendación de
clasificación. Esta entrega corresponde a Jira `PG-4`, a la capacidad vigente
[`complaint-routing-interface`](../../openspec/specs/complaint-routing-interface/spec.md)
y al [expediente OpenSpec archivado](../../openspec/changes/archive/2026-07-24-integrate-frontend-foundation/).

## Estado real

| Capacidad                      | Estado                                                                              |
| ------------------------------ | ----------------------------------------------------------------------------------- |
| Formulario de reclamación      | Implementado y verificado con texto sintético                                       |
| Contrato TypeScript            | Implementado y alineado con OpenAPI                                                 |
| Recomendación                  | Solo API local real; sin configuración o con backend degradado no muestra categoría |
| Revisión humana                | Representada en la interfaz                                                         |
| Dictado                        | Implementado mediante Web Speech API con fallback por teclado                       |
| PWA instalable                 | Verificada manualmente en Chrome sobre Windows                                      |
| Shell offline                  | Implementado; no clasifica sin conexión                                             |
| Identidad y tema               | ClaimVox; preferencias claro, oscuro y sistema persistentes                         |
| Autenticación y administración | JWT demo por entorno; no aporta identidad ni autorización productiva                |
| Backend, modelo e inferencia   | Integración verificada; no hay Champion ni despliegue cloud acreditado              |
| Feedback                       | Registro minimizado y resumen agregado protegido por token                          |

La integración local de frontend, servicio y artefacto reproducible aporta la
evidencia de `ESS-04`. No equivale a identidad compartida, despliegue,
reclamaciones, observabilidad operativa ni a un modelo aprobado para producción.
La única persistencia implementada conserva metadatos cerrados de feedback en
SQLite local o PostgreSQL configurado y aplica retención finita.

## Servicio local opcional

ClaimVox conserva un cliente mock para pruebas aisladas, pero la interfaz no lo
usa para presentar una clasificación. La [guía local
canónica](../../docs/project_management/essential_delivery_guide.md) explica el
recorrido Git Bash de dos terminales: backend FastAPI con origen CORS local
explícito y frontend con `VITE_PREDICTION_API_BASE_URL`.

La variable puede vivir solo en la sesión de terminal o en un `.env.local`
ignorado por Git. El desarrollo usa el puerto `5173` y la vista previa `4173`.
Sin URL explícita, el cliente usa el origen actual para el proxy Nginx. Si la
API no responde, ClaimVox muestra indisponibilidad y no fabrica una categoría.
La misma frontera rechaza respuestas degradadas
identificadas como mock. No se usan comodines CORS, credenciales, dominios
públicos, proxy ni datos CFPB reales en este recorrido.

La identidad ClaimVox y las preferencias de tema se integraron mediante la PR
#28. Son cambios de experiencia visual: no modifican el contrato de predicción
ni acreditan modelo, servicio, autenticación o administración operativos.

## Ejecución local

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

### Flujo autenticado de demostración

1. Abrir `/login` e introducir las credenciales temporales configuradas por el operador.
2. Abrir `/classify` y escribir una narrativa sintética o pulsar `Use a synthetic example`.
3. Revisar que el texto no contiene nombres, cuentas, direcciones ni otros datos
   personales innecesarios.
4. Pulsar `Review text` y comprobar el resumen.
5. Pulsar `Classify complaint`.
6. Sin API, comprobar el error recuperable y la ausencia de categoría.
7. Con el backend en marcha, revisar `Local prediction`, la confianza devuelta
   y `Human review required`.
8. Tras una respuesta local real, confirmar o corregir la sugerencia con los
   selectores cerrados de revisión y registrar el feedback local.
9. Continuar al siguiente paso o iniciar una nueva clasificación.

En modo local configurado, la vista consulta `POST /api/v1/predictions`; el
Dashboard consulta además `GET /api/v1/health` y el resumen agregado
`GET /api/v1/feedback/summary`. Nunca consulta el CSV, artefactos de
entrenamiento ni registros individuales desde el navegador. Un error de red,
una respuesta incompatible o un modelo mock no generan una recomendación
visible. Una respuesta real sigue siendo revisable, no una decisión automática.

### Rutas

| Ruta              | Propósito                                      |
| ----------------- | ---------------------------------------------- |
| `/`               | Inicio de la aplicación local                  |
| `/classify`       | Flujo guiado y recomendación local configurada |
| `/login`          | Acceso JWT local de demostración               |
| `/admin`          | Salud y desglose agregado de feedback local    |
| `/admin/training` | Concepto de flujo de entrenamiento             |
| `/admin/models`   | Concepto de registro de modelos                |

Las rutas administrativas requieren el usuario de demostración configurado por
entorno con rol `admin`; ninguna credencial está en el repositorio. Estas
pantallas no proporcionan identidad, autorización productiva, datos operativos
compartidos, entrenamiento ni registro de modelos. El Dashboard distingue esos
límites del health y muestra solo el desglose agregado permitido: versión de
modelo, clase sugerida, decisión y conteo.

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

El selector de cliente conserva
[`src/services/mock-prediction-client.ts`](src/services/mock-prediction-client.ts)
para pruebas y compatibilidad interna, y usa el transporte HTTP tipado solo con
`VITE_PREDICTION_API_BASE_URL`. La página bloquea resultados mock; el transporte
valida las respuestas antes de mostrarlas. La vista no accede directamente a
datos de entrenamiento.

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
│   ├── hooks/              # conectividad, sesión local y dictado
│   ├── layouts/            # layouts de acceso, usuario y administración
│   ├── pages/              # clasificación y capacidades propuestas
│   ├── providers/          # contexto de sesión JWT de demostración
│   ├── pwa/                # política de caché comprobable
│   ├── services/           # clientes configurados de API y autenticación
│   └── sw.ts               # service worker
├── package.json
├── vite.config.ts
└── vitest.config.ts
```

## Limitaciones y próximos límites

- Existe un login JWT de demostración con un único usuario y rol configurados
  por entorno. No es identidad corporativa, autorización productiva ni gestión
  real de usuarios.
- No existe modelo seleccionado como Champion ni monitorización productiva. La
  inferencia real verificada es local y requiere configuración explícita.
- No existe cola operativa ni persistencia de narrativas. El feedback se limita
  a metadatos cerrados; SQLite funciona localmente y Compose define PostgreSQL,
  pero falta evidencia dinámica de la base compartida.
- Docker, Compose y un workflow EC2 están integrados, pero no existe evidencia
  versionada de URL cloud, smoke remoto, rollback o operación sostenida.
- Las pantallas de entrenamiento y modelos son conceptos no operativos.
- No se ha aprobado una política de idioma.
- Edge continúa pendiente de revisión manual equivalente.
- La PWA no ofrece clasificación offline.
- Las métricas del nivel esencial están versionadas y deben citarse con el
  tamaño y la partición del informe correspondiente; no acreditan un Champion.

La evidencia detallada está en
[`reports/validation/frontend_foundation_integration.md`](../../reports/validation/frontend_foundation_integration.md).
