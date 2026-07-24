# Inventario de la base frontend de Abel

## Identificación

| Campo | Valor |
|---|---|
| Cambio OpenSpec | `integrate-frontend-foundation` |
| Jira | `PG-4` |
| Tarea | `1.1` |
| Fecha | `2026-07-24` |
| Tipo de revisión | Inspección no destructiva |
| Rama fuente | `origin/feature/frontend-foundation` |
| Commit fuente inspeccionado | `70cf2d9479047eefad07b02f05b3b64467b77fd9` |
| `origin/dev` observado | `5558ae2204151767a53be0e45102bd04a3b6da83` |
| Merge base observado | `5558ae2204151767a53be0e45102bd04a3b6da83` |

Este informe no incorpora commits, no modifica `app/interface/` y no cambia la rama fuente. La inspección utilizó la referencia remota ya disponible localmente; la actualización remota y la confirmación de la línea base corresponden a la tarea `1.2`.

## Resultado ejecutivo

La rama contiene trabajo frontend reutilizable y atribuible a Abel, pero no debe fusionarse completa:

- está `37` commits por delante del `dev` observado y `0` por detrás según la referencia local;
- modifica `94` archivos frente a `dev`;
- contiene marcadores de conflicto en `26` archivos, todos fuera de `app/interface/`;
- el árbol frontend final contiene `50` archivos;
- el tramo candidato `2b9bfd6^..b7e95da` contiene `30` commits, todos de Abel;
- ese tramo modifica `47` archivos y todos pertenecen a `app/interface/`;
- el tramo no es autosuficiente: conserva tres archivos de contrato y cliente creados antes de que Abel reconstruyera la aplicación;
- el snapshot declara cinco tests del flujo principal, pero no se ejecutaron en esta tarea porque `npm ci` no terminó dentro del límite operativo de la copia temporal;
- la auditoría del lockfile informa `5` vulnerabilidades: `3` moderadas, `1` alta y `1` crítica.

Conclusión: el tramo de treinta commits queda confirmado como núcleo atribuible de Abel, con una corrección importante. Antes de incorporarlo deben materializarse de forma trazable los tres archivos base que el tramo presupone.

## Topología e historial

```text
origin/dev observado / merge base
5558ae2204151767a53be0e45102bd04a3b6da83
        |
        | 37 commits
        v
origin/feature/frontend-foundation
70cf2d9479047eefad07b02f05b3b64467b77fd9
```

El último commit es un merge de `dev` que dejó marcadores de conflicto materializados en archivos versionados. Por ello no constituye una integración válida.

### Clasificación de los commits anteriores al tramo candidato

| Commit | Autor | Contenido | Tratamiento recomendado |
|---|---|---|---|
| `3ced1f5` | Miguel Redondo Nunez | Fundación anterior de la PWA y cambios globales | No incorporar completo; contiene tres archivos base todavía necesarios |
| `a15d8b6` | Miguel Redondo Nunez | Reconciliación documental global | Excluir |
| `21b32aa` | Miguel Redondo Nunez | Cierre documental global | Excluir |
| `71eb100` | Miguel Redondo Nunez | Daily | Excluir |
| `ef2dbbf` | Abel Cañas | Cambios en la spec heredada `003` | Excluir; OpenSpec vigente gobierna la integración |
| `125cfe2` | Abel Cañas | Eliminación de la interfaz anterior conservando contratos | Usar como evidencia del límite; no es el tramo de reconstrucción |

### Commit posterior al tramo candidato

| Commit | Autor | Contenido | Tratamiento recomendado |
|---|---|---|---|
| `70cf2d9` | Abel Cañas | Merge de `dev` en la rama fuente | Excluir; contiene conflictos versionados y cambios ajenos |

## Tramo candidato atribuible a Abel

Tramo evaluado:

```text
2b9bfd6d5454995a75dccd90532b16badc471a2b^
..
b7e95da503fab3f897f226e22ba976d9cbd21bbf
```

Los treinta commits tienen el autor:

```text
Abel Cañas <abelstor@gmail.com>
```

Lista ordenada:

```text
2b9bfd6d5454995a75dccd90532b16badc471a2b feat: create package.json with full stack dependencies
64fda0eb18a8102959bf30625459bf0a7ebb7882 chore: install npm dependencies
d701e212cd0a4ae2684a7e6e50b7ac0f0af6e9e8 feat: configure Vite with PWA plugin
3d7e19148217a4483ae010c8d4854f39ef5d32a2 chore: configure TypeScript
e556a10b9d6fcccb2383e419bdb18c6a747b72eb feat: add Tailwind CSS configuration
8345f0000f0d89f5c3edaf76d1560486395c286f feat: initialize shadcn/ui
f664323ae6a99ce61b26f94b8d7008c4370d0085 chore: configure ESLint and Prettier
97ae83ea8e8db76bd371c7dd89a01ad9729f9075 feat: create index.html and entry points
d55d0a06200da5fd12849a3b4afbaf17f95c49ce feat: create project folder structure
c7be18ddc8dbceab1cc26092eab8df1789630c8e feat: implement AuthLayout
8cd069dac8953a9f49b116319cbee7a4f8d9b5d8 feat: implement UserLayout
5b41c0a52701cbac17131eed01e5f18eee9db87f feat: implement AdminLayout
a82abe9b302c017943240db32e984f3a12440df1 feat: implement mock auth with localStorage
c70321347acb05deed50ac8ffd2a43b53d2c3ca8 feat: create AuthProvider and useAuth hook
68398d0011013631260b988ab459eb4983576e1d feat: configure React Router with base routes
7bda4a57718528da1f01766c1a12df57fcf387e7 fix: resolve ESLint errors in UI components and auth
3bf162e160a30447a1201efcbaafb5a407956d40 feat: integrate PredictionResult with Tailwind + shadcn
4000e8c8d8f3dc791cf868093a70e2a730a54a83 feat: configure TanStack Query
37a027082b4509d0b5a0bb14258ddce2e1acf88d feat: create ClassificationPage with full form
45a31b3123bd99c9e08dc0c9c4764b4a361a9918 feat: add voice dictation with Whisper Tiny
c3eb91571d8f997dd6da2d0323bc82b08e9361bf fix: resolve lint errors in voice dictation hook
8509889bc4f4272878d1370346fe7f7393d2fc27 test: add main flow tests for ClassificationPage
145517988717f6b179a7d8aa6a0ea891e716fafe fix: simplify voice dictation to use pipeline API for type safety
6bb667f39533dc0e5d60dc5ebccb9aac1dd3b205 chore: remove .gitkeep files and finalize directory structure
5a1db32a2d4607e31332963f9a9c7a98f7ee9082 fix: resolve transformers.js HTML parsing error with Vite SPA fallback
e1a0e1bec2bcf46ab5c92db2c0e39b6606933d39 fix: set Spanish language for Whisper transcription
e1552ccfb6c0d26220d152c380dd9eae011ef77f fix: use low-level Whisper API with forced Spanish language
b6863d5b08002ea1dbfeaeb4246bb8fcfe78fa93 fix: pass input_features correctly to Whisper model.generate()
23a1aee818344ca048e760c2e8121d26ea72aed0 fix: replace @xenova/transformers with Web Speech API for voice dictation
b7e95da503fab3f897f226e22ba976d9cbd21bbf feat: Implement PWA features and offline support
```

