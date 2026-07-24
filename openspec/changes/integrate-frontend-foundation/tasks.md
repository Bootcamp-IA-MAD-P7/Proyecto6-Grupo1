## 1. Inventario y línea base

- [x] 1.1 Inventariar la rama `origin/feature/frontend-foundation` y registrar en `reports/validation/frontend_foundation_inventory.md` el commit inspeccionado, autores, commits candidatos, rutas afectadas, funcionalidades, comprobaciones iniciales y exclusiones.
  - **Responsable:** Miguel / arquitectura.
  - **Dependencias:** ninguna.
  - **Evidencia:** informe que confirme o corrija el tramo candidato `2b9bfd6^..b7e95da` y diferencie trabajo frontend de cambios ajenos.
  - **Verificación:** `git rev-parse origin/feature/frontend-foundation`; `git log --reverse --format="%H%x09%an%x09%ae%x09%s" 2b9bfd6^..b7e95da`; `git diff --name-status 2b9bfd6^..b7e95da`.

- [x] 1.2 Confirmar que `feature/PG-4-integrate-frontend-foundation` parte del `dev` vigente, que la rama original permanece intacta y que no hay cambios locales ajenos a los artefactos OpenSpec aprobados.
  - **Responsable:** Miguel / arquitectura.
  - **Dependencias:** 1.1.
  - **Evidencia:** hashes de `origin/dev`, `HEAD` y rama fuente, más salida de estado incluida en el informe de inventario.
  - **Verificación:** `git fetch origin`; `git merge-base --is-ancestor origin/dev HEAD`; `git status --short --branch`; `git rev-parse origin/feature/frontend-foundation`.

## 2. Incorporación selectiva y atribución

- [x] 2.1 Recuperar exclusivamente desde `3ced1f5` los tres archivos base identificados por el inventario, conservando `Miguel Redondo Nunez <miguel.rnunez@gmail.com>` como autor y sin incorporar el commit completo.
  - **Responsable:** Miguel / integración.
  - **Dependencias:** 1.2.
  - **Evidencia:** commit preparatorio limitado a `prediction.ts`, `prediction-client.ts` y `mock-prediction-client.ts`, con autoría original.
  - **Resultado:** `e525a3e0e85c2246634fa84e72550aa8286acb09`; tres archivos, `104` líneas añadidas y autoría `Miguel Redondo Nunez <miguel.rnunez@gmail.com>` confirmada.
  - **Verificación:** `git show --stat --format=fuller HEAD`; `git diff-tree --no-commit-id --name-only -r HEAD`; `git status --short --branch`.

- [x] 2.2 Incorporar en orden únicamente los treinta commits frontend aprobados por el inventario, conservando `Abel Cañas <abelstor@gmail.com>` como autor de cada commit y sin incluir el merge commit ni documentación histórica.
  - **Responsable:** Miguel / integración, con revisión de Abel.
  - **Dependencias:** 2.1.
  - **Evidencia:** historial de `app/interface/` con autoría original y lista final de commits incorporados.
  - **Resultado:** treinta commits incorporados entre `00510a7` y `a1f41a0`; todos conservan `Abel Cañas <abelstor@gmail.com>` como autor, no modifican rutas fuera de `app/interface/` y reproducen sin diferencias el snapshot `b7e95da`.
  - **Verificación:** `git log --format="%H%x09%an%x09%ae%x09%s" origin/dev..HEAD -- app/interface`; `git diff --name-status origin/dev...HEAD`.

- [x] 2.3 Resolver los conflictos de incorporación contra los contratos vigentes de `dev`, comparar cada resolución con la rama fuente y excluir archivos ajenos a `PG-4`.
  - **Responsable:** Miguel / integración y Abel / frontend.
  - **Dependencias:** 2.2.
  - **Evidencia:** sección de conflictos y resoluciones en el informe de inventario; diferencia final acotada.
  - **Resultado:** incorporación sin conflictos, entradas sin fusionar ni marcadores; cero diferencias frente al snapshot `b7e95da` y cero rutas inesperadas. Los diecinueve hallazgos de espacios finales quedan acotados y asignados a 3.2.
  - **Verificación:** `git diff --check`; `git diff --name-only origin/dev...HEAD`; `git status --short --branch`.

## 3. Formato, lint y estructura frontend

- [x] 3.1 Instalar exactamente las dependencias bloqueadas del frontend y comprobar que la estructura importada puede ejecutarse sin modificar dependencias todavía.
  - **Responsable:** Abel / frontend.
  - **Dependencias:** 2.3.
  - **Evidencia:** instalación reproducible y cualquier fallo inicial registrado antes de corregirlo.
  - **Resultado:** `npm ci` finalizó con código `0` sobre Node.js `24.18.0` y npm `11.16.0`; instaló `585` paquetes, mantuvo intacto el lockfile `96cc4da1ecda89b59106069bc482ff16e61b0fa5` y dejó `node_modules` ignorado. La línea base informa cinco vulnerabilidades, pendientes de 8.1–8.3.
  - **Verificación:** `cd app/interface && npm ci`.

