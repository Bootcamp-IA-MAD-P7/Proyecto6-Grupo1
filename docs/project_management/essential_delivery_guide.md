# Guía local de ClaimVox

Esta es la guía canónica para ejecutar ClaimVox en un equipo Windows con Git
Bash. Describe una revisión segura de interfaz sin servicio y una comprobación
de inferencia y feedback locales. Ninguna equivale a despliegue, autenticación, base
compartida ni operación productiva.

## Antes de empezar

- Trabajar desde un clon actualizado del repositorio.
- No pegar narrativas reales del CFPB ni datos personales: usar el ejemplo
  sintético incluido en la interfaz.
- La interfaz nunca lee el CSV ni los artefactos de entrenamiento. Solo envía
  una narrativa al endpoint local cuando se configura explícitamente.
- El backend usa por defecto `models/cfpb_baseline.pkl`. Es un artefacto local
  ignorado por Git; sin él, el backend permanece disponible pero en modo mock.

## Opción A: revisión de interfaz sin clasificación

Este recorrido permite revisar UX, accesibilidad y dictado sin necesitar datos
ni modelos locales. No produce una categoría.

En una terminal Git Bash:

```bash
cd "/c/Users/migue/Documents/Proyecto Clasificación Multiclase/app/interface"
npm ci
npm run dev -- --host 127.0.0.1 --port 5173 --strictPort
```

Abre `http://127.0.0.1:5173/classify`, pulsa **Use example**, revisa el texto y
después intenta clasificar. Si no existe `VITE_PREDICTION_API_BASE_URL`, debe
aparecer un error recuperable, conservarse el texto en Review y no mostrarse
ninguna clase ni confianza.

Detén Vite con `Ctrl + C` cuando termines.

## Opción B: inferencia local real

Este recorrido solo funciona si el artefacto local `models/cfpb_baseline.pkl`
está disponible. No hace falta reconstruirlo para una demo si ya existe. Para
reconstruir datos o artefactos desde sus particiones locales aprobadas, consulta
los informes de evaluación antes de ejecutar entrenamiento; no se versionan
datos ni binarios.

### Terminal 1: backend

Desde la raíz del repositorio:

```bash
cd "/c/Users/migue/Documents/Proyecto Clasificación Multiclase"
export APP_CORS_ALLOWED_ORIGINS="http://127.0.0.1:5173"
python -m uvicorn app.api.main:app --host 127.0.0.1 --port 8000
```

Deja la terminal abierta. En otra terminal comprueba el estado:

```bash
curl -s http://127.0.0.1:8000/api/v1/health
```

- `"status":"ok"` significa que el predictor local está cargado y puede
  devolver una predicción real.
- `"status":"degraded"` significa que falta o no se pudo cargar el artefacto;
  la API conserva un fallback técnico, pero la PWA no presenta su salida como
  clasificación.

Si el puerto `8000` ya está ocupado, no inicies una segunda instancia. Primero
consulta esa misma ruta de salud: así sabrás si ya es el servicio local correcto.

### Terminal 2: frontend

En otra terminal Git Bash:

```bash
cd "/c/Users/migue/Documents/Proyecto Clasificación Multiclase/app/interface"
export VITE_PREDICTION_API_BASE_URL="http://127.0.0.1:8000"
npm ci
npm run dev -- --host 127.0.0.1 --port 5173 --strictPort
```

La variable se lee al iniciar Vite. Si cambias su valor, detén Vite con
`Ctrl + C` y vuelve a ejecutarlo. Abre `http://127.0.0.1:5173/classify`, usa el
ejemplo sintético y clasifica.

Con health `ok`, el resultado esperado es **Local prediction**, con una
confianza numérica, hasta tres alternativas y **Human review required**. La revisión humana
sigue siendo obligatoria: una predicción local no enruta automáticamente una
reclamación ni toma una decisión financiera.

Después de una predicción local válida aparece **Record human review**. El
registro envía únicamente versión, clases, decisión y finalidad; no guarda la
narrativa. Para comprobar el resumen agregado:

```bash
curl -s http://127.0.0.1:8000/api/v1/feedback/summary
```

La salida no contiene UUID ni registros individuales. Se conserva en SQLite
local con retención finita; no es una base compartida ni un corpus de
reentrenamiento.

Con la identidad administrativa de demostración, `/admin` muestra el health,
la disponibilidad factual del baseline y el mismo resumen en una tabla
agregada por versión de modelo, clase sugerida y decisión. `Operational data`
permanece `Not connected`: no existe base compartida ni historial individual.

## Si el navegador muestra una versión antigua

La PWA puede conservar recursos de una ejecución anterior. Antes de usar
DevTools, abre una ventana de incógnito con `Ctrl + Shift + N` y visita la misma
dirección local. Esto aísla la caché del sitio sin borrar archivos del proyecto.

Si el problema continúa, el procedimiento detallado de service workers y caché
está en el [manual del frontend](../../app/interface/README.md#pwa-y-funcionamiento-offline).

## Evidencia y límites

- EDA: `reports/validation/cfpb_eda.md`.
- Evaluación esencial: `reports/validation/cfpb_essential_evaluation.md`.
- Artefacto y smoke backend: `reports/validation/backend_foundation_real_smoke.md`.
- Integración PWA → API local: `reports/validation/claimvox_local_inference_smoke.md`.
- Estado verificable del briefing: `docs/project_management/delivery_levels.md`.

No se incorporan narrativas CFPB, predicciones por fila, datasets ni binarios de
modelo a Git. Las clases débiles requieren revisión humana reforzada. El modelo
local no está desplegado ni monitorizado en producción.
