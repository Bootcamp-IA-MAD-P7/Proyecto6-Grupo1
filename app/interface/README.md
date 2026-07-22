# Interfaz React PWA

Implementación de `003/T-006` para validar la experiencia de clasificación antes de disponer de un servicio o modelo aprobado.

`app/interface/` es la ubicación canónica del frontend. No debe crearse una carpeta `/frontend` paralela. La revisión y el endurecimiento posteriores se gobiernan mediante `003/T-008`.

## Estado

- React, TypeScript y Vite.
- Manifest y service worker generados mediante `vite-plugin-pwa`.
- Cliente de inferencia sustituible con adaptador mock activo.
- Respuestas sintéticas, confianza nula y revisión humana obligatoria.
- Sin backend, modelo, historial, feedback, routing automático ni persistencia.

El shell estático puede almacenarse para funcionar como PWA. Las rutas `/api/` se excluyen de la navegación offline y no tienen caché en runtime.

## Desarrollo

Requiere Node.js 24 o posterior.

```bash
cd app/interface
npm ci
npm run dev
```

## Verificación

```bash
npm run typecheck
npm run lint
npm test
npm run build
```

La copia de interfaz en inglés es provisional. No resuelve la política de idioma pendiente en la spec `003`.

## Integración futura

El componente recibe un `PredictionClient`. La integración real deberá implementar esa interfaz contra `/api/v1/predictions`, respetar [`docs/api/openapi.json`](../../docs/api/openapi.json) y conservar los límites de privacidad. El mock no debe reutilizarse como sustituto silencioso cuando el servicio real esté caído.

Autenticación, roles, dashboard, KPIs, entrenamiento, voz y nuevas librerías de routing, estado o componentes no forman parte del alcance vigente. Se evaluarán desde Jira y specs independientes si el producto demuestra que son necesarios.
