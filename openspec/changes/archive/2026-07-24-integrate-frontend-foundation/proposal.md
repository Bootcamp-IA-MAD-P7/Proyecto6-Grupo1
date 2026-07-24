## Why

Abel ha desarrollado una base funcional de la React PWA en `feature/frontend-foundation`, pero esa rama mezcla trabajo frontend con historial y cambios ajenos a `PG-4` y todavía no supera todas las comprobaciones del repositorio. Es necesario conservar su trabajo y autoría, integrarlo selectivamente desde una rama limpia basada en `dev` y convertirlo en una entrega verificable sin confundir mocks con capacidades reales.

## What Changes

- Inventariar la rama original y delimitar los commits y archivos que pertenecen al frontend de Abel.
- Incorporar selectivamente el trabajo frontend en la rama limpia `feature/PG-4-integrate-frontend-foundation`, preservando autoría y sin modificar `feature/frontend-foundation`.
- Consolidar una React PWA con formulario de reclamación, recomendación simulada identificada como mock, revisión humana, contrato TypeScript, estados de interfaz, funcionamiento offline, dictado por voz y tests del flujo principal.
- Alinear el dictado para que convierta voz en texto dentro del campo de narrativa y prepare ese texto para un futuro `PredictionRequest.narrative`, sin acceder al CSV ni persistir audio o narrativas.
- Corregir conflictos de integración, formato, lint, tipado y build del service worker.
- Revisar dependencias vulnerables y actualizar únicamente mediante cambios compatibles y verificables, sin arreglos forzados.
- Verificar accesibilidad, responsive, offline, dictado, permisos del navegador y privacidad.
- Mantener login y autenticación mock, panel administrativo, pantallas de entrenamiento y registro o comparación de modelos como capacidades propuestas pendientes de aprobación, separadas del flujo entregable y sin métricas o estados de producción inventados.
- Preparar evidencias reproducibles y una Pull Request acotada hacia `dev`.

### Resultados medibles

- La rama original de Abel permanece intacta y sus commits frontend conservan su atribución.
- La integración solo contiene cambios justificados por `PG-4`.
- Typecheck, lint, formato, tests, build, auditoría de dependencias y quality gate del repositorio producen resultados registrados.
- El flujo principal distingue de forma visible una recomendación mock de una inferencia real.
- El shell de la PWA funciona offline sin fabricar predicciones y el dictado respeta disponibilidad, permisos y privacidad.

### Fuera de alcance

- Implementar o simular como real un backend, un modelo entrenado o un servicio de inferencia.
- Conectar la interfaz directamente al CSV o incorporar narrativas reales del CFPB.
- Aprobar autenticación, administración, entrenamiento o registro de modelos como alcance de producción.
- Inventar precisión, confianza, modelos, entrenamientos, métricas o resultados.
- Modificar documentación global o incorporar cambios ajenos a `PG-4`, salvo la evidencia mínima exigida para cerrar esta integración.

### Entrega, privacidad y seguridad

- Este cambio avanza `ESS-04`, pero no permite marcarlo como verificado hasta conectar la PWA con inferencia real.
- El texto y el audio no se persistirán ni se incluirán en logs, analítica, URLs o almacenamiento local.
- El dictado dependerá de capacidades y permisos del navegador; sus limitaciones y riesgos se harán explícitos.
- Los fixtures y pruebas utilizarán contenido sintético.

## Capabilities

### New Capabilities

- `complaint-routing-interface`: Experiencia React PWA para introducir una reclamación, obtener una recomendación mock revisable, usar dictado accesible, operar el shell offline y respetar el contrato y los límites de privacidad.

### Modified Capabilities

Ninguna.

## Impact

- Código principal afectado: `app/interface/`.
- Contratos consultados: `docs/api/openapi.json` y `config/cfpb_target_contract.json`.
- Rama fuente preservada: `feature/frontend-foundation`.
- Rama de integración: `feature/PG-4-integrate-frontend-foundation`, basada en `dev`.
- Dependencias frontend y configuración de Vite, TypeScript, PWA, lint, formato y tests.
- Evidencias de validación específicas de la integración y plantilla de Pull Request.
- No se modifica el backend, el pipeline de datos, el modelo ni el dataset.

## Tracking

- Jira: `PG-4`.
- Historia: Construir la experiencia React PWA de clasificación.
- Expediente heredado relacionado: `specs/003-complaint-routing-experience/`, tarea `T-006`.
- Responsable funcional comunicado: Abel Cañas.