Todos los archivos modificados por el tramo están dentro de:

```text
app/interface/
```

No se detectaron archivos globales ni de datos, backend, ML, documentación general o specs dentro de ese tramo.

## Prerrequisitos que el tramo no contiene

El árbol final tiene cincuenta archivos. Estos tres existen en el snapshot final, pero no son creados ni modificados por los treinta commits candidatos:

```text
app/interface/src/contracts/prediction.ts
app/interface/src/services/mock-prediction-client.ts
app/interface/src/services/prediction-client.ts
```

Proceden de la fundación anterior `3ced1f5` y fueron conservados deliberadamente por `125cfe2`. Si se aplicaran únicamente los treinta commits sobre `dev`, la aplicación quedaría incompleta.

La tarea `2.1` deberá definir una incorporación trazable que:

1. recupere esos tres archivos desde su commit de origen sin importar los cambios globales de `3ced1f5`;
2. conserve la autoría de los treinta commits de Abel;
3. no importe `a15d8b6`, `21b32aa`, `71eb100`, `ef2dbbf`, `125cfe2` ni `70cf2d9` como unidades completas;
4. revise el resultado final frente al snapshot de referencia.

No se ejecutó ninguna de estas acciones durante el inventario.

## Inventario funcional del snapshot

### Flujo aprobado por `PG-4`

- React 19, TypeScript, Vite y React Router.
- Shell PWA y página offline.
- Formulario de narrativa con validación de texto vacío.
- Ejemplo sintético.
- `PredictionClient` desacoplado.
- Respuesta mock con confianza nula y revisión humana.
- Estados de carga, error, offline y resultado.
- Nueva clasificación.
- Contrato TypeScript con once clases canónicas.
- Dictado mediante Web Speech API.
- Actualización de PWA.
- Cinco tests declarados para el flujo principal.

### Capacidades que requieren tratamiento como propuestas

- login y autenticación mock;
- persistencia de usuario mock en `localStorage`;
- roles `user` y `admin` simulados;
- panel administrativo;
- pantalla de entrenamiento;
- registro y comparación de modelos;
- cifras sintéticas de accuracy, muestras, fechas y estados de modelos.

Estas capacidades no deben eliminarse por defecto, pero tampoco pueden presentarse como autenticación segura, entrenamiento real, registro operativo o MLOps implementado.

### Dictado

El estado final del hook:

- usa `SpeechRecognition` o `webkitSpeechRecognition`;
- configura `es-ES` de forma fija;
- inserta el texto mediante `onTranscript`;
- permite iniciar y detener;
- ofrece fallback por teclado cuando no hay soporte;
- registra errores técnicos mediante `console.error`;
- no incluye todavía una explicación suficiente sobre proveedor, permisos y privacidad.

No se observa acceso directo al CSV. La transcripción se añade al mismo estado `narrative` que posteriormente utiliza el cliente de predicción.

### PWA y service worker

El snapshot contiene `src/sw.ts` con caché manual y configuración `injectManifest`. La revisión estática identifica:

- mezcla del contexto DOM de React y tipos WebWorker;
- ausencia de una separación TypeScript específica para el worker;
- configuración de Vite con formato pendiente;
- respuestas `503` sintéticas para `/api/`, que deberán revisarse para que nunca parezcan predicciones;
- logs del worker que deben comprobarse para evitar información sensible;
- whitespace pendiente en `sw.ts`, `vite.config.ts` y `public/offline.html`.

## Comprobaciones iniciales

### Alcance y conflictos

| Comprobación | Resultado |
|---|---|
| Divergencia local observada | `0` commits detrás, `37` delante |
| Archivos modificados por la rama completa | `94` |
| Archivos finales bajo `app/interface/` | `50` |
| Archivos del tramo candidato | `47` |
| Archivos del tramo candidato fuera de `app/interface/` | `0` |
| Archivos finales no aportados por el tramo | `3` |
| Archivos con marcadores de conflicto en la rama completa | `26` |
| Archivos frontend con marcadores de conflicto | `0` |

Los veintiséis archivos con conflictos son globales o documentales. Incluyen configuración Git/GitHub, README, AGENTS, documentación, scripts de calidad y specs heredadas. Se excluyen de la futura integración.

`git diff --check origin/dev...origin/feature/frontend-foundation` también comunica diecinueve incidencias de whitespace dentro de:

```text
app/interface/public/offline.html
app/interface/src/sw.ts
app/interface/vite.config.ts
```

### Instalación

Se creó un worktree temporal detached en el commit inspeccionado. `npm ci` se intentó con un límite de sesenta segundos y no terminó dentro de ese tiempo. Un intento sobre la instalación parcial produjo `ENOTEMPTY` en `node_modules/lucide-react/dist/esm/icons`; el directorio parcial se eliminó después de verificar que pertenecía al worktree temporal. Un nuevo intento limpio volvió a superar sesenta segundos.

Resultado: la instalación limpia no queda verificada en esta tarea. No se modificó el lockfile ni se aplicó ningún arreglo.

