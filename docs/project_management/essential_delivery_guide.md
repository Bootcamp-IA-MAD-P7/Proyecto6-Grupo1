# Guía local de ClaimVox

Esta es la guía canónica para ejecutar ClaimVox en un equipo Windows con Git
Bash. Describe una revisión segura de interfaz y una comprobación autenticada
de inferencia y feedback locales. El inicio de sesión es una frontera de
demostración configurada por entorno: no equivale a identidad corporativa,
autorización productiva, despliegue ni operación compartida.

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
export APP_JWT_SECRET="<random-local-secret>"
export APP_DEMO_USERNAME="<temporary-reviewer>"
export APP_DEMO_PASSWORD="<temporary-password>"
export APP_DEMO_ROLE="admin"
export APP_DEMO_NAME="Local reviewer"
python -m uvicorn app.api.main:app --host 127.0.0.1 --port 8000
```

Los valores anteriores son temporales y no se escriben en Git. Sin usuario y
contraseña configurados, el endpoint de login rechaza todo acceso. En una
operación real deben sustituirse por un proveedor de identidad, sesiones y
permisos administrados.

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
`Ctrl + C` y vuelve a ejecutarlo. Abre `http://127.0.0.1:5173/login`, utiliza
las credenciales temporales de la terminal del backend y después entra en
`/classify`, usa el ejemplo sintético y clasifica.

Con health `ok`, el resultado esperado es **Local prediction**, con una
confianza numérica, hasta tres alternativas y **Human review required**. La revisión humana
sigue siendo obligatoria: una predicción local no enruta automáticamente una
reclamación ni toma una decisión financiera.

Después de una predicción local válida aparece **Record human review**. El
registro envía únicamente versión, clases, decisión y finalidad; no guarda la
narrativa. El Dashboard autenticado muestra el mismo resumen agregado. Para
consultarlo por terminal, primero solicita un token con las credenciales
temporales:

```bash
TOKEN="$(
  curl -s -X POST http://127.0.0.1:8000/api/v1/auth/login \
    -H "Content-Type: application/json" \
    --data "{\"username\":\"${APP_DEMO_USERNAME}\",\"password\":\"${APP_DEMO_PASSWORD}\"}" \
  | python -c "import json,sys; print(json.load(sys.stdin)['access_token'])"
)"
curl -s http://127.0.0.1:8000/api/v1/feedback/summary \
  -H "Authorization: Bearer ${TOKEN}"
```

La salida no contiene UUID ni registros individuales. Se conserva en SQLite
local con retención finita; no es una base compartida ni un corpus de
reentrenamiento.

Con el rol administrativo de demostración, `/admin` muestra health, la
disponibilidad factual del baseline y el resumen en una tabla agregada por
versión de modelo, clase sugerida y decisión. `Operational data` permanece
`Not connected`: el Dashboard no ofrece navegación ni consulta de registros
individuales, aunque Compose ya define una persistencia PostgreSQL pendiente de
verificación dinámica y migraciones gobernadas.

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

No se incorporan narrativas CFPB, predicciones por fila, datasets, secretos ni
binarios de modelo a Git. Las clases débiles requieren revisión humana
reforzada. El repositorio contiene empaquetado y automatización de despliegue,
pero no hay una URL cloud, smoke remoto, rollback probado ni monitorización que
acrediten operación productiva.
