## Context

`PG-4` solicita una React PWA responsive y accesible que permita introducir una reclamación y revisar una recomendación. Puede avanzar con mocks, pero `ESS-04` no se verificará hasta que exista una integración posterior con backend y modelo reales.

Abel ha desarrollado el frontend en `feature/frontend-foundation`. La rama remota se ha inspeccionado de forma no destructiva y su estado de referencia es `70cf2d9479047eefad07b02f05b3b64467b77fd9`. Contiene una aplicación completa bajo `app/interface/`, pero también hereda historial y cambios ajenos que no deben fusionarse directamente en `dev`.

El tramo candidato de trabajo frontend propio de Abel comienza en `2b9bfd6d5454995a75dccd90532b16badc471a2b` y termina en `b7e95da503fab3f897f226e22ba976d9cbd21bbf`. El inventario de la primera tarea deberá confirmar este límite y registrar cualquier exclusión antes de incorporar commits.

La revisión preliminar identificó estas condiciones que la fase de aplicación deberá resolver:

- el frontend no está presente todavía en `dev`;
- el flujo principal y cinco tests de componente existen en la rama fuente;
- el modo mock está parcialmente identificado;
- el dictado final utiliza Web Speech API y escribe la transcripción en la narrativa;
- existe un service worker personalizado, pero su tipado y configuración impiden completar typecheck y build;
- lint y formato no pasan todavía;
- la auditoría de dependencias comunica vulnerabilidades que deben revisarse sin `--force`;
- login mock, panel administrativo, entrenamiento y registro de modelos exceden el flujo principal aprobado y muestran estados o métricas de demostración que necesitan una presentación inequívoca como propuestas;
- la rama completa incluye conflictos y documentación global no relacionada, por lo que no es una unidad segura de merge.

Stakeholders:

- Abel: autor y responsable funcional del frontend.
- Miguel: coordinación de arquitectura, OpenSpec y proceso de integración.
- José: futuro consumidor del contrato desde backend.
- Víctor: datos y EDA; su trabajo no se modifica en este cambio.
- Personas usuarias: personal de operaciones o atención, todavía como hipótesis pendiente de contraste.

## Goals / Non-Goals

**Goals:**

- conservar el trabajo y la atribución de Abel;
- integrar únicamente el frontend relacionado con `PG-4` desde una rama limpia basada en `dev`;
- obtener una React PWA verificable con mock, revisión humana, offline, dictado, contrato TypeScript, estados y tests;
- resolver los defectos técnicos que actualmente impiden typecheck, lint, formato, build y auditoría aceptable;
- separar con claridad el flujo aprobado de las capacidades propuestas;
- dejar evidencias reproducibles para una revisión humana y una futura Pull Request.

**Non-Goals:**

- entrenar o seleccionar un modelo;
- implementar backend o inferencia real;
- marcar `ESS-04` como verificado;
- acceder al CSV desde el navegador;
- persistir audio, narrativas o feedback;
- aprobar autenticación, roles, administración, entrenamiento o registro de modelos para producción;
- fijar idioma de producto, longitud máxima, umbral de confianza o mapping a colas;
- modificar la rama de Abel o reescribir sus commits;
- incorporar documentación global o cambios ajenos a `PG-4`.

## Decisions

### 1. Integración selectiva por commits en lugar de merge de rama

Se incorporarán en orden los commits frontend atribuidos a Abel después de completar el inventario. `git cherry-pick` conserva el autor original aunque la persona integradora figure como committer. La rama `feature/frontend-foundation` no se modificará.

El tramo `2b9bfd6...^..b7e95da...` es el candidato inicial porque su diferencia neta está acotada a `app/interface/`; el inventario deberá confirmar autores, rutas y dependencias antes de ejecutarlo. El merge commit `70cf2d9...` y los commits previos de documentación o fundación no forman parte de la incorporación prevista.

Alternativas consideradas:

- **Fusionar la rama completa:** descartado porque arrastraría historial, conflictos y cambios no relacionados.
- **Copiar solo el snapshot final:** descartado porque perdería trazabilidad y atribución a nivel de commits.
- **Reimplementar desde cero:** descartado porque eliminaría trabajo válido y contradice el objetivo del cambio.

Consecuencia: pueden aparecer conflictos locales durante la incorporación, pero se resolverán contra los contratos vigentes de `dev` sin alterar la rama fuente.

### 2. Límite de integración en `app/interface/`

La aplicación se mantendrá autocontenida en `app/interface/`. Los cambios fuera de esa ruta solo se permitirán para:

- artefactos y evidencias de este cambio OpenSpec;
- ajustes mínimos y justificados en CI o quality gates para ejecutar comprobaciones reales;
- documentación cuyo significado cambie al cerrar la integración.

No se importarán README, dailies, changelog, specs heredadas ni configuraciones globales de la rama fuente. Cualquier necesidad transversal se implementará de forma mínima sobre la versión actual de `dev`, no resolviendo a favor de contenido histórico.

### 3. Flujo principal desacoplado mediante contrato TypeScript