- [x] 3.2 Aplicar Prettier únicamente a `app/interface/` y dejar la comprobación de formato sin diferencias.
  - **Responsable:** Abel / frontend.
  - **Dependencias:** 3.1.
  - **Evidencia:** archivos formateados y salida correcta de Prettier.
  - **Resultado:** el commit `67907bc` normaliza con Prettier veinticinco archivos de `app/interface/`, elimina los diecinueve hallazgos de espacios finales identificados en 2.3 y no modifica rutas externas ni dependencias. `format:check` y la comprobación de whitespace finalizaron correctamente.
  - **Verificación:** `cd app/interface && npm run format`; `cd app/interface && npm run format:check`; `git diff --check`.

- [x] 3.3 Corregir errores y avisos accionables de ESLint sin desactivar reglas de accesibilidad, React o TypeScript para ocultar fallos.
  - **Responsable:** Abel / frontend.
  - **Dependencias:** 3.2.
  - **Evidencia:** lint correcto y cualquier excepción imprescindible justificada junto a la regla concreta.
  - **Resultado:** la línea base identificó un único error `@typescript-eslint/no-unused-vars` en `src/sw.ts`. Se eliminó el identificador no utilizado del bloque `catch` sin cambiar su comportamiento, desactivar reglas ni añadir excepciones. ESLint finalizó con cero errores y cero avisos.
  - **Verificación:** `cd app/interface && npm run lint`.

## 4. Contrato, flujo principal y mocks

- [x] 4.1 Alinear `PredictionRequest`, `PredictionResponse`, clases y motivos de revisión con `docs/api/openapi.json`, manteniendo `PredictionClient` desacoplado de la vista.
  - **Responsable:** Abel / frontend, con revisión de José / backend.
  - **Dependencias:** 3.3.
  - **Evidencia:** tipos y tests que demuestren que el formulario envía `PredictionRequest.narrative` y rechaza respuestas incompatibles.
  - **Resultado:** el commit `319fe07` alinea clases y motivos con OpenAPI, valida en ejecución las peticiones y respuestas y mantiene el transporte desacoplado mediante `PredictionTransport` y `PredictionClient`. El formulario envía la narrativa recortada; una respuesta con clase desconocida y una petición en blanco se rechazan. Pasan nueve tests frontend, siete tests Python del contrato y el typecheck completo.
  - **Verificación:** `cd app/interface && npm run typecheck`; `python -m unittest tests.contract.test_inference_contract -v`.

- [x] 4.2 Consolidar formulario, validación, envío, carga, error, recomendación mock, revisión humana y nueva clasificación sin persistir ni devolver la narrativa.
  - **Responsable:** Abel / frontend.
  - **Dependencias:** 4.1.
  - **Evidencia:** tests del flujo principal con fixtures sintéticos y captura o registro de los estados relevantes.
  - **Resultado:** el flujo conserva el formulario y la validación de espacios, anuncia la carga mediante `role="status"`, bloquea envíos duplicados, muestra resultados mock con motivos de revisión, conserva la narrativa solo en memoria para reintentar tras un error seguro y vuelve a un formulario vacío y enfocado al iniciar otra clasificación. Pasan doce tests frontend con contenido sintético.
  - **Verificación:** `cd app/interface && npm test -- --run`.

- [ ] 4.3 Identificar de forma persistente el modo mock, mantener confianza nula cuando no exista evidencia calibrada y eliminar cualquier texto que sugiera inferencia, modelo o rendimiento real.
  - **Responsable:** Abel / frontend, con revisión de Miguel / producto.
  - **Dependencias:** 4.2.
  - **Evidencia:** test de etiquetado mock y revisión manual del resultado.
  - **Verificación:** `cd app/interface && npm test -- --run`; `rg -n "accuracy|precision|trained|production|real prediction" app/interface/src`.

## 5. Dictado, permisos y privacidad

- [ ] 5.1 Integrar el dictado Web Speech API mediante detección de capacidad, acción explícita, inicio, parada, transcripción editable y fallback por teclado.
  - **Responsable:** Abel / frontend.
  - **Dependencias:** 4.2.
  - **Evidencia:** tests de soporte, éxito, permiso denegado y error; transcripción insertada en el campo antes del envío.
  - **Verificación:** `cd app/interface && npm test -- --run`; `cd app/interface && npm run typecheck`.