### Tests, typecheck, lint, formato y build

El paquete declara estos scripts:

```text
typecheck
lint
format:check
test
build
```

El archivo `ClassificationPage.test.tsx` declara cinco escenarios:

1. render del formulario;
2. rechazo de narrativa compuesta por espacios;
3. resultado sintético;
4. ausencia de resultado offline;
5. error de servicio seguro.

No se ejecutaron en este inventario porque la instalación limpia temporal no finalizó. Por tanto, este informe no afirma que tests, typecheck, lint, formato o build pasen.

El quality checker de la rama fuente no puede arrancar: `scripts/quality/check_repository.py` contiene marcadores de conflicto y produce `SyntaxError`. Esto confirma que debe utilizarse el script vigente de `dev`, no el de la rama fuente.

### Auditoría del lockfile

Comando:

```bash
npm audit --package-lock-only --json
```

Resultado:

| Severidad | Total |
|---|---:|
| Moderada | 3 |
| Alta | 1 |
| Crítica | 1 |
| Total | 5 |

Hallazgos principales:

- `vitest`: vulnerabilidad crítica y dependencia directa;
- `vite`: vulnerabilidad alta dentro del grafo de Vitest;
- `@vitest/mocker`, `esbuild` y `vite-node`: vulnerabilidades moderadas.

La solución propuesta por npm para el conjunto implica actualizar Vitest a una versión major. No se aplicó `npm audit fix`, `--force`, overrides ni actualización alguna.

## Exclusiones aprobadas para la futura integración

- el merge commit `70cf2d9`;
- marcadores y resoluciones de conflicto de la rama fuente;
- documentación global de la rama fuente;
- specs heredadas modificadas por Abel antes de OpenSpec;
- dailies y changelog históricos;
- workflows, Dependabot, scripts de calidad y configuración global de la rama;
- datos, notebooks, backend, modelos y cualquier narrativa CFPB;
- afirmaciones de modelo, inferencia, entrenamiento, accuracy o producción.

## Decisión de inventario

El tramo `2b9bfd6^..b7e95da` queda **confirmado con prerrequisitos**:

- es el núcleo de reconstrucción frontend atribuible a Abel;
- está correctamente acotado a `app/interface/`;
- no puede aplicarse solo porque depende de tres archivos conservados de `3ced1f5`;
- la rama completa no es apta para merge;
- las correcciones técnicas y de seguridad previstas en tareas posteriores siguen siendo necesarias.

La tarea `1.2` actualiza las referencias remotas y confirma la línea base antes de cualquier cherry-pick.

## Confirmación de línea base — tarea 1.2

Las referencias se actualizaron mediante:

```bash
git fetch --prune origin
```

El fetch eliminó dos referencias remotas locales correspondientes a ramas ya borradas y descubrió `origin/data/adopt-jupytext-workflow`. No modificó `origin/dev` ni `origin/feature/frontend-foundation`.

### Referencias antes y después

| Referencia | Antes del fetch | Después del fetch | Resultado |
|---|---|---|---|
| `origin/dev` | `5558ae2204151767a53be0e45102bd04a3b6da83` | `5558ae2204151767a53be0e45102bd04a3b6da83` | Sin cambios |
| `origin/feature/frontend-foundation` | `70cf2d9479047eefad07b02f05b3b64467b77fd9` | `70cf2d9479047eefad07b02f05b3b64467b77fd9` | Sin cambios |

La referencia fuente coincide con el commit inventariado en la tarea `1.1`. Por tanto, la rama original de Abel permanece intacta respecto al estado auditado.

### Rama de integración

| Comprobación | Resultado |
|---|---|
| Rama | `feature/PG-4-integrate-frontend-foundation` |
| HEAD confirmado | `90ca53f94da11d724fa2d18bb0560657f3b13c82` |
| Merge base con `origin/dev` | `5558ae2204151767a53be0e45102bd04a3b6da83` |
| `origin/dev` es ancestro de HEAD | Sí |
| Divergencia frente a `origin/dev` | `0` detrás, `2` delante |
| Archivos modificados frente a `origin/dev` | `6` |
| Archivos modificados bajo `app/interface/` | `0` |

Los dos commits propios de la rama de integración son:

```text
1577a504a82ec074174f27791777680995c39e70 docs: define frontend foundation integration
90ca53f94da11d724fa2d18bb0560657f3b13c82 docs: inventory frontend foundation
```

Los seis archivos de diferencia son exclusivamente:

```text
openspec/changes/integrate-frontend-foundation/.openspec.yaml
openspec/changes/integrate-frontend-foundation/design.md
openspec/changes/integrate-frontend-foundation/proposal.md
openspec/changes/integrate-frontend-foundation/specs/complaint-routing-interface/spec.md
openspec/changes/integrate-frontend-foundation/tasks.md
reports/validation/frontend_foundation_inventory.md
```

Conclusión de `1.2`: la rama de integración parte del `dev` vigente observado, contiene únicamente planificación y evidencia aprobadas y no ha incorporado ni modificado el frontend. La rama fuente continúa en el mismo commit auditado. La tarea `2.1` puede plantear la incorporación selectiva sin arrastrar una desviación previa.

## Comandos de evidencia

```bash
git fetch --prune origin
git rev-parse origin/feature/frontend-foundation
git rev-parse origin/dev
git merge-base origin/dev origin/feature/frontend-foundation
git merge-base origin/dev HEAD
git merge-base --is-ancestor origin/dev HEAD
git rev-list --left-right --count origin/dev...origin/feature/frontend-foundation
git rev-list --left-right --count origin/dev...HEAD
git log --reverse --format="%H%x09%an%x09%ae%x09%s" origin/dev..HEAD
git diff --name-only origin/dev...HEAD
git show-ref refs/remotes/origin/feature/frontend-foundation
git rev-list --count 2b9bfd6^..b7e95da
git log --reverse --format="%H%x09%an%x09%ae%x09%s" 2b9bfd6^..b7e95da
git diff --name-status 2b9bfd6^..b7e95da
git diff --check origin/dev...origin/feature/frontend-foundation
git grep -n -E "^(<<<<<<<|=======|>>>>>>>)" origin/feature/frontend-foundation
npm ci --prefer-offline --no-audit --no-fund
npm audit --package-lock-only --json
python scripts/quality/check_repository.py
```