`ClassificationPage` dependerá de una interfaz `PredictionClient`, no de una implementación concreta. `PredictionRequest`, `PredictionResponse`, clases y motivos de revisión deberán mantenerse alineados con `docs/api/openapi.json` y con el contrato de target versionado, sin duplicar decisiones nuevas.

El cliente mock:

- usará fixtures sintéticos;
- recibirá `{ narrative }`;
- no leerá el CSV, notebooks ni artefactos de modelo;
- no registrará ni devolverá la narrativa;
- devolverá confianza nula salvo que un dato sintético tenga una razón de prueba explícita;
- identificará su versión como mock y exigirá revisión humana.

Alternativa considerada:

- **Conectar directamente el frontend a los datos o a lógica de clasificación local:** descartado porque rompe los límites entre interfaz, datos e inferencia y no representa la futura arquitectura.

### 4. Dictado con detección de capacidad y degradación segura

Se conservará el enfoque final de Abel basado en Web Speech API porque reduce bundle y complejidad frente a cargar Whisper en el navegador. El reconocimiento solo comenzará tras una acción explícita, mostrará un estado de escucha, podrá detenerse y escribirá la transcripción en el mismo campo editable.

El idioma de reconocimiento se derivará de la configuración de la página o del navegador; esto no cierra la política de idioma del producto. Cualquier valor de demo se documentará como configuración técnica, no como decisión de negocio.

La interfaz deberá explicar:

- que la capacidad no está disponible en todos los navegadores;
- que requiere permiso de micrófono;
- que el navegador o su proveedor puede procesar el audio;
- que la aplicación no guarda audio ni transcripciones;
- que siempre se puede continuar mediante teclado.

Alternativas consideradas:

- **Whisper Tiny en el cliente:** descartado para esta integración por coste de descarga, complejidad, errores previos de bundling y ausencia de una decisión de producto que lo justifique.
- **Eliminar el dictado:** descartado porque forma parte del alcance aprobado y ya existe trabajo válido.

### 5. Service worker personalizado con contexto TypeScript separado

Se conservará el service worker y la estrategia `injectManifest`, pero se separará su comprobación TypeScript del contexto DOM de React. La configuración deberá:

- compilar el worker con tipos `WebWorker`;
- compilar la aplicación con tipos `DOM`;
- permitir que `vite-plugin-pwa` inyecte el precache mediante un punto de inyección válido;
- excluir `/api/` de cualquier caché de respuestas;
- precachear solo recursos estáticos necesarios;
- ofrecer fallback offline para navegación;
- evitar logs con request bodies o narrativas.

Los scripts `typecheck` y `build` deberán validar ambos contextos.

Alternativas consideradas:

- **Excluir `sw.ts` del typecheck:** descartado porque ocultaría fallos reales.
- **Cambiar a un service worker generado sin código propio:** viable a futuro, pero no elegido ahora para conservar el trabajo y el comportamiento offline ya desarrollado.

### 6. Offline limitado al shell

El worker podrá servir la aplicación y la página informativa offline, pero nunca deberá cachear ni fabricar respuestas de predicción. Si el cliente configurado necesita el servicio, el formulario mostrará un estado offline y bloqueará el envío.

El mock existe para desarrollo y pruebas de interfaz, no como promesa de inferencia offline. La evidencia deberá distinguir:

- shell disponible offline;
- resultado mock en un entorno de desarrollo explícito;
- inferencia real inexistente.

### 7. Capacidades propuestas aisladas del flujo principal

Login y autenticación mock, panel administrativo, entrenamiento y registro o comparación de modelos se conservarán en el código, pero no gobernarán el flujo principal de `PG-4`.

Se aplicarán estas reglas:

- la clasificación mock será accesible sin presentar la autenticación simulada como control de seguridad;
- las capacidades pendientes quedarán detrás de una entrada o configuración claramente marcada como laboratorio o propuesta;
- las pantallas mostrarán un aviso persistente de que no están aprobadas para producción;
- se retirarán cifras que puedan interpretarse como resultados del proyecto o se sustituirán por estados textuales inequívocamente sintéticos;
- el estado de login mock podrá persistir solo información ficticia de sesión, nunca narrativas;
- no se atribuirán permisos reales ni protección de datos a la autenticación mock.

Alternativas consideradas:

- **Eliminar estas pantallas:** descartado por la instrucción de conservar el trabajo.
- **Integrarlas como producto aprobado:** descartado porque no existen requisitos, backend, seguridad ni evidencia que las sustenten.

### 8. Dependencias actualizadas de forma compatible

La revisión empezará por `npm audit --json` y el grafo de dependencias del frontend. Se aplicarán actualizaciones compatibles y se regenerará el lockfile mediante npm. No se utilizará `npm audit fix --force`, no se ignorarán vulnerabilidades alterando el umbral y no se añadirán overrides sin justificar compatibilidad.

Si una vulnerabilidad alta o crítica no puede resolverse sin ruptura:

1. se identificará la dependencia directa o transitiva y su superficie real;
2. se evaluará una alternativa mantenida;
3. se registrará el riesgo y el bloqueo;
4. no se solicitará integración como si la auditoría estuviera resuelta.