- [ ] 5.2 Documentar y mostrar disponibilidad del navegador, permiso de micrófono, posible procesamiento por el proveedor y ausencia de persistencia de audio o transcripciones.
  - **Responsable:** Abel / frontend, con revisión de Miguel / seguridad.
  - **Dependencias:** 5.1.
  - **Evidencia:** textos de interfaz, README del frontend y comprobación de Storage, Cache Storage, URL y consola con una narrativa sintética.
  - **Verificación:** `rg -n "localStorage|sessionStorage|indexedDB|console\\." app/interface/src`; revisión manual de privacidad registrada en el informe de validación.

## 6. Service worker y experiencia offline

- [x] 6.1 Separar los contextos TypeScript de React y service worker, tipar los eventos del worker y configurar un punto de inyección válido para `vite-plugin-pwa`.
  - **Responsable:** Abel / frontend.
  - **Dependencias:** 3.3.
  - **Evidencia:** typecheck y build de producción correctos sin excluir el worker de las comprobaciones.
  - **Resultado:** React, configuración Node y service worker disponen de contextos TypeScript separados y referenciados por el mismo `tsc -b`. El worker utiliza tipos `ServiceWorkerGlobalScope`, declara `self.__WB_MANIFEST` y el build `injectManifest` genera `dist/sw.js` con ocho entradas de precaché. Typecheck y build finalizan con código `0`.
  - **Verificación:** `cd app/interface && npm run typecheck`; `cd app/interface && npm run build`.

- [ ] 6.2 Limitar la caché a recursos estáticos, excluir `/api/`, ofrecer fallback de navegación y evitar cualquier respuesta de predicción fabricada sin conexión.
  - **Responsable:** Abel / frontend, con revisión de Miguel / arquitectura.
  - **Dependencias:** 6.1.
  - **Evidencia:** inspección del build, prueba sobre `vite preview` y capturas del shell offline y del bloqueo de clasificación.
  - **Verificación:** `cd app/interface && npm run build`; `cd app/interface && npm run preview -- --host 127.0.0.1`.

## 7. Capacidades propuestas

- [ ] 7.1 Separar login y autenticación mock del flujo principal, conservar su código como propuesta y dejar claro que no aporta seguridad, identidad ni permisos reales.
  - **Responsable:** Abel / frontend, con revisión de Miguel / seguridad.
  - **Dependencias:** 4.2.
  - **Evidencia:** acceso al flujo principal sin autenticación ficticia obligatoria y aviso visible cuando se revise la propuesta de login.
  - **Verificación:** `cd app/interface && npm test -- --run`; revisión manual de rutas y almacenamiento.

- [ ] 7.2 Conservar panel administrativo, entrenamiento y registro o comparación de modelos como propuestas aisladas, retirando cifras confundibles con resultados reales y etiquetando cualquier contenido sintético.
  - **Responsable:** Abel / frontend, con revisión de Miguel / producto.
  - **Dependencias:** 7.1.
  - **Evidencia:** inventario de rutas propuestas, avisos persistentes y ausencia de afirmaciones de producción, entrenamiento o métricas reales.
  - **Verificación:** `rg -n "[0-9]+(\\.[0-9]+)?%|trained|active model|production" app/interface/src/pages app/interface/src/layouts`; revisión manual registrada.

## 8. Dependencias y auditoría

- [ ] 8.1 Obtener una línea base de vulnerabilidades y dependencias desactualizadas, identificando para cada hallazgo alto o crítico el paquete directo o transitivo y su uso real.
  - **Responsable:** Abel / frontend, con revisión de Miguel / seguridad.
  - **Dependencias:** 3.1.
  - **Evidencia:** sección de dependencias en el informe de validación, sin narrativas ni datos sensibles.
  - **Verificación:** `cd app/interface && npm audit --json`; `cd app/interface && npm outdated`.

- [ ] 8.2 Aplicar actualizaciones compatibles, regenerar el lockfile sin `--force` ni overrides injustificados y repetir el conjunto de pruebas tras cada grupo de cambios.
  - **Responsable:** Abel / frontend.
  - **Dependencias:** 8.1, 4.2, 6.1.
  - **Evidencia:** diff de `package.json` y lockfile, razones de actualización y resultados de regresión.
  - **Verificación:** `cd app/interface && npm ci`; `cd app/interface && npm run typecheck`; `cd app/interface && npm run lint`; `cd app/interface && npm test -- --run`; `cd app/interface && npm run build`.

- [ ] 8.3 Cerrar la auditoría sin vulnerabilidades altas o críticas, o registrar un bloqueo explícito si no existe una actualización compatible y segura.
  - **Responsable:** Miguel / seguridad y Abel / frontend.
  - **Dependencias:** 8.2.
  - **Evidencia:** salida final de auditoría y decisión sobre cada riesgo no resuelto.
  - **Verificación:** `cd app/interface && npm audit --audit-level=high`.

## 9. Verificación funcional, UX y repositorio