## Incorporación selectiva — tarea 2.2

Los treinta commits aprobados se incorporaron individualmente y en el orden
original después del commit documental `a47e1d2`. La operación:

- finalizó sin conflictos;
- conservó `Abel Cañas <abelstor@gmail.com>` como autor de los treinta commits;
- no modificó ninguna ruta fuera de `app/interface/`;
- no incorporó el merge commit `70cf2d9` ni documentación histórica;
- dejó intacta `origin/feature/frontend-foundation` en
  `70cf2d9479047eefad07b02f05b3b64467b77fd9`;
- produjo un árbol `app/interface/` sin diferencias respecto al snapshot
  aprobado `b7e95da`.

| Commit fuente | Commit integrado | Mensaje |
|---|---|---|
| `2b9bfd6` | `00510a7` | feat: create package.json with full stack dependencies |
| `64fda0e` | `016c57f` | chore: install npm dependencies |
| `d701e21` | `3c220a0` | feat: configure Vite with PWA plugin |
| `3d7e191` | `653c606` | chore: configure TypeScript |
| `e556a10` | `d535b24` | feat: add Tailwind CSS configuration |
| `8345f00` | `58074c5` | feat: initialize shadcn/ui |
| `f664323` | `bcb7cc8` | chore: configure ESLint and Prettier |
| `97ae83e` | `5486d3b` | feat: create index.html and entry points |
| `d55d0a0` | `d4425da` | feat: create project folder structure |
| `c7be18d` | `c1a8dbd` | feat: implement AuthLayout |
| `8cd069d` | `e12de40` | feat: implement UserLayout |
| `5b41c0a` | `66bd297` | feat: implement AdminLayout |
| `a82abe9` | `fbf2135` | feat: implement mock auth with localStorage |
| `c703213` | `de2c934` | feat: create AuthProvider and useAuth hook |
| `68398d0` | `355e23b` | feat: configure React Router with base routes |
| `7bda4a5` | `11784e6` | fix: resolve ESLint errors in UI components and auth |
| `3bf162e` | `0fee48c` | feat: integrate PredictionResult with Tailwind + shadcn |
| `4000e8c` | `f321202` | feat: configure TanStack Query |
| `37a0270` | `2947e03` | feat: create ClassificationPage with full form |
| `45a31b3` | `433a518` | feat: add voice dictation with Whisper Tiny |
| `c3eb915` | `a200c1e` | fix: resolve lint errors in voice dictation hook |
| `8509889` | `f8f5859` | test: add main flow tests for ClassificationPage |
| `1455179` | `b1012e3` | fix: simplify voice dictation to use pipeline API for type safety |
| `6bb667f` | `c9e1b58` | chore: remove .gitkeep files and finalize directory structure |
| `5a1db32` | `f50d6e4` | fix: resolve transformers.js HTML parsing error with Vite SPA fallback |
| `e1a0e1b` | `39883cd` | fix: set Spanish language for Whisper transcription |
| `e1552cc` | `0d0b24c` | fix: use low-level Whisper API with forced Spanish language |
| `b6863d5` | `0057dbe` | fix: pass input_features correctly to Whisper model.generate() |
| `23a1aee` | `10098b9` | fix: replace @xenova/transformers with Web Speech API for voice dictation |
| `b7e95da` | `a1f41a0` | feat: Implement PWA features and offline support |

## Revisión de conflictos y alcance — tarea 2.3

La incorporación no produjo conflictos que requirieran una resolución manual:

| Comprobación | Resultado |
|---|---|
| Entradas sin fusionar en el índice | `0` |
| Marcadores de conflicto en `app/interface/` | `0` |
| Diferencias frente al snapshot aprobado `b7e95da` | `0` |
| Rutas inesperadas frente a `origin/dev` | `0` |
| Estado local después de la revisión | Limpio |

La diferencia frente a `origin/dev` contiene `56` archivos:

- `50` archivos del árbol final `app/interface/`;
- los cinco artefactos del cambio
  `openspec/changes/integrate-frontend-foundation/`;
- este informe de validación.

No se incorporaron documentos históricos, backend, datos, modelos, notebooks ni
otros archivos ajenos a `PG-4`. La rama fuente permaneció intacta en
`70cf2d9479047eefad07b02f05b3b64467b77fd9`.

La comprobación reforzada `git diff --check origin/dev...HEAD` identificó
diecinueve líneas con espacios finales en:

- `app/interface/public/offline.html`;
- `app/interface/src/sw.ts`;
- `app/interface/vite.config.ts`.

No son conflictos de incorporación y no se corrigieron durante 2.3 para no
mezclar responsabilidades. Su corrección y la comprobación completa de formato
pertenecen a la tarea 3.2.

## Instalación reproducible — tarea 3.1

La instalación se ejecutó desde `app/interface/` sin modificar dependencias:

```bash
npm ci
npm ls --depth=0
```

| Campo | Resultado |
|---|---|
| Fecha | `2026-07-24` |
| Node.js | `24.18.0` |
| npm | `11.16.0` |
| Código de salida de `npm ci` | `0` |
| Paquetes instalados | `585` |
| Paquetes auditados por npm | `586` |
| Hash Git del lockfile antes y después | `96cc4da1ecda89b59106069bc482ff16e61b0fa5` |
| Modificaciones en archivos versionados | Ninguna |
| `node_modules` ignorado por Git | Sí |

La instalación informó:

- tres vulnerabilidades moderadas;
- una vulnerabilidad alta;
- una vulnerabilidad crítica;
- avisos de obsolescencia para `whatwg-encoding` y `glob`.

No se ejecutó `npm audit fix`, `--force`, una actualización de paquetes ni una
corrección de código. La identificación de las cadenas de dependencia y su
tratamiento corresponden a las tareas 8.1–8.3.

No se usaron narrativas reales, credenciales, secretos, datasets ni servicios externos de IA.

## Normalización de formato — tarea 3.2

El formato se aplicó exclusivamente dentro de `app/interface/` después de
confirmar la instalación reproducible de la tarea 3.1:

```bash
cd app/interface
npm run format
npm run format:check
cd ../..
git diff --check
```

| Campo | Resultado |
|---|---|
| Fecha | `2026-07-24` |
| Commit | `67907bc` |
| Archivos modificados | `25`, todos bajo `app/interface/` |
| Diferencia | `230` inserciones y `263` eliminaciones de formato |
| Código de salida de `npm run format` | `0` |
| Código de salida de `npm run format:check` | `0` |
| Resultado de Prettier | Todos los archivos comprobados utilizan el estilo configurado |
| Resultado de `git diff --check` | Sin errores |
| Dependencias o lockfile modificados | Ninguno |
| Cambio funcional intencionado | Ninguno |

La normalización corrigió también los diecinueve espacios finales detectados
durante la tarea 2.3 en `public/offline.html`, `src/sw.ts` y `vite.config.ts`.
Los avisos locales de Git sobre conversión futura entre LF y CRLF no representan
errores de contenido ni una comprobación fallida.

No se ejecutaron lint, typecheck, tests, build ni correcciones funcionales como
parte de esta tarea; pertenecen a tareas posteriores del cambio.

## Corrección de lint — tarea 3.3

La primera ejecución de ESLint encontró un único problema:

```text
src/sw.ts
93:18  error  'error' is defined but never used
@typescript-eslint/no-unused-vars
```

Se sustituyó `catch (error)` por `catch` porque el identificador no se utilizaba.
La captura y el fallback de caché mantienen el mismo comportamiento.

| Comprobación | Resultado |
|---|---|
| Fecha | `2026-07-24` |
| Archivos de código modificados | `app/interface/src/sw.ts` |
| Reglas desactivadas | Ninguna |
| Excepciones añadidas | Ninguna |
| `npm run lint` final | Código `0`; cero errores y cero avisos |
| `npm run format:check` | Código `0` |
| `git diff --check` | Sin errores |

No se modificaron contratos, dependencias, configuración de ESLint ni
funcionalidades de la interfaz.

## Contrato frontend — tarea 4.1

El contrato TypeScript se contrastó con `docs/api/openapi.json` y se añadió una
frontera de validación en tiempo de ejecución:

- `PredictionRequest` solo admite `narrative` y el identificador técnico opcional;
- las once clases canónicas y los cinco motivos de revisión se comparan con OpenAPI;
- las respuestas deben contener todos los campos obligatorios y ningún campo extra;
- las clases, UUID, fecha, confianza, alternativas y reglas de revisión se validan;
- una respuesta incompatible se transforma en un error seguro
  `invalid_response`;
- `PredictionTransport` queda separado de `PredictionClient`, por lo que la vista
  no depende de una futura implementación HTTP;
- el formulario envía la narrativa recortada y rechaza valores en blanco.

| Comprobación | Resultado |
|---|---|
| Commit de implementación | `319fe07` |
| Tests del cliente y formulario | `9` aprobados |
| Tests Python del contrato | `7` aprobados |
| Respuesta con clase desconocida | Rechazada |
| Petición con narrativa en blanco | Rechazada antes de llamar al transporte |
| `npm run typecheck` final | Código `0` |
| Narrativas reales utilizadas | Ninguna |

El primer typecheck ejecutado tras implementar el contrato mostró ocho errores
exclusivamente en `src/sw.ts`. No se ocultaron ni se atribuyeron al contrato: se
resolvieron mediante la separación de contextos de la tarea 6.1 antes de cerrar
formalmente 4.1.

## Contexto TypeScript y build PWA — tarea 6.1

La línea base mezclaba los tipos DOM de React con los tipos WebWorker. Además,
el build `injectManifest` no encontraba `self.__WB_MANIFEST`. La solución:

- excluye `src/sw.ts` del contexto React;
- añade `tsconfig.worker.json` con `WebWorker`;
- referencia app, worker y configuración Node desde `tsconfig.json`;
- declara el módulo virtual de registro PWA;
- tipa los eventos sobre `ServiceWorkerGlobalScope`;
- utiliza `self.__WB_MANIFEST` como punto de inyección;
- garantiza que el fallback HTML siempre devuelve una `Response`.

| Comprobación | Resultado |
|---|---|
| `npm run typecheck` | Código `0` |
| `npm run build` | Código `0` |
| Estrategia PWA | `injectManifest` |
| Worker generado | `dist/sw.js` |
| Entradas de precaché inyectadas | `8` |
| Tamaño comunicado del precaché | `336.03 KiB` |
| Tests frontend de regresión | `9` aprobados |
| ESLint | Cero errores y cero avisos |
| Prettier | Correcto |

La política de caché, la exclusión operativa de `/api/` y el comportamiento
offline completo todavía pertenecen a la tarea 6.2; este resultado no los da por
verificados.

## Flujo principal — tarea 4.2

El flujo ya aportado por Abel se mantuvo y se reforzó con una indicación
accesible del envío y pruebas sobre todos sus estados principales.

| Escenario | Resultado verificado |
|---|---|
| Formulario inicial | Campo y acción principal disponibles |
| Entrada en blanco o con espacios | Envío bloqueado y mensaje asociado al campo |
| Petición válida | Solo envía `PredictionRequest.narrative` recortada |
| Envío en curso | Estado anunciado, campo y botón deshabilitados |
| Envío duplicado | Impedido mientras la petición está pendiente |
| Resultado mock | Clase sintética, alternativas y revisión visibles |
| Motivo de revisión | `confidence_unavailable` explicado en texto |
| Error de servicio | Mensaje seguro sin stack ni narrativa |
| Frecuencia limitada | Mensaje específico sin detalle interno |
| Reintento | Narrativa conservada únicamente en el estado del formulario |
| Nueva clasificación | Formulario vacío y foco devuelto al campo |
| Persistencia o devolución de narrativa | No implementada |

La batería final contiene doce tests aprobados: cuatro de la frontera contractual
y ocho del flujo de clasificación. También pasan `typecheck`, ESLint, Prettier y
la comprobación de whitespace.

No existe todavía backend, inferencia ni modelo real. La recomendación sigue
siendo sintética.

## Etiquetado inequívoco del mock — tarea 4.3