### 9. Evidencia automática y manual proporcional

Las comprobaciones automáticas se ejecutarán desde `app/interface/`:

```bash
npm ci
npm run typecheck
npm run lint
npm run format:check
npm test -- --run
npm run build
npm audit --audit-level=high
```

Las comprobaciones de repositorio se ejecutarán desde la raíz:

```bash
python scripts/quality/check_repository.py
git diff --check
```

La revisión manual o asistida por navegador cubrirá:

- teclado y foco;
- anuncios de estado y textos alternativos;
- móvil, tablet y escritorio;
- instalación y actualización PWA;
- recarga y apertura offline;
- ausencia de resultados fabricados sin conexión;
- disponibilidad, permiso, inicio, parada y error del dictado;
- edición de la transcripción antes del envío;
- ausencia de audio o narrativas en almacenamiento, URL, logs y cachés;
- etiquetado del mock y de las capacidades propuestas.

La evidencia utilizará narrativas sintéticas y no incluirá datos CFPB reales.

### 10. Documentación mínima y fuente de verdad

Durante la aplicación se actualizarán únicamente:

- el README de `app/interface/` para instalación, scripts, mock, offline, dictado y capacidades pendientes;
- el informe de validación específico de esta integración;
- los artefactos OpenSpec y, cuando cambie el estado verificable, la fuente técnica de NotebookLM y el changelog.

No se reescribirá documentación global para compensar conflictos de la rama fuente. Jira conservará estado y responsable; OpenSpec conservará requisitos y decisiones; GitHub conservará implementación y evidencia.

## Risks / Trade-offs

- **El cherry-pick arrastra un commit no relacionado** → inventariar autores y rutas, incorporar en orden y revisar `git diff dev...HEAD` antes de continuar.
- **Resolver conflictos elimina trabajo válido de Abel** → comparar cada resolución con la rama fuente y registrar ajustes posteriores por separado.
- **El mock se interpreta como modelo real** → etiqueta persistente, versión `mock-not-a-model`, confianza nula y textos de apoyo a revisión.
- **Las pantallas administrativas inventan madurez** → aislarlas como propuestas, retirar métricas confundibles y documentar que no hay backend ni modelo.
- **Web Speech API cambia entre navegadores o procesa audio externamente** → detección de capacidad, permiso explícito, aviso de privacidad, fallback por teclado y matriz de navegadores.
- **El service worker cachea información sensible** → caché solo de recursos estáticos, exclusión de API y revisión de Cache Storage.
- **El worker funciona en desarrollo pero falla en build** → contextos TypeScript separados, build de producción y prueba sobre `vite preview`.
- **Una actualización de dependencias rompe la PWA** → cambios incrementales, lockfile, todos los checks tras cada grupo y sin arreglos forzados.
- **La PWA parece cumplir `ESS-04` antes de tiempo** → mantener el criterio en curso hasta que `PG-6` demuestre inferencia real extremo a extremo.
- **El alcance crece hacia autenticación o MLOps** → conservar esas vistas como propuestas sin implementar contratos, servicios o métricas.

## Migration Plan

1. Fijar el commit remoto inspeccionado e inventariar commits, autores, rutas y capacidades.
2. Confirmar que la rama de integración parte del `dev` vigente y que solo contiene este cambio OpenSpec.
3. Incorporar selectivamente el tramo frontend aprobado, conservando cada autor.
4. Resolver conflictos únicamente dentro del alcance y comparar el resultado con la rama original.
5. Alinear contratos, mock, flujo principal, dictado, capacidades propuestas y service worker.
6. Revisar dependencias y aplicar actualizaciones compatibles.
7. Ejecutar comprobaciones automáticas y la matriz manual.
8. Registrar resultados, limitaciones y archivos afectados en el informe de validación.
9. Revisar las tareas OpenSpec con Abel y Miguel antes de archivar o publicar.
10. Solo tras aprobación humana, archivar el cambio y preparar una Pull Request hacia `dev`.

Rollback:

- si falla la incorporación antes de completarse, usar `git cherry-pick --abort` y conservar tanto la rama fuente como los artefactos de planificación;
- si un ajuste posterior introduce una regresión, revertir ese commit concreto en la rama de integración;
- si la integración completa no es aceptable, cerrar la rama sin modificar `dev` ni `feature/frontend-foundation`.

## Open Questions

- ¿Qué navegadores y sistemas operativos formarán la matriz mínima de demo para dictado e instalación PWA?
- ¿Qué configuración de idioma se utilizará en la demo sin convertirla en política definitiva del producto?
- ¿Qué mecanismo de feature flag o navegación hará visibles las capacidades propuestas durante revisión sin confundirlas con el flujo aprobado?
- ¿Requiere el equipo una comprobación automatizada adicional de accesibilidad o será suficiente la combinación de lint, tests de componentes y evidencia manual en esta entrega?
- ¿Puede resolverse todo el riesgo de dependencias con versiones compatibles o será necesario bloquear y proponer una migración separada?