- [ ] 9.1 Ejecutar la batería automática completa del frontend sobre una instalación limpia.
  - **Responsable:** Abel / frontend.
  - **Dependencias:** 4.3, 5.2, 6.2, 7.2, 8.3.
  - **Evidencia:** comandos, fecha, entorno y resultados en `reports/validation/frontend_foundation_integration.md`.
  - **Verificación:** `cd app/interface && npm ci`; `cd app/interface && npm run typecheck`; `cd app/interface && npm run lint`; `cd app/interface && npm run format:check`; `cd app/interface && npm test -- --run`; `cd app/interface && npm run build`; `cd app/interface && npm audit --audit-level=high`.

- [ ] 9.2 Verificar con contenido sintético teclado, foco, anuncios de estado, contraste, movimiento reducido y responsive en móvil, tablet y escritorio.
  - **Responsable:** Abel / UX, con revisión de Miguel.
  - **Dependencias:** 9.1.
  - **Evidencia:** matriz de escenarios, navegador, viewport, resultado y capturas no sensibles en el informe de validación.
  - **Verificación:** revisión manual sobre el build servido por `npm run preview`, documentada escenario por escenario.

- [ ] 9.3 Verificar instalación, actualización, recarga offline, ausencia de predicción sin servicio, dictado soportado y no soportado, permisos y privacidad.
  - **Responsable:** Abel / frontend, con revisión de Miguel / seguridad.
  - **Dependencias:** 9.1.
  - **Evidencia:** matriz de navegadores acordada, resultados y limitaciones en el informe de validación.
  - **Verificación:** revisión manual de Application, Cache Storage, Network, Console y permisos sobre `npm run preview`.

- [ ] 9.4 Ejecutar los quality gates del repositorio y confirmar que la diferencia frente a `dev` no contiene conflictos, whitespace, datos reales ni cambios ajenos a `PG-4`.
  - **Responsable:** Miguel / arquitectura.
  - **Dependencias:** 9.1, 9.2, 9.3.
  - **Evidencia:** salidas de calidad y revisión final de alcance incorporadas al informe.
  - **Verificación:** `python scripts/quality/check_repository.py`; `git diff --check`; `git diff --name-status origin/dev...HEAD`; `git status --short --branch`.

## 10. Documentación, evidencia y Pull Request

- [ ] 10.1 Actualizar `app/interface/README.md` con instalación, scripts, flujo mock, contrato, offline, dictado, compatibilidad, privacidad, capacidades propuestas y limitaciones.
  - **Responsable:** Abel / frontend.
  - **Dependencias:** 9.4.
  - **Evidencia:** manual reproducible alineado con el comportamiento validado.
  - **Verificación:** `python scripts/quality/check_repository.py`; revisión de enlaces y comandos del README.

- [ ] 10.2 Completar `reports/validation/frontend_foundation_integration.md` y actualizar solo los documentos globales cuyo significado cambie: estado técnico de NotebookLM, changelog y referencias mínimas de README.
  - **Responsable:** Miguel / documentación.
  - **Dependencias:** 10.1.
  - **Evidencia:** resultados reales, limitaciones, mocks, riesgos y estado de `ESS-04` todavía no verificado.
  - **Verificación:** `python scripts/documentation/build_notebooklm_pack.py --date 2026-07-24`; `python scripts/quality/check_repository.py`; `git diff --check`.

- [ ] 10.3 Revisar con Abel que se conserva su trabajo y autoría, que las tareas y evidencias coinciden con la implementación y que no hay capacidades de producción inventadas.
  - **Responsable:** Abel y Miguel.
  - **Dependencias:** 10.2.
  - **Evidencia:** revisión humana registrada en el cambio y conversaciones resueltas antes de cerrar tareas.
  - **Verificación:** `git log --format="%H%x09%an%x09%ae%x09%s" origin/dev..HEAD -- app/interface`; `npm exec -- openspec validate integrate-frontend-foundation --type change --strict`.

- [ ] 10.4 Preparar, sin publicar hasta aprobación humana, el cuerpo de Pull Request hacia `dev` mediante `.github/pull_request_template.md`, enlazando `PG-4`, este cambio OpenSpec, comandos, evidencias, riesgos y rollback.
  - **Responsable:** Miguel / integración.
  - **Dependencias:** 10.3.
  - **Evidencia:** borrador Markdown completo y diferencia final revisada.
  - **Verificación:** `python scripts/harness.py verify --change integrate-frontend-foundation`; `git diff --check`; `git status --short --branch`.

- [ ] 10.5 Solicitar revisión humana antes de cualquier archive, commit final de cierre, push, Pull Request o merge.
  - **Responsable:** Miguel / coordinación.
  - **Dependencias:** 10.4.
  - **Evidencia:** aprobación explícita y checks correctos; Jira `PG-4` conserva el estado operativo.
  - **Verificación:** no ejecutar acciones de publicación hasta recibir aprobación.