El resultado del flujo principal identifica de forma persistente que se trata de
una demostración de interfaz. La etiqueta, el aviso y los textos de apoyo no
atribuyen la respuesta a una capacidad real ni permiten confundirla con una
decisión automática.

| Comprobación | Resultado |
|---|---|
| Etiqueta visible | `Mock response · demo only` |
| Aviso persistente | Respuesta sintética que no puede enrutar una reclamación |
| Confianza | `null`; se muestra `Not available` |
| Porcentaje de confianza | No se renderiza |
| Revisión humana | Obligatoria y visible |
| Fuente técnica mostrada | Identificada como mock |
| Tests frontend | `12` aprobados |
| Typecheck | Código `0` |
| ESLint | Código `0` |
| Prettier | Código `0` |
| `git diff --check` | Sin errores |

La búsqueda
`rg -n "accuracy|precision|trained|production|real prediction" app/interface/src`
solo devuelve las tres propiedades `accuracy` del registro administrativo
sintético. Esas rutas no forman parte del flujo principal de clasificación y su
aislamiento, retirada de cifras y etiquetado definitivo están asignados a la
tarea 7.2. Este resultado no aprueba el panel administrativo ni sus métricas.

## Dictado funcional y fallback — tarea 5.1

Se conserva el enfoque Web Speech API aportado por Abel y se refuerza su
integración sin añadir dependencias ni procesar audio dentro de la aplicación.
El reconocimiento se obtiene en tiempo de ejecución, por lo que la interfaz
puede distinguir de forma fiable entre navegadores compatibles y no
compatibles.

| Escenario | Resultado verificado |
|---|---|
| Inicio | Solo después de pulsar `Start dictation` |
| Estado activo | `Listening…` anunciado mediante `role="status"` |
| Transcripción | Se añade recortada al campo de narrativa |
| Edición posterior | El campo continúa habilitado y editable |
| Parada manual | Detiene la instancia y restablece la acción de inicio |
| Idioma técnico | Documento, navegador o fallback `en-US` |
| Navegador sin soporte | Teclado disponible y explicación visible |
| Permiso denegado | Mensaje seguro y retorno al teclado |
| Error de reconocimiento | Mensaje seguro y retorno al teclado |
| Dependencias nuevas | Ninguna |
| Tests frontend | `16` aprobados |
| Typecheck | Código `0` |
| ESLint | Código `0` |
| Prettier | Código `0` |

Esta tarea verifica el comportamiento funcional. Los avisos completos sobre
permiso, posible procesamiento por el proveedor y ausencia de persistencia se
abordan de forma separada en 5.2.

## Privacidad y condiciones del dictado — tarea 5.2

Antes de activar el micrófono, la interfaz comunica que la función:

- solicitará permiso mediante el navegador;
- puede depender del navegador o de su proveedor para procesar audio;
- no guarda audio ni transcripciones en esta aplicación;
- deja el texto editable para revisión antes del envío;
- mantiene el teclado como alternativa.

La misma información queda versionada en `app/interface/README.md`. No se afirma
compatibilidad universal ni se convierte el idioma técnico de reconocimiento en
una política de producto.

Se ejecutó un test con la cadena sintética `Synthetic spoken complaint` y se
obtuvo:

| Superficie revisada | Resultado |
|---|---|
| `localStorage` y `sessionStorage` | Ninguna escritura durante el dictado |
| Cache Storage | Ninguna apertura o escritura durante el dictado |
| URL | Sin cambios |
| Consola | Sin texto ni eventos registrados por el flujo |
| Campo de narrativa | Transcripción visible y editable |
| Tests frontend | `16` aprobados |
| Typecheck, ESLint y Prettier | Correctos |

La búsqueda estática requerida conserva hallazgos fuera del flujo de dictado:

- `auth-client.ts` usa `localStorage` exclusivamente para la sesión ficticia;
- `main.tsx` y `sw.ts` contienen mensajes técnicos genéricos sin cuerpo de
  petición, audio ni narrativa.

Estos hallazgos no se ocultan ni se consideran aprobados: la autenticación mock
se revisa en 7.1 y los límites del service worker en 6.2 y 9.3.

## Política de caché y shell offline — tarea 6.2

La implementación anterior aplicaba caché dinámica a casi cualquier petición
GET y la página offline afirmaba que las clasificaciones se guardarían y
sincronizarían. Ambas conductas se retiraron.

La nueva política se encuentra en `src/pwa/cache-policy.ts` y dispone de siete
tests específicos:

| Tipo de petición | Estrategia |
|---|---|
| `/api` y `/api/*` | Solo red |
| Métodos distintos de GET | Solo red |
| Orígenes externos | Solo red |
| Fetch de datos sin destino estático | Solo red |
| Navegación del mismo origen | Red con fallback al shell o ayuda offline |
| CSS, JavaScript, imágenes, fuentes y manifiesto | Caché estática del mismo origen |
| `connectivity-check.txt` | Solo red y sin contenido de negocio |

El worker:

- no intercepta ni fabrica respuestas para API o escrituras;
- no almacena respuestas de predicción ni peticiones de datos;
- elimina únicamente cachés antiguas que pertenecen a esta aplicación;
- precarga los ocho recursos generados por el build;
- normaliza las URLs antes de precargarlas para evitar peticiones equivalentes
  duplicadas;
- recupera recursos estáticos del mismo origen ignorando únicamente diferencias
  de `Vary`, después de que la política haya descartado API, datos y orígenes
  externos;
- no registra peticiones, cuerpos ni narrativas;
- ofrece un mensaje offline que niega expresamente almacenamiento o
  sincronización de clasificaciones.

La interfaz no depende solo de `navigator.onLine`. Antes de invocar el cliente
realiza una petición `HEAD` sin caché a `connectivity-check.txt`. Esta sonda no
incluye la narrativa, no accede a datos ni se precarga. Si falla, actualiza el
estado a offline, muestra un aviso y deshabilita la acción sin llamar al cliente
mock.

| Comprobación automática | Resultado |
|---|---|
| Tests de política | `7` aprobados |
| Tests frontend totales | `24` aprobados |
| Typecheck, ESLint y Prettier | Correctos |
| Build PWA | Correcto |
| Entradas de precaché | `8` |
| `vite preview` `/` | HTTP `200` |
| `vite preview` `/offline.html` | HTTP `200` y texto honesto |
| `vite preview` `/sw.js` | HTTP `200` y política incluida |
| OpenSpec estricto | Correcto |
| Quality gate del repositorio | Correcto |

### Revisión manual en navegador

La revisión se realizó el `2026-07-24` con Chrome y DevTools sobre
`http://127.0.0.1:4173/classify`, utilizando exclusivamente el ejemplo
sintético de la interfaz.

1. La primera instalación falló porque rutas como `app-mark.svg` y
   `/app-mark.svg` se convertían en la misma petición. Se normalizó y deduplicó
   el precaché, y se añadió una prueba de regresión.
2. El primer shell offline quedó sin estilos ni JavaScript porque las respuestas
   de Vite incluían `Vary: Origin`. Se restringió primero el acceso a recursos
   estáticos del mismo origen y se utilizó `ignoreVary` solo en esa caché.
3. Chrome mantuvo `navigator.onLine` durante la simulación de Service Worker y
   permitió inicialmente una respuesta mock. Se añadió la sonda anónima de
   conectividad y una prueba que demuestra que el cliente no se invoca cuando
   la sonda falla.
4. La versión final del worker quedó `activated and running`.
5. Cache Storage mostró únicamente `/`, `app-mark.svg`, los bundles CSS y
   JavaScript, el helper de Workbox, `index.html`, `manifest.webmanifest` y
   `offline.html`; no aparecieron `/api`, narrativas ni respuestas.
6. Con `Offline` activo, `/classify` recargó el shell completo, mostró
   `You are offline. A prediction requires a service connection.`, mantuvo el
   campo vacío, deshabilitó `Classify complaint` y no presentó resultado.

Las capturas se revisaron durante la sesión y no contienen narrativas reales,
audio ni datos del CFPB. No se incorporan artefactos del navegador al
repositorio.

## Separación de autenticación mock — tarea 7.1

El flujo principal dejó de depender de la autenticación ficticia:

- `/classify` y el layout de usuario son accesibles sin sesión;
- visitar el flujo público no crea `complaint-routing-auth` ni otra identidad;
- la cabecera muestra `Public prototype · no identity` y enlaza a la revisión
  opcional del login;
- una sesión ficticia activa se identifica como `Mock session`;
- `End mock session` elimina solo la clave de la demo y vuelve a `/classify`;
- `/login` se conserva como propuesta y permite regresar mediante
  `Continue without mock login`.

La pantalla de login muestra antes del formulario:

> Mock authentication proposal only. This screen uses fixed demo identities
> and accepts any password. It provides no real identity, security,
> authorization or access control.

| Comprobación | Resultado |
|---|---|
| Acceso directo a `/classify` sin sesión | Correcto |
| Identidad mostrada en el flujo público | `Public prototype · no identity` |
| Escritura de autenticación al visitar el flujo | Ninguna |
| Acceso a `/login` como revisión opcional | Correcto |
| Advertencia persistente de ausencia de seguridad | Visible |
| Retorno al flujo sin iniciar sesión | Correcto |
| Tests de rutas añadidos | `2` aprobados |
| Tests frontend totales | `26` aprobados |
| Typecheck, ESLint y Prettier | Correctos |
| Build PWA | Correcto |

La revisión manual se realizó el `2026-07-24` sobre `vite preview`. Las
capturas muestran únicamente identidades sintéticas de la propia demo y no se
incorporan al repositorio. El código de autenticación mock y su almacenamiento
local se conservan solo para evaluar la propuesta; no constituyen un control de
seguridad. Las rutas administrativas y sus contenidos se revisan por separado
en la tarea 7.2.

## Capacidades administrativas como propuestas — tarea 7.2

El trabajo visual de Abel se conserva sin presentar madurez inexistente. Las
rutas administrativas continúan disponibles para revisión mediante la identidad
sintética `carlos@example.com`, pero el layout las identifica de forma
persistente como conceptos sin autorización real:

| Ruta | Capacidad conservada | Estado verificable |
|---|---|---|
| `/admin` | Resumen administrativo | Concepto sin datos operativos ni servicio conectado |
| `/admin/training` | Flujo de entrenamiento | Propuesta sin dataset, ejecución ni resultados |
| `/admin/models` | Registro y comparación | Propuesta vacía sin modelos ni evidencias |

Se eliminaron las cifras que podían confundirse con resultados del proyecto:
volúmenes, porcentajes, latencias, muestras de entrenamiento, versiones, fechas
y estados de modelos. En su lugar, la interfaz utiliza estados textuales
inequívocos y no accionables. La portada pública también dejó de presentar
métricas simuladas y diferencia la interfaz disponible de los flujos todavía no
conectados.

El aviso común comunica que no existen:

- permisos reales;
- datos operativos;
- trabajos de entrenamiento;
- modelos registrados;
- resultados de comparación;
- servicios desplegados.

| Comprobación | Resultado |
|---|---|
| Rutas administrativas conservadas | `3` |
| Tests de rutas de propuesta | `3` aprobados |
| Tests frontend totales | `29` aprobados |
| Typecheck | Correcto |
| ESLint | Correcto |
| Prettier | Correcto |
| Build PWA | Correcto |
| Búsqueda de métricas y afirmaciones confundibles | Sin resultados |

La revisión manual se realizó el `2026-07-24` con Chrome sobre `vite preview`.
Se inspeccionaron el resumen administrativo, el concepto de entrenamiento y el
concepto de registro de modelos. Las tres vistas conservaron el aviso
persistente, no ofrecieron acciones operativas y no mostraron cifras o estados
atribuibles a un sistema real. Las capturas contienen únicamente una identidad
de demostración incluida en la propia interfaz y no se incorporan al
repositorio.

## Línea base de dependencias — tarea 8.1

La auditoría se ejecutó sin modificar `package.json`, el lockfile ni
`node_modules`:

```bash
npm audit --json
npm outdated --json
npm ls vitest vite vite-node @vitest/mocker esbuild --all
npm explain vitest
npm explain vite-node
npm explain @vitest/mocker
npm explain esbuild
```

### Resumen

| Severidad | Total |
|---|---:|
| Moderada | 3 |
| Alta | 1 |
| Crítica | 1 |
| Total | 5 |

Todos los hallazgos pertenecen al entorno de desarrollo y pruebas. No forman
parte de las dependencias de ejecución declaradas ni del bundle final de la
aplicación.

### Cadena afectada

```text
vitest@2.1.9                           dependencia directa de desarrollo
├── @vitest/mocker@2.1.9               transitiva
│   └── vite@5.4.21                    transitiva
├── vite-node@2.1.9                    transitiva
│   └── vite@5.4.21                    transitiva
│       └── esbuild@0.21.5             transitiva
└── vite@5.4.21                        transitiva
    └── esbuild@0.21.5                 transitiva
```

La cadena principal de build queda separada:

```text
vite@6.4.3                             dependencia directa de desarrollo
└── esbuild@0.25.12                    transitiva
```

`vite@6.4.3` y `esbuild@0.25.12` no pertenecen a los rangos afectados
comunicados por la auditoría.

### Hallazgos altos y críticos

| Paquete | Severidad | Relación | Aviso | Uso observado |
|---|---|---|---|---|
| `vitest@2.1.9` | Crítica | Directa de desarrollo | `GHSA-5xrq-8626-4rwp` | Runner local de los tests; el servidor UI vulnerable no está configurado ni se inicia con los scripts del proyecto |
| `vite@5.4.21` | Alta | Transitiva de Vitest | `GHSA-fx2h-pf6j-xcff` | Transformación y servidor interno del runner de tests; no es el Vite utilizado por el build principal |

El aviso crítico describe lectura y ejecución arbitrarias cuando el servidor UI
de Vitest está escuchando. El proyecto ejecuta `vitest run`, no declara
`@vitest/ui` y no expone ese servidor. Esto reduce la superficie actual, pero no
justifica conservar una versión vulnerable.

El aviso alto afecta a rutas alternativas de Windows en `server.fs.deny`. La
copia vulnerable es `vite@5.4.21`, instalada dentro del árbol de Vitest. El
servidor de build principal utiliza `vite@6.4.3`.

### Hallazgos moderados

| Paquete | Relación | Origen |
|---|---|---|
| `@vitest/mocker@2.1.9` | Transitiva de Vitest | Depende de la copia vulnerable de Vite |
| `vite-node@2.1.9` | Transitiva de Vitest | Depende de la copia vulnerable de Vite |
| `esbuild@0.21.5` | Transitiva de Vite dentro de Vitest | `GHSA-67mh-4wv8-2f99` |

La auditoría también comunica dos avisos moderados adicionales sobre la copia de
Vite: `GHSA-4w7w-66w2-5vf9` y `GHSA-v6wh-96g9-6wx3`.

### Dependencias desactualizadas

`npm outdated` informa varias versiones major disponibles. No se actualizarán
en bloque porque una versión más reciente no implica automáticamente una
migración necesaria o compatible. Para resolver la cadena vulnerable, npm
propone `vitest@4.1.10`, que constituye un cambio major. La tarea 8.2 evaluará
exclusivamente esa actualización y ejecutará typecheck, lint, formato, tests y
build antes de considerar cualquier otro paquete.

No se utilizó `npm audit fix`, `--force`, overrides ni modificación manual del
lockfile.

## Actualización compatible de dependencias — tarea 8.2

La única actualización necesaria para retirar la cadena vulnerable identificada
en 8.1 fue el runner de pruebas:

| Dependencia directa | Antes | Después | Motivo |
|---|---:|---:|---|
| `vitest` | `2.1.9` | `4.1.10` | Retirar la cadena vulnerable de Vite 5 y conservar compatibilidad con Node.js 24 y Vite 6 |

La actualización se aplicó mediante npm y regeneró `package-lock.json`. No se
utilizaron `npm audit fix`, `--force`, overrides ni ediciones manuales del
lockfile.

### Compatibilidad comprobada

- `vitest@4.1.10` admite Node.js `^20`, `^22` o `>=24`;
- su peer de Vite admite las versiones `6`, `7` y `8`;
- el proyecto utiliza Node.js `24.18.0` y conserva `vite@6.4.3`;
- los scripts existentes continúan funcionando sin cambios;
- `npm ci` reconstruye correctamente las dependencias desde el lockfile.

### Árbol resultante

```text
vite@6.4.3
└── esbuild@0.25.12

vitest@4.1.10
├── @vitest/mocker@4.1.10
│   └── vite@6.4.3 deduplicado
└── vite@6.4.3 deduplicado
```

Ya no aparecen en el árbol `vite-node@2.1.9`, `vite@5.4.21` ni
`esbuild@0.21.5`.

### Regresión sobre instalación limpia

| Comprobación | Resultado |
|---|---|
| `npm ci` | Correcto; `575` paquetes instalados y `0` vulnerabilidades |
| `npm run typecheck` | Correcto |
| `npm run lint` | Correcto |
| `npm run format:check` | Correcto |
| `npm test -- --run` | `4` archivos y `29` tests aprobados |
| `npm run build` | Correcto; PWA generada con `8` entradas de precaché |
| `npm audit --audit-level=high` | Correcto; `0` vulnerabilidades |

npm mantiene avisos de deprecación en paquetes transitivos de desarrollo, pero
la auditoría no les atribuye vulnerabilidades. Su eventual actualización no se
mezcla con esta corrección de seguridad y requerirá una evaluación independiente
si llega a afectar al proyecto.

## Cierre de auditoría — tarea 8.3

La auditoría final se ejecutó el `2026-07-24` sobre el lockfile actualizado y
comprometido en `b181fba`:

```bash
npm audit --audit-level=high --json
```

| Severidad | Resultado |
|---|---:|
| Informativa | 0 |
| Baja | 0 |
| Moderada | 0 |
| Alta | 0 |
| Crítica | 0 |
| Total | 0 |

npm analizó `645` dependencias y finalizó con código `0`. Los cinco hallazgos
registrados en la línea base 8.1 quedan resueltos por la actualización compatible
de Vitest realizada en 8.2. No quedan vulnerabilidades conocidas, excepciones,
riesgos de seguridad pendientes ni bloqueos de dependencias para esta
integración.
